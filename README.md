# Video Broadcaster 🎥✨

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35.svg)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-Powered Virtual Camera with Real-Time Background Processing**

An advanced video broadcasting application that leverages YOLOv8 segmentation models to provide real-time background effects for video streaming. Perfect for content creators, streamers, and video conferencing with professional-grade background processing capabilities.

## 🌟 Features

### 🎯 **Real-Time AI Segmentation**
- **YOLOv8 Integration**: State-of-the-art person segmentation using YOLOv8m-seg model
- **GPU Acceleration**: Automatic CUDA/MPS detection for optimal performance
- **Real-Time Processing**: Low-latency video processing for smooth streaming

### 🎨 **Background Effects**
- **Blur Background**: Customizable Gaussian blur with adjustable intensity (1-51)
- **Black Background**: Clean removal of background for professional presentations
- **Custom Background**: Replace background with your own images
- **No Processing**: Original video feed without modifications

### 📹 **Virtual Camera Support**
- **pyvirtualcam Integration**: Creates a virtual camera device
- **Multi-Platform**: Works with OBS, Zoom, Teams, and other streaming software
- **Configurable Resolution**: Maintains original camera resolution and aspect ratio
- **Adjustable FPS**: Frame rate control (1-60 FPS) for performance optimization

### 🌐 **Web-Based Control Panel**
- **Modern UI**: Clean, responsive web interface
- **Real-Time Controls**: Start/stop streaming with live parameter adjustment
- **Device Detection**: Automatic camera device discovery
- **Status Monitoring**: Live streaming status and performance metrics

### ⚡ **Performance Optimizations**
- **Frame Skipping**: Intelligent frame processing for better performance
- **Memory Management**: Optimized memory usage for long streaming sessions
- **Multi-Threading**: Non-blocking video processing
- **Error Recovery**: Automatic error handling and recovery mechanisms
## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Conda (recommended) or pip
- Webcam or video input device
- CUDA-compatible GPU (optional, for better performance)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/rohan911438/Video-Broadcaster.git
cd Video-Broadcaster
```

2. **Create and activate conda environment:**
```bash
conda create -n broadcaster_live python=3.9
conda activate broadcaster_live
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download YOLOv8 model:**
The YOLOv8m-seg model will be automatically downloaded on first run, or you can download it manually:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8m-seg.pt')"
```

5. **Run the application:**
```bash
python main.py
```

6. **Open your browser:**
Navigate to `http://localhost:8000` to access the control panel.

## 🎮 Usage

### Web Interface
1. **Start the application** using `python main.py`
2. **Open the web interface** at `http://localhost:8000`
3. **Configure settings:**
   - Select camera source (0, 1, 2, etc.)
   - Set desired FPS (1-60)
   - Choose background effect (blur, black, custom, none)
   - Adjust blur strength (1-51, for blur effect)
4. **Click "Start Stream"** to begin virtual camera output
5. **Use in your streaming software** (OBS, Zoom, etc.) by selecting the virtual camera

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/start` | GET | Start streaming with parameters |
| `/stop` | GET | Stop streaming |
| `/status` | GET | Get current streaming status |
| `/devices` | GET | List available camera devices |
| `/health` | GET | Health check |

### Example API Usage
```bash
# Start streaming with blur background
curl "http://localhost:8000/start?source=0&fps=30&blur_strength=21&background=blur"

# Stop streaming
curl "http://localhost:8000/stop"

# Check status
curl "http://localhost:8000/status"
```

## ⚙️ Configuration

The application uses a modular configuration system in `config.py`:

### Stream Settings
```python
default_fps: int = 15          # Default frames per second
max_fps: int = 60             # Maximum allowed FPS
min_fps: int = 1              # Minimum allowed FPS
default_blur_strength: int = 21  # Default blur intensity
max_blur_strength: int = 51    # Maximum blur strength
min_blur_strength: int = 1     # Minimum blur strength
```

### Model Settings
```python
model_path: str = "yolov8m-seg.pt"  # YOLOv8 model path
confidence_threshold: float = 0.5    # Detection confidence
iou_threshold: float = 0.45          # IoU threshold
person_class_id: int = 0             # COCO person class
```

### Server Settings
```python
host: str = "0.0.0.0"         # Server host
port: int = 8000              # Server port
static_dir: str = "static"    # Static files directory
```

## 🏗️ Architecture

```
Video Broadcaster
├── main.py              # FastAPI application and API endpoints
├── config.py            # Configuration management
├── engine.py            # YOLOv8 segmentation engine
├── stream_utils.py      # Video streaming and processing
├── logger_utils.py      # Logging utilities
├── utils.py             # Helper functions
├── requirements.txt     # Python dependencies
├── static/              # Web interface files
│   ├── index.html       # Main web interface
│   ├── wallhaven.png    # Default background image
│   └── KNA.png          # Logo/assets
└── logs/                # Application logs
```

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.104.1 | Web framework and API |
| Uvicorn | 0.24.0 | ASGI server |
| Ultralytics | 8.0.196 | YOLOv8 model inference |
| OpenCV | 4.8.1.78 | Computer vision operations |
| PyTorch | 2.0.1+ | Deep learning framework |
| pyvirtualcam | Latest | Virtual camera creation |
| NumPy | 1.24.3 | Numerical operations |

## 🎯 Use Cases

### 📺 **Content Creation**
- YouTube videos with professional backgrounds
- Twitch streaming with custom effects
- Educational content with clean backgrounds

### 💼 **Professional Meetings**
- Video conferences with noise-free backgrounds
- Client presentations with branded backgrounds
- Remote work with professional appearance

### 🎮 **Gaming & Streaming**
- Game streaming with face cam effects
- Virtual backgrounds for gaming content
- Real-time background replacement

## 🔧 Troubleshooting

### Common Issues

**Application won't start:**
```bash
# Check if conda environment is activated
conda activate broadcaster_live

# Verify all packages are installed
pip list

# Check for missing model file
ls yolov8m-seg.pt
```

**Virtual camera not detected:**
- Restart your streaming software after starting the broadcaster
- Check if pyvirtualcam is properly installed
- Verify camera permissions on your system

**Poor performance:**
- Lower the FPS setting
- Reduce blur strength
- Ensure GPU drivers are updated for CUDA acceleration

**Camera not found:**
- Check camera connections
- Try different source IDs (0, 1, 2, etc.)
- Verify camera isn't being used by another application

## 📊 Performance Tips

1. **GPU Acceleration**: Use CUDA-compatible GPU for better performance
2. **Frame Rate**: Lower FPS for better stability on slower systems
3. **Resolution**: Lower camera resolution for improved processing speed
4. **Background Effects**: "None" or "Black" are fastest, "Blur" is most intensive

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for the YOLOv8 model
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) for virtual camera support
- COCO dataset for providing the training data for person segmentation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/rohan911438/Video-Broadcaster/issues) page
2. Create a new issue with detailed description
3. Include system information and error logs

## 🔮 Roadmap

- [ ] Multiple person tracking and segmentation
- [ ] Real-time background image upload
- [ ] Advanced video filters and effects
- [ ] WebRTC integration for browser-based streaming
- [ ] Mobile app support
- [ ] Cloud deployment options

---

**Made with ❤️ by [rohan911438](https://github.com/rohan911438)**

⭐ **Star this repository if you found it helpful!**

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
