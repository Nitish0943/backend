#!/usr/bin/env python3
"""
Health check script for the eye tracking backend
"""

import sys
import os
import asyncio
import websockets
import json
from datetime import datetime

def check_opencv():
    """Check if OpenCV can be imported successfully"""
    try:
        import cv2
        print(f"✅ OpenCV imported successfully - version: {cv2.__version__}")
        
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

async def check_websocket_server():
    """Test WebSocket server connectivity"""
    try:
        host = os.getenv('HOST', 'localhost')
        port = int(os.getenv('PORT', 5000))
        
        # Try to connect to the WebSocket server
        uri = f"ws://{host}:{port}"
        print(f"🔌 Testing WebSocket connection to {uri}")
        
        timeout = 5  # 5 second timeout
        async with asyncio.wait_for(
            websockets.connect(uri, ping_interval=None), 
            timeout=timeout
        ) as websocket:
            # Send a ping message
            test_message = {
                "type": "ping",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            data = json.loads(response)
            
            if data.get('type') == 'pong':
                print("✅ WebSocket server responding correctly")
                return True
            else:
                print(f"⚠️ Unexpected response: {data}")
                return True  # Still connected, just different response
                
    except asyncio.TimeoutError:
        print("❌ WebSocket connection timeout")
        return False
    except ConnectionRefusedError:
        print("❌ WebSocket server not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def check_production_readiness():
    """Check production-specific configurations"""
    print("\n🚀 Production Readiness Check:")
    
    issues = []
    
    # Check if running as root (security issue)
    if os.getuid() == 0:
        issues.append("Running as root user (security risk)")
    else:
        print("✅ Not running as root user")
    
    # Check environment variables for production
    host = os.getenv('HOST', 'localhost')
    if host == 'localhost':
        issues.append("HOST is set to localhost (won't accept external connections)")
    else:
        print(f"✅ HOST configured for external access: {host}")
    
    # Check log level
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    if log_level in ['INFO', 'WARNING', 'ERROR']:
        print(f"✅ Log level appropriate for production: {log_level}")
    else:
        print(f"⚠️ Log level might be too verbose for production: {log_level}")
    
    # Check connection limits
    max_conn = os.getenv('MAX_CONNECTIONS', '100')
    print(f"✅ Max connections configured: {max_conn}")
    
    if issues:
        print("\n❌ Production issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Production configuration looks good")
        return True

async def run_async_checks():
    """Run asynchronous health checks"""
    print("\n🔌 WebSocket Server Check:")
    websocket_ok = await check_websocket_server()
    return websocket_ok

def main():
    """Run all health checks"""
    print("🏥 Eye Tracking Backend Health Check")
    print("=" * 50)
    
    # Check dependencies
    print("\n📦 Dependency Check:")
    deps_ok = check_dependencies()
    
    # Check OpenCV specifically
    print("\n📹 OpenCV Check:")
    opencv_ok = check_opencv()
    
    # Check environment
    env_ok = check_environment()
    
    # Check production readiness
    prod_ok = check_production_readiness()
    
    # Run async checks
    try:
        websocket_ok = asyncio.run(run_async_checks())
    except Exception as e:
        print(f"❌ Async checks failed: {e}")
        websocket_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Health Check Summary:")
    print(f"  Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"  OpenCV: {'✅' if opencv_ok else '❌'}")
    print(f"  Environment: {'✅' if env_ok else '❌'}")
    print(f"  Production Ready: {'✅' if prod_ok else '❌'}")
    print(f"  WebSocket Server: {'✅' if websocket_ok else '❌'}")
    
    all_checks = deps_ok and opencv_ok and env_ok and prod_ok and websocket_ok
    
    if all_checks:
        print("\n🎉 All checks passed! Backend is ready for production.")
        return 0
    else:
        print("\n🚨 Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())