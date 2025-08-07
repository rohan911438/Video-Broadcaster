from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import time
import threading
import os
import cv2
import numpy as np
import pyvirtualcam
from ultralytics import YOLO

# Initialize FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# Global variables for video processing
video_feed_active = False
camera_device_index = 0
fps_setting = 15
blur_strength = 10
background_mode = "none"
camera = None
cap = None
model = None
video_thread = None

# Function to list available camera devices
def list_camera_devices():
    devices = []
    for i in range(10):  # Check up to 10 possible camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            backend_name = cap.getBackendName()
            # Attempt to get a more descriptive name if possible
            # This part is tricky as OpenCV doesn't directly expose device names easily
            # On Windows, it might show "DirectShow" or "MSMF"
            # On Linux, it might show "V4L2"
            # For now, we'll just use a generic name
            devices.append({"id": i, "name": f"Camera {i} ({backend_name})"})
            cap.release()
    return devices

# Function to start video feed
def start_video_feed():
    global video_feed_active, camera, cap, model

    # Initialize YOLO model if not already loaded
    if model is None:
        try:
            model = YOLO("yolov8n.pt")  # Ensure yolov8n.pt is in the same directory or provide full path
            print("YOLO model loaded successfully.")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            video_feed_active = False
            return

    # Initialize virtual camera
    # Try common formats
    pixel_format = None
    for fmt in ['BGRX', 'RGBA', 'MJPG']:
        try:
            camera = pyvirtualcam.Camera(width=640, height=480, fps=fps_setting, fmt=fmt)
            pixel_format = fmt
            print(f"Using virtual camera pixel format: {fmt}")
            break
        except ValueError:
            print(f"Pixel format {fmt} not supported by pyvirtualcam, trying next...")
            continue
    
    if not pixel_format:
        print("Error: No suitable pixel format found for virtual camera. Please ensure a virtual camera is installed and active.")
        video_feed_active = False
        return

    # Open default camera
    cap = cv2.VideoCapture(camera_device_index)
    if not cap.isOpened():
        print(f"Error: Could not open video stream from device {camera_device_index}. Please check if the camera is in use or not available.")
        video_feed_active = False
        return

    print(f"Starting video feed from camera {camera_device_index} at {fps_setting} FPS.")

    while video_feed_active:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        processed_frame = frame.copy()

        # Apply background effects
        if background_mode == "blur" and blur_strength > 0:
            # Ensure blur_strength is an odd number for GaussianBlur kernel size
            ksize = (blur_strength, blur_strength)
            processed_frame = cv2.GaussianBlur(processed_frame, ksize, 0)
        elif background_mode == "default":
            # Example: Replace background with a solid color or an image
            # For simplicity, let's just make it a solid blue background for now
            processed_frame[:] = (255, 0, 0) # Blue color (BGR)

        # Perform object detection and overlay on the processed frame
        if model:
            results = model(frame, verbose=False) # verbose=False to suppress output
            annotated_frame = results[0].plot()
            # Overlay annotated frame on the processed background
            # This is a simplified overlay. For proper background removal,
            # you'd need segmentation masks from YOLO or another model.
            # For now, we'll just use the annotated frame directly if background is 'none'
            # or if we want to show detection on top of blurred/default background.
            if background_mode == "none":
                processed_frame = annotated_frame
            else:
                # Simple blending: This will just put the annotated frame on top,
                # not truly remove background. A more advanced solution is needed for that.
                # For demonstration, let's just show the annotated frame.
                processed_frame = annotated_frame


        # Convert frame to the virtual camera's pixel format
        if pixel_format == 'BGRX':
            processed_frame_bgrx = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2BGRA)
            camera.send(processed_frame_bgrx)
        elif pixel_format == 'RGBA':
            processed_frame_rgba = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGBA)
            camera.send(processed_frame_rgba)
        elif pixel_format == 'MJPG':
            processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            camera.send(processed_frame_rgb)
        else:
            camera.send(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))

        camera.sleep_until_next_frame()

    # Release resources
    if cap:
        cap.release()
    if camera:
        camera.close()
    print("Video feed stopped.")

# Function to stop video feed
def stop_video_feed():
    global video_feed_active
    video_feed_active = False

# Route to serve the main page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to list camera devices
@app.get("/devices")
async def get_devices():
    devices = list_camera_devices()
    return JSONResponse(content=devices)

# Route to start the video feed
@app.get("/start")
async def start_feed(
    source: int = Query(..., description="Camera device index"),
    fps: int = Query(15, description="Frames per second"),
    blur: int = Query(0, description="Blur strength (odd number)"),
    background: str = Query("none", description="Background mode (none, blur, default)")
):
    global video_feed_active, camera_device_index, fps_setting, blur_strength, background_mode, video_thread

    if video_feed_active:
        return {"message": "Video feed is already active. Please stop it first."}

    camera_device_index = source
    fps_setting = fps
    blur_strength = blur if blur % 2 != 0 else blur + 1 # Ensure blur strength is odd
    background_mode = background

    video_feed_active = True
    video_thread = threading.Thread(target=start_video_feed)
    video_thread.start()
    return {"message": "Video feed started."}

# Route to stop the video feed
@app.get("/stop")
async def stop_feed():
    global video_feed_active, video_thread
    if video_feed_active:
        stop_video_feed()
        if video_thread and video_thread.is_alive():
            video_thread.join(timeout=5) # Wait for the thread to finish
        return {"message": "Video feed stopping."}
    return {"message": "Video feed is not active."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)