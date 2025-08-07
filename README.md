# Video Broadcaster - AI-Powered Virtual Camera

A sophisticated real-time video streaming application that uses YOLO v8 for person segmentation and provides various background effects for virtual camera applications.

## Features

### Core Features
- 🎯 **Real-time Person Segmentation** using YOLOv8 model
- 📹 **Virtual Camera Output** compatible with video conferencing apps
- 🎨 **Multiple Background Options**:
  - Black background (remove background)
  - Blur background (keep person sharp, blur everything else)
  - Custom background image
- ⚡ **Adjustable Performance Settings**:
  - Configurable FPS (1-60)
  - Adjustable blur strength
  - Optimized for different hardware capabilities

### Enhanced Features
- 🔍 **Automatic Camera Detection** and validation
- 📊 **Real-time Status Monitoring** with auto-refresh
- 🎚️ **Advanced Controls** with proper validation
- 🛡️ **Robust Error Handling** and recovery
- 📝 **Comprehensive Logging** system
- ⚙️ **Configuration Management** with environment variables
- 🖥️ **Modern Web Interface** with responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam or video input device
- CUDA-compatible GPU (optional, for better performance)

### Step-by-step Installation

1. **Clone or download the repository**
   ```bash
   cd "c:\Users\ABHINAV KUMAR\Desktop\Video Broadcaster"
   ```

2. **Create a virtual environment**
   ```bash
   conda create -n broadcaster_live python=3.9
   conda activate broadcaster_live
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify YOLO model**
   - Ensure `yolov8m-seg.pt` is in the project directory
   - The model will be downloaded automatically on first run if missing

## Usage

### Starting the Application

1. **Activate your environment**
   ```bash
   conda activate broadcaster_live
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Open web interface**
   - Navigate to `http://localhost:8000` in your browser
   - The interface will automatically detect available cameras

### Web Interface Guide

1. **Camera Setup**:
   - Click "List Devices" to detect available cameras
   - Select your preferred camera from the dropdown

2. **Configuration**:
   - **FPS**: Set frame rate (1-60, higher = smoother but more CPU intensive)
   - **Blur Strength**: Adjust background blur intensity (odd numbers only)
   - **Background**: Choose between black, blur, or custom background

3. **Control Stream**:
   - **Start Stream**: Begin virtual camera output
   - **Stop Stream**: End the stream
   - **Get Status**: Check current stream status
   - **Auto Refresh**: Enable automatic status updates

### Virtual Camera Usage

Once the stream is started, the virtual camera will be available in:
- Zoom, Teams, Skype, Discord
- OBS Studio, Streamlabs
- Any application that supports virtual cameras

## Configuration

### Environment Variables
```bash
# Server configuration
BROADCASTER_HOST=0.0.0.0        # Server host
BROADCASTER_PORT=8000           # Server port

# Model configuration  
YOLO_MODEL_PATH=yolov8m-seg.pt  # Path to YOLO model
```

### Advanced Settings
Edit `config.py` to modify:
- Default FPS and blur settings
- Model confidence thresholds
- Camera detection range
- Logging levels

## API Endpoints

The application provides a REST API:

- `GET /` - Web interface
- `GET /devices` - List available cameras
- `GET /start` - Start streaming with parameters
- `GET /stop` - Stop streaming
- `GET /status` - Get current status
- `GET /health` - Health check

## Troubleshooting

### Common Issues

1. **No cameras detected**
   - Check camera connections
   - Ensure camera isn't used by other applications
   - Try different camera indices

2. **Low performance**
   - Reduce FPS setting
   - Lower blur strength
   - Use GPU acceleration if available

3. **Virtual camera not appearing**
   - Install OBS Virtual Camera
   - Restart video applications
   - Check camera permissions

4. **Model loading errors**
   - Verify `yolov8m-seg.pt` exists
   - Check internet connection for model download
   - Ensure sufficient disk space

### Performance Optimization

- **GPU Acceleration**: CUDA or MPS will be used automatically if available
- **Frame Skipping**: Higher original camera FPS with lower output FPS
- **Memory Management**: Automatic cleanup and error recovery

## File Structure

```
Video Broadcaster/
├── main.py              # FastAPI server and routes
├── engine.py            # YOLO segmentation engine
├── stream_utils.py      # Video streaming utilities
├── utils.py             # General utility functions
├── config.py            # Configuration management
├── logger_utils.py      # Logging utilities
├── requirements.txt     # Python dependencies
├── yolov8m-seg.pt      # YOLO model (auto-downloaded)
├── static/             # Web interface files
│   ├── index.html      # Main web interface
│   ├── wallhaven.png   # Background image
│   └── KNA.png         # Logo
└── logs/               # Application logs (auto-created)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please ensure you comply with the licenses of all dependencies, including YOLOv8 and other libraries.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in the `logs/` directory
3. Create an issue with detailed error information

---

**Enjoy your enhanced video streaming experience!** 🎥✨
