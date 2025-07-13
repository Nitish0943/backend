import cv2
import numpy as np
import json
import asyncio
import os
from datetime import datetime
import logging
from websockets.server import serve
from websockets.exceptions import ConnectionClosed

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get host and port from environment variables (for cloud hosting)
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5000))

# Production settings
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 100))
PING_INTERVAL = int(os.getenv('PING_INTERVAL', 20))
PING_TIMEOUT = int(os.getenv('PING_TIMEOUT', 20))

class EyeTracker:
    def __init__(self):
        try:
            # Load cascade classifiers with error handling
            face_cascade_path = cv2.__path__[0] + '/data/haarcascade_frontalface_default.xml'
            eye_cascade_path = cv2.__path__[0] + '/data/haarcascade_eye.xml'
            
            if not os.path.exists(face_cascade_path):
                logger.error(f"❌ Face cascade file not found: {face_cascade_path}")
                raise FileNotFoundError(f"Face cascade file not found: {face_cascade_path}")
                
            if not os.path.exists(eye_cascade_path):
                logger.error(f"❌ Eye cascade file not found: {eye_cascade_path}")
                raise FileNotFoundError(f"Eye cascade file not found: {eye_cascade_path}")
            
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
            
            # Check if cascade classifiers loaded successfully
            if self.face_cascade.empty():
                logger.error("❌ Failed to load face cascade classifier")
                raise RuntimeError("Failed to load face cascade classifier")
                
            if self.eye_cascade.empty():
                logger.error("❌ Failed to load eye cascade classifier")
                raise RuntimeError("Failed to load eye cascade classifier")
                
            logger.info("✅ Cascade classifiers loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing cascade classifiers: {e}")
            raise
            
        self.connected_clients = set()
        self.is_running = False
        
    async def start_server(self):
        """Start the WebSocket server"""
        try:
            # Add connection limits for production
            server = await serve(
                self.handle_client, 
                HOST, 
                PORT,
                ping_interval=PING_INTERVAL,
                ping_timeout=PING_TIMEOUT,
                max_size=2**20,  # 1MB max message size
                compression=None  # Disable compression for better performance
            )
            logger.info(f"🚀 Eye tracking server started on {HOST}:{PORT}")
            logger.info(f"📡 WebSocket endpoint: ws://{HOST}:{PORT}")
            logger.info(f"🔧 Max connections: {MAX_CONNECTIONS}")
            logger.info(f"🔧 Ping interval: {PING_INTERVAL}s, timeout: {PING_TIMEOUT}s")
            
            # Keep the server running
            await server.wait_closed()
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            raise

    async def handle_client(self, websocket, path):
        """Handle WebSocket client connections"""
        try:
            # Check connection limits
            if len(self.connected_clients) >= MAX_CONNECTIONS:
                await websocket.close(code=1013, reason="Server at capacity")
                logger.warning(f"🚫 Connection rejected - server at capacity ({MAX_CONNECTIONS})")
                return
                
            self.connected_clients.add(websocket)
            client_ip = websocket.remote_address[0] if websocket.remote_address else "unknown"
            logger.info(f"✅ Client connected from {client_ip}. Total clients: {len(self.connected_clients)}")
            
            # Send welcome message
            await websocket.send(json.dumps({
                "type": "connection",
                "message": "Eye tracking connected",
                "timestamp": datetime.now().isoformat(),
                "server_info": {
                    "version": "1.0.0",
                    "max_connections": MAX_CONNECTIONS
                }
            }))
            
            # Keep connection alive and handle messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.process_message(websocket, data)
                except json.JSONDecodeError:
                    logger.warning(f"❌ Invalid JSON received from {client_ip}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format",
                        "timestamp": datetime.now().isoformat()
                    }))
                except Exception as e:
                    logger.error(f"❌ Error processing message from {client_ip}: {e}")
                    
        except ConnectionClosed:
            logger.info(f"🔌 Client {client_ip if 'client_ip' in locals() else 'unknown'} disconnected normally")
        except Exception as e:
            logger.error(f"❌ Client error: {e}")
        finally:
            self.connected_clients.discard(websocket)
            logger.info(f"👋 Client disconnected. Total clients: {len(self.connected_clients)}")

    async def process_message(self, websocket, data):
        """Process incoming WebSocket messages"""
        message_type = data.get('type')
        
        if message_type == 'start_tracking':
            logger.info("🎯 Starting eye tracking...")
            await self.start_eye_tracking(websocket)
        elif message_type == 'stop_tracking':
            logger.info("⏹️ Stopping eye tracking...")
            self.is_running = False
        elif message_type == 'ping':
            await websocket.send(json.dumps({
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            }))
        else:
            logger.warning(f"❓ Unknown message type: {message_type}")

    async def start_eye_tracking(self, websocket):
        """Start eye tracking and send results via WebSocket"""
        self.is_running = True
        
        # Initialize camera with multiple fallback options
        cap = None
        camera_index = 0
        
        # Try different camera indices
        for i in range(3):  # Try indices 0, 1, 2
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    logger.info(f"📹 Camera initialized successfully on index {i}")
                    break
                else:
                    cap.release()
            except Exception as e:
                logger.warning(f"❌ Failed to open camera on index {i}: {e}")
                if cap:
                    cap.release()
        
        if not cap or not cap.isOpened():
            logger.error("❌ Could not open camera on any index")
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Could not open camera - no camera available",
                "timestamp": datetime.now().isoformat()
            }))
            return

        logger.info("📹 Camera initialized successfully")
        
        try:
            while self.is_running:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("❌ Failed to read frame")
                    continue

                # Convert to grayscale for detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces with adjusted parameters for better detection
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=5, 
                    minSize=(30, 30)
                )
                
                eye_data = {
                    "type": "eye_data",
                    "timestamp": datetime.now().isoformat(),
                    "face_detected": len(faces) > 0,
                    "eye_count": 0,
                    "looking_away": False,
                    "confidence": 0.0
                }
                
                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]
                    
                    # Detect eyes within the face region
                    eyes = self.eye_cascade.detectMultiScale(
                        roi_gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(20, 20)
                    )
                    eye_data["eye_count"] = len(eyes)
                    
                    # Calculate confidence based on face and eye detection
                    if len(faces) > 0 and len(eyes) >= 2:
                        eye_data["confidence"] = min(1.0, len(eyes) / 2.0)
                    elif len(faces) > 0:
                        eye_data["confidence"] = 0.5
                    else:
                        eye_data["confidence"] = 0.0
                
                # Determine if user is looking away
                if len(faces) == 0 or eye_data["eye_count"] < 2:
                    eye_data["looking_away"] = True
                
                # Send data to client
                try:
                    await websocket.send(json.dumps(eye_data))
                except ConnectionClosed:
                    logger.info("🔌 Client disconnected during tracking")
                    break
                except Exception as e:
                    logger.error(f"❌ Error sending data: {e}")
                    break
                
                # Add small delay to prevent overwhelming the client
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"❌ Eye tracking error: {e}")
        finally:
            if cap:
                cap.release()
            logger.info("📹 Camera released")

async def main():
    """Main function to start the server"""
    tracker = EyeTracker()
    await tracker.start_server()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
