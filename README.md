# Eye Tracking Backend

This is the Python backend for the Intervue AI platform that provides real-time eye tracking via WebSocket connections.

## Features

- Real-time eye tracking using OpenCV
- WebSocket server for live communication
- Face and eye detection using Haar cascades
- Cloud-ready deployment with Docker
- Headless OpenCV support for server environments

## Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Camera access (for local development)

## Local Development

### Option 1: Direct Python

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the health check:
```bash
python health_check.py
```

4. Start the server:
```bash
python eye_gaze.py
```

### Option 2: Docker

#### Automatic Build (Recommended)
Use the build script that tries different configurations:

**Linux/macOS:**
```bash
./build.sh
```

**Windows (PowerShell):**
```powershell
bash build.sh
```

#### Manual Build Options

1. **Simple Build (Recommended for most cases):**
```bash
docker build -f Dockerfile.simple -t eye-tracking-backend .
docker run -p 5000:5000 eye-tracking-backend
```

2. **Minimal Build (if simple fails):**
```bash
docker build -f Dockerfile.minimal -t eye-tracking-backend .
docker run -p 5000:5000 eye-tracking-backend
```

3. **Full Build (if others fail):**
```bash
docker build -f Dockerfile -t eye-tracking-backend .
docker run -p 5000:5000 eye-tracking-backend
```

4. **Docker Compose:**
```bash
docker-compose up --build
```

## Cloud Deployment

### Railway

1. Connect your repository to Railway
2. Set the following environment variables:
   - `HOST`: `0.0.0.0`
   - `PORT`: `5000`
3. Deploy the backend directory

### Render

1. Create a new Web Service on Render
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python eye_gaze.py`
5. Set environment variables:
   - `HOST`: `0.0.0.0`
   - `PORT`: `10000` (Render's default port)

### Heroku

1. Create a `Procfile`:
```
web: python eye_gaze.py
```

2. Deploy using Heroku CLI or GitHub integration

## Environment Variables

- `HOST`: Server host (default: `localhost`)
- `PORT`: Server port (default: `5000`)

## WebSocket API

### Connection
- URL: `ws://your-backend-url:port`
- Protocol: WebSocket

### Messages

#### From Client to Server

**Start Tracking**
```json
{
  "type": "start_tracking"
}
```

**Stop Tracking**
```json
{
  "type": "stop_tracking"
}
```

**Ping**
```json
{
  "type": "ping"
}
```

#### From Server to Client

**Connection Confirmation**
```json
{
  "type": "connection",
  "message": "Eye tracking connected",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Eye Tracking Data**
```json
{
  "type": "eye_data",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "face_detected": true,
  "eye_count": 2,
  "looking_away": false,
  "confidence": 1.0
}
```

**Error**
```json
{
  "type": "error",
  "message": "Error description",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Pong Response**
```json
{
  "type": "pong",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Troubleshooting

### OpenCV Import Error

If you see `libGL.so.1: cannot open shared object file`, this means you're using the full OpenCV package instead of the headless version. The `requirements.txt` should use `opencv-python-headless`.

### Camera Not Found

The backend tries multiple camera indices (0, 1, 2). If no camera is found, it will send an error message to the client.

### Cascade Files Not Found

The Haar cascade files are included with OpenCV. If they're not found, check that OpenCV is properly installed.

### WebSocket Connection Issues

1. Check that the backend is running on the correct host and port
2. Ensure your frontend is connecting to the correct WebSocket URL
3. Check for firewall or network restrictions

### Docker Build Issues

If you encounter package installation errors during Docker build:

1. **Try the simple Dockerfile first:**
   ```bash
   docker build -f Dockerfile.simple -t eye-tracking-backend .
   ```

2. **Clean Docker cache:**
   ```bash
   docker system prune -a
   ```

3. **Check Docker version:**
   ```bash
   docker --version
   ```

4. **Use the build script:**
   ```bash
   # Linux/macOS
   ./build.sh
   
   # Windows
   bash build.sh
   ```

5. **Alternative: Use Docker Compose with simple Dockerfile:**
   ```bash
   docker-compose up --build
   ```

## Health Check

Run the health check script to verify everything is working:

```bash
python health_check.py
```

This will check:
- All Python dependencies
- OpenCV installation and cascade files
- Environment variables
- Cascade classifier loading

## Development Notes

- The backend uses `opencv-python-headless` for cloud compatibility
- Camera access is required for eye tracking functionality
- WebSocket connections are maintained with ping/pong heartbeats
- Error handling is implemented throughout the application 