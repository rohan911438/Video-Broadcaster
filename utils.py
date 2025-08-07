import cv2
import numpy as np
import time
import os
from datetime import datetime

COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "purple": (128, 0, 128),
    "orange": (0, 165, 255)
}

def validate_camera_source(source_id):
    """Validate if camera source is available"""
    try:
        cap = cv2.VideoCapture(source_id)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            return ret
        return False
    except:
        return False

def get_camera_properties(source_id):
    """Get camera properties like resolution and FPS"""
    try:
        cap = cv2.VideoCapture(source_id)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            cap.release()
            return {"width": width, "height": height, "fps": fps}
        return None
    except:
        return None

def create_log_entry(message, log_type="INFO"):
    """Create a formatted log entry with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{log_type}] {message}"

def ensure_odd_number(value):
    """Ensure a number is odd (required for some OpenCV operations)"""
    if value % 2 == 0:
        return value + 1
    return value

def resize_image(image, max_width=None, max_height=None):
    """Resize image while maintaining aspect ratio"""
    if max_width is None and max_height is None:
        return image
    
    h, w = image.shape[:2]
    
    if max_width and max_height:
        scale = min(max_width / w, max_height / h)
    elif max_width:
        scale = max_width / w
    else:
        scale = max_height / h
    
    if scale < 1:
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return image

def add_text_overlay(image, text, position=(10, 30), color="white", font_scale=0.7, thickness=2):
    """Add text overlay to image"""
    color_bgr = COLORS.get(color.lower(), COLORS["white"])
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color_bgr, thickness)
    return image

def benchmark_function(func, *args, **kwargs):
    """Benchmark function execution time"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time