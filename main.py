import uvicorn
import numpy as np
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import threading
from stream_utils import Streaming
from config import config
from logger_utils import logger

app = FastAPI(
    title="Video Broadcaster API",
    description="AI-Powered Virtual Camera with YOLO segmentation",
    version="2.0.0"
)

app.mount("/static", StaticFiles(directory=config.server.static_dir), name="static")

stream_thread = None
streaming = Streaming()

logger.info("Video Broadcaster application started")


@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


@app.get("/start")
def start_stream(
    source: int = Query(0),
    fps: int = Query(config.stream.default_fps),
    blur_strength: int = Query(config.stream.default_blur_strength),
    background: str = Query("none")
):
    """Start video streaming with specified parameters"""
    global stream_thread

    if streaming.running:
        logger.warning("Attempt to start stream while already running")
        return JSONResponse(content={"message": "Stream already running"}, status_code=400)

    if fps < config.stream.min_fps or fps > config.stream.max_fps:
        logger.error(f"Invalid FPS value: {fps}")
        return JSONResponse(content={"message": f"Invalid FPS value ({config.stream.min_fps}-{config.stream.max_fps})"}, status_code=400)

    if blur_strength < config.stream.min_blur_strength or blur_strength > config.stream.max_blur_strength:
        logger.error(f"Invalid blur strength: {blur_strength}")
        return JSONResponse(content={"message": f"Invalid blur strength ({config.stream.min_blur_strength}-{config.stream.max_blur_strength})"}, status_code=400)

    try:
        streaming.update_streaming_config(
            in_source=source, 
            out_source=None, 
            fps=fps, 
            blur_strength=blur_strength, 
            background=background
        )
        
        stream_thread = threading.Thread(
            target=streaming.stream_video, 
            args=(),
            daemon=True
        )
        stream_thread.start()
        
        logger.info(f"Stream started - Source: {source}, FPS: {fps}, Blur: {blur_strength}, Background: {background}")
        return {"message": f"Streaming started from source {source}: {fps} FPS and blur strength {blur_strength}"}
        
    except Exception as e:
        logger.error(f"Failed to start stream: {str(e)}")
        return JSONResponse(content={"message": f"Failed to start stream: {str(e)}"}, status_code=500)


@app.get("/stop")
def stop_stream():
    if streaming.running:
        streaming.update_running_status(False)
        if stream_thread and stream_thread.is_alive():
            stream_thread.join(timeout=5)
        return {"message": "Streaming stopped"}
    else:
        return {"message": "Stream is not running"}


@app.get("/devices")
def devices():
    return streaming.list_available_devices()


@app.get("/status")
def get_status():
    return {
        "running": streaming.running,
        "input_source": streaming.input_source,
        "fps": streaming.fps,
        "blur_strength": streaming.blur_strength,
        "background": streaming.background
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Video Broadcaster API is running"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)