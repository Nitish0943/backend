#!/usr/bin/env python3
"""
Health check script for the eye tracking backend
"""

import sys
import os

def check_opencv():
    """Check if OpenCV can be imported successfully"""
    try:
        import cv2
        print(f"✅ OpenCV imported successfully - version: {cv2.Version()}")
        
        # Check if cascade files exist
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        
        if os.path.exists(face_cascade_path):
            print(f"✅ Face cascade file found: {face_cascade_path}")
        else:
            print(f"❌ Face cascade file not found: {face_cascade_path}")
            return False
            
        if os.path.exists(eye_cascade_path):
            print(f"✅ Eye cascade file found: {eye_cascade_path}")
        else:
            print(f"❌ Eye cascade file not found: {eye_cascade_path}")
            return False
        
        # Test cascade classifier loading
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        
        if not face_cascade.empty():
            print("✅ Face cascade classifier loaded successfully")
        else:
            print("❌ Failed to load face cascade classifier")
            return False
            
        if not eye_cascade.empty():
            print("✅ Eye cascade classifier loaded successfully")
        else:
            print("❌ Failed to load eye cascade classifier")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import OpenCV: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking OpenCV: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies can be imported"""
    dependencies = [
        ('numpy', 'numpy'),
        ('websockets', 'websockets'),
        ('asyncio', 'asyncio'),
        ('json', 'json'),
        ('datetime', 'datetime'),
        ('logging', 'logging')
    ]
    
    all_good = True
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {name}: {e}")
            all_good = False
    
    return all_good

def check_environment():
    """Check environment variables"""
    print("\n🔧 Environment Check:")
    
    host = os.getenv('HOST', 'localhost')
    port = os.getenv('PORT', '5000')
    
    print(f"✅ HOST: {host}")
    print(f"✅ PORT: {port}")
    
    return True

def main():
    """Run all health checks"""
    print("🏥 Eye Tracking Backend Health Check")
    print("=" * 40)
    
    # Check dependencies
    print("\n📦 Dependency Check:")
    deps_ok = check_dependencies()
    
    # Check OpenCV specifically
    print("\n📹 OpenCV Check:")
    opencv_ok = check_opencv()
    
    # Check environment
    env_ok = check_environment()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Health Check Summary:")
    
    if deps_ok and opencv_ok and env_ok:
        print("✅ All checks passed! Backend should work correctly.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 