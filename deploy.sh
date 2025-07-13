#!/bin/bash

# Production deployment script for Eye Tracking Backend
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

echo "🚀 Deploying Eye Tracking Backend to ${ENVIRONMENT}"
echo "================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Compose file not found: $COMPOSE_FILE"
    echo "Available environments:"
    ls docker-compose.*.yml 2>/dev/null | sed 's/docker-compose\.\(.*\)\.yml/  - \1/' || echo "  - No compose files found"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your production values before deploying!"
    read -p "Press Enter to continue or Ctrl+C to abort..."
fi

# Run health check first
echo "🏥 Running health check..."
python health_check.py
if [ $? -ne 0 ]; then
    echo "❌ Health check failed. Please fix issues before deploying."
    exit 1
fi

# Build and deploy
echo "🔨 Building Docker image..."
docker-compose -f "$COMPOSE_FILE" build --no-cache

echo "📦 Starting services..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose -f "$COMPOSE_FILE" ps

# Test the deployment
echo "🧪 Testing deployment..."
sleep 5

# Run health check against the running service
echo "🏥 Running post-deployment health check..."
docker-compose -f "$COMPOSE_FILE" exec eye-tracking-backend python health_check.py
if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Your Eye Tracking Backend is now running:"
    echo "   WebSocket: ws://localhost:5000"
    echo "   Health: http://localhost:5000/health"
    echo ""
    echo "📊 To monitor logs: docker-compose -f $COMPOSE_FILE logs -f"
    echo "🛑 To stop: docker-compose -f $COMPOSE_FILE down"
else
    echo "❌ Post-deployment health check failed"
    echo "📋 Service logs:"
    docker-compose -f "$COMPOSE_FILE" logs eye-tracking-backend
    exit 1
fi
