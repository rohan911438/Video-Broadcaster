@echo off
echo ========================================
echo    Video Broadcaster Startup Script
echo ========================================
echo.

:: Check if conda is available
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda first
    pause
    exit /b 1
)

:: Check if environment exists
call conda env list | findstr broadcaster_live >nul
if %ERRORLEVEL% NEQ 0 (
    echo Creating conda environment 'broadcaster_live'...
    call conda create -n broadcaster_live python=3.9 -y
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create conda environment
        pause
        exit /b 1
    )
)

:: Activate environment
echo Activating conda environment...
call conda activate broadcaster_live
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate conda environment
    pause
    exit /b 1
)

:: Install requirements
echo Checking and installing requirements...
pip install -r requirements.txt --upgrade
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

:: Check if YOLO model exists
if not exist "yolov8m-seg.pt" (
    echo WARNING: YOLO model file not found. It will be downloaded on first run.
    echo This may take a few minutes depending on your internet connection.
    echo.
)

:: Start the application
echo.
echo ========================================
echo Starting Video Broadcaster...
echo ========================================
echo.
echo Web interface will be available at: http://localhost:8000
echo Press Ctrl+C to stop the application
echo.

python main.py

echo.
echo Application stopped.
pause
