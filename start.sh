#!/bin/bash

# Render startup script for Eye Tracking WebSocket Server
echo "🚀 Starting Eye Tracking WebSocket Server on Render..."

# Set production environment variables
export HOST="0.0.0.0"
export PORT="${PORT:-10000}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export MAX_CONNECTIONS="${MAX_CONNECTIONS:-100}"

echo "📋 Configuration:"
echo "  HOST: $HOST"
echo "  PORT: $PORT"
echo "  LOG_LEVEL: $LOG_LEVEL"
echo "  MAX_CONNECTIONS: $MAX_CONNECTIONS"

# Run health check first
echo "🏥 Running health check..."
python health_check.py

if [ $? -eq 0 ]; then
    echo "✅ Health check passed, starting server..."
    python app.py
else
    echo "❌ Health check failed, but starting server anyway for Render..."
    python app.py
fi
