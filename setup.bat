@echo off
echo ========================================
echo    Eye Tracking Backend Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Checking version...
python --version

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try running: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo Testing setup...
python setup.py

if errorlevel 1 (
    echo ERROR: Setup verification failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Setup completed successfully!
echo ========================================
echo.
echo The eye tracking backend will start automatically
echo when you begin an interview in the frontend.
echo.
pause 