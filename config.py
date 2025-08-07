"""
Configuration settings for Video Broadcaster application
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class StreamConfig:
    """Configuration for streaming settings"""
    default_fps: int = 15
    max_fps: int = 60
    min_fps: int = 1
    default_blur_strength: int = 21
    max_blur_strength: int = 51
    min_blur_strength: int = 1
    default_erode_size: int = 5
    default_erode_intensity: int = 2
    max_camera_check_range: int = 10

@dataclass
class ModelConfig:
    """Configuration for YOLO model"""
    model_path: str = "yolov8m-seg.pt"
    confidence_threshold: float = 0.5
    iou_threshold: float = 0.45
    person_class_id: int = 0  # COCO class ID for person

@dataclass
class ServerConfig:
    """Configuration for FastAPI server"""
    host: str = "0.0.0.0"
    port: int = 8000
    static_dir: str = "static"
    default_background_image: str = "static/wallhaven.png"
    log_level: str = "info"

@dataclass
class AppConfig:
    """Main application configuration"""
    stream: StreamConfig = StreamConfig()
    model: ModelConfig = ModelConfig()
    server: ServerConfig = ServerConfig()
    
    def __post_init__(self):
        # Validate model file exists
        if not os.path.exists(self.model.model_path):
            raise FileNotFoundError(f"YOLO model file not found: {self.model.model_path}")
        
        # Create static directory if it doesn't exist
        if not os.path.exists(self.server.static_dir):
            os.makedirs(self.server.static_dir)

# Global configuration instance
config = AppConfig()

# Environment variable overrides
if os.getenv("BROADCASTER_HOST"):
    config.server.host = os.getenv("BROADCASTER_HOST")

if os.getenv("BROADCASTER_PORT"):
    config.server.port = int(os.getenv("BROADCASTER_PORT"))

if os.getenv("YOLO_MODEL_PATH"):
    config.model.model_path = os.getenv("YOLO_MODEL_PATH")
