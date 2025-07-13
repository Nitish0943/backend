#!/usr/bin/env python3
"""
Test script for the Eye Tracking WebSocket Server
Run this locally before deploying to Render
"""

import asyncio
import json
import sys
import websockets
from datetime import datetime
import requests

async def test_websocket(url):
    """Test WebSocket functionality"""
    try:
        print(f"🔌 Testing WebSocket connection to {url}")
        
        async with websockets.connect(url, ping_interval=None) as websocket:
            print("✅ WebSocket connected successfully")
            
            # Test ping
            ping_msg = {
                "type": "ping",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(ping_msg))
            print("📤 Sent ping message")
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            data = json.loads(response)
            print(f"📥 Received: {data}")
            
            if data.get('type') == 'pong':
                print("✅ Ping/Pong test passed")
            else:
                print("⚠️ Unexpected response to ping")
            
            # Test start tracking
            start_msg = {
                "type": "start_tracking",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(start_msg))
            print("📤 Sent start_tracking message")
            
            # Receive a few eye tracking messages
            for i in range(3):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    data = json.loads(response)
                    print(f"📥 Eye data {i+1}: {data.get('type', 'unknown')}")
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout waiting for eye data {i+1}")
                    break
            
            # Test stop tracking
            stop_msg = {
                "type": "stop_tracking",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(stop_msg))
            print("📤 Sent stop_tracking message")
            
            print("✅ WebSocket test completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def test_health_endpoint(url):
    """Test HTTP health endpoint"""
    try:
        print(f"🏥 Testing health endpoint: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data.get('status', 'unknown')}")
            print(f"📊 Service: {data.get('service', 'unknown')}")
            print(f"📅 Timestamp: {data.get('timestamp', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

def test_info_endpoint(url):
    """Test info endpoint"""
    try:
        print(f"📋 Testing info endpoint: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Info endpoint working")
            print(f"🔗 WebSocket URL: {data.get('websocket_url', 'unknown')}")
            print(f"🔒 Secure WebSocket URL: {data.get('websocket_url_secure', 'unknown')}")
            return True
        else:
            print(f"❌ Info endpoint failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Info endpoint test failed: {e}")
        return False

async def main():
    """Run all tests"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = "http://localhost:10000"
    
    print("🧪 Eye Tracking Backend Test Suite")
    print("=" * 50)
    print(f"🎯 Testing server at: {base_url}")
    print()
    
    # Determine WebSocket URL
    if base_url.startswith('https://'):
        ws_url = base_url.replace('https://', 'wss://') + '/ws'
    else:
        ws_url = base_url.replace('http://', 'ws://') + '/ws'
    
    # Run tests
    results = []
    
    # Test 1: Health endpoint
    print("🏥 Test 1: Health Endpoint")
    health_result = test_health_endpoint(f"{base_url}/health")
    results.append(("Health Endpoint", health_result))
    print()
    
    # Test 2: Info endpoint
    print("📋 Test 2: Info Endpoint")
    info_result = test_info_endpoint(f"{base_url}/info")
    results.append(("Info Endpoint", info_result))
    print()
    
    # Test 3: WebSocket functionality
    print("🔌 Test 3: WebSocket Functionality")
    ws_result = await test_websocket(ws_url)
    results.append(("WebSocket", ws_result))
    print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed! Your server is ready for production.")
        return 0
    else:
        print("🚨 Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        sys.exit(1)
