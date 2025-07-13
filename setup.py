#!/usr/bin/env python3
"""
Setup script for the eye tracking backend
This script helps install dependencies and verify the environment
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        "cv2",
        "numpy", 
        "flask",
        "flask_socketio"
    ]
    
    print("🔍 Testing imports...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            return False
    return True

def check_webcam():
    """Check if webcam is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam is accessible")
            cap.release()
            return True
        else:
            print("❌ Webcam is not accessible")
            return False
    except Exception as e:
        print(f"❌ Error checking webcam: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up eye tracking backend...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Check webcam
    if not check_webcam():
        print("⚠️  Webcam not accessible. Eye tracking may not work properly.")
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("🎯 You can now run the eye tracking backend with: python eye_gaze.py")

if __name__ == "__main__":
    main() 