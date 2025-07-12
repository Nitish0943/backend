#!/bin/bash

echo "========================================"
echo "    Eye Tracking Backend Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

echo "Python found! Checking version..."
python3 --version

echo
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Try running: pip3 install --upgrade pip"
    exit 1
fi

echo
echo "Testing setup..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo "ERROR: Setup verification failed"
    exit 1
fi

echo
echo "========================================"
echo "    Setup completed successfully!"
echo "========================================"
echo
echo "The eye tracking backend will start automatically"
echo "when you begin an interview in the frontend."
echo 