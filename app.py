#!/usr/bin/env python3
"""
Simple HTTP + WebSocket server for Render deployment
Combines your existing eye tracking with HTTP health checks
"""

import asyncio
import json
import os
from datetime import datetime
import logging
from aiohttp import web, WSMsgType
from aiohttp.web import Response, WebSocketResponse
import cv2
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get host and port from environment variables
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 10000))

class EyeTracker:
    def __init__(self):
        self.connected_clients = set()
        self.is_running = False
        
        try:
            # Load cascade classifiers
            face_cascade_path = cv2.__path__[0] + '/data/haarcascade_frontalface_default.xml'
            eye_cascade_path = cv2.__path__[0] + '/data/haarcascade_eye.xml'
            
            if not os.path.exists(face_cascade_path):
                logger.warning(f"Face cascade file not found: {face_cascade_path}")
                self.face_cascade = None
            else:
                self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
                
            if not os.path.exists(eye_cascade_path):
                logger.warning(f"Eye cascade file not found: {eye_cascade_path}")
                self.eye_cascade = None
            else:
                self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
                
            if self.face_cascade and not self.face_cascade.empty() and self.eye_cascade and not self.eye_cascade.empty():
                logger.info("✅ Cascade classifiers loaded successfully")
            else:
                logger.warning("⚠️ Some cascade classifiers failed to load - using simulation mode")
                
        except Exception as e:
            logger.warning(f"⚠️ Error loading cascade classifiers: {e} - using simulation mode")
            self.face_cascade = None
            self.eye_cascade = None

    async def handle_websocket(self, request):
        """Handle WebSocket connections"""
        ws = WebSocketResponse()
        await ws.prepare(request)

        self.connected_clients.add(ws)
        client_ip = request.remote if request.remote else "unknown"
        logger.info(f"✅ Client connected from {client_ip}. Total clients: {len(self.connected_clients)}")

        try:
            # Send welcome message
            await ws.send_str(json.dumps({
                "type": "connection",
                "message": "Eye tracking connected",
                "timestamp": datetime.now().isoformat(),
                "server_info": {
                    "version": "1.0.0"
                }
            }))

            # Handle messages
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await self.process_message(ws, data)
                    except json.JSONDecodeError:
                        logger.warning(f"❌ Invalid JSON received from {client_ip}")
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f"❌ WebSocket error: {ws.exception()}")
                    break

        except Exception as e:
            logger.error(f"❌ WebSocket error: {e}")
        finally:
            self.connected_clients.discard(ws)
            logger.info(f"👋 Client disconnected. Total clients: {len(self.connected_clients)}")

        return ws

    async def process_message(self, ws, data):
        """Process incoming WebSocket messages"""
        message_type = data.get('type')
        
        if message_type == 'start_tracking':
            logger.info("🎯 Starting eye tracking...")
            await self.start_eye_tracking(ws)
        elif message_type == 'stop_tracking':
            logger.info("⏹️ Stopping eye tracking...")
            self.is_running = False
        elif message_type == 'ping':
            await ws.send_str(json.dumps({
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            }))
        else:
            logger.warning(f"❓ Unknown message type: {message_type}")

    async def start_eye_tracking(self, ws):
        """Start eye tracking simulation (since cameras aren't available in cloud)"""
        self.is_running = True
        
        try:
            # Simulate eye tracking data since cameras aren't available in cloud environments
            counter = 0
            while self.is_running:
                counter += 1
                
                # Simulate realistic eye tracking data
                eye_data = {
                    "type": "eye_data",
                    "timestamp": datetime.now().isoformat(),
                    "face_detected": True,
                    "eye_count": 2,
                    "looking_away": counter % 10 < 8,  # Looking away 20% of the time
                    "confidence": 0.8 + (counter % 5) * 0.04,  # Varying confidence
                    "note": "Simulated data - camera not available in cloud environment"
                }
                
                try:
                    await ws.send_str(json.dumps(eye_data))
                except Exception as e:
                    logger.error(f"❌ Error sending data: {e}")
                    break
                
                await asyncio.sleep(0.5)  # Send updates every 500ms
                
        except Exception as e:
            logger.error(f"❌ Eye tracking error: {e}")

async def health_check(request):
    """Health check endpoint for Render"""
    return Response(text=json.dumps({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "eye-tracking-backend",
        "version": "1.0.0",
        "port": PORT
    }), content_type='application/json')

async def websocket_info(request):
    """WebSocket connection info endpoint"""
    return Response(text=json.dumps({
        "websocket_url": f"ws://{request.host}/ws",
        "websocket_url_secure": f"wss://{request.host}/ws",
        "instructions": "Connect to /ws endpoint for WebSocket communication",
        "supported_messages": [
            {"type": "ping", "description": "Health check ping"},
            {"type": "start_tracking", "description": "Start eye tracking"},
            {"type": "stop_tracking", "description": "Stop eye tracking"}
        ]
    }), content_type='application/json')

async def create_app():
    """Create the web application"""
    app = web.Application()
    
    # Initialize eye tracker
    tracker = EyeTracker()
    
    # HTTP routes
    app.router.add_get('/health', health_check)
    app.router.add_get('/', websocket_info)
    
    # WebSocket route
    app.router.add_get('/ws', tracker.handle_websocket)
    
    return app

async def main():
    """Main function to start the server"""
    try:
        app = await create_app()
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, HOST, PORT)
        await site.start()
        
        logger.info(f"🚀 Eye tracking server started on {HOST}:{PORT}")
        logger.info(f"📡 WebSocket endpoint: ws://{HOST}:{PORT}/ws")
        logger.info(f"🏥 Health check: http://{HOST}:{PORT}/health")
        
        # Keep the server running
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            logger.info("🛑 Server stopped by user")
        finally:
            await runner.cleanup()
            
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
