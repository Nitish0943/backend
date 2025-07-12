#!/bin/bash

# Build script for the eye tracking backend
# This script tries different Dockerfile options to find the best working configuration

echo "🔨 Building Eye Tracking Backend..."
echo "=================================="

# Function to try building with a specific Dockerfile
try_build() {
    local dockerfile=$1
    local tag=$2
    
    echo "📦 Trying build with $dockerfile..."
    
    if docker build -f $dockerfile -t eye-tracking-backend:$tag .; then
        echo "✅ Build successful with $dockerfile!"
        echo "🚀 You can now run: docker run -p 5000:5000 eye-tracking-backend:$tag"
        return 0
    else
        echo "❌ Build failed with $dockerfile"
        return 1
    fi
}

# Try different Dockerfile options in order of preference
echo "🔄 Attempting builds with different configurations..."

# Option 1: Simple (full Python image)
if try_build "Dockerfile.simple" "simple"; then
    echo "🎉 Using simple configuration (recommended for most cases)"
    exit 0
fi

# Option 2: Minimal (slim image with minimal deps)
if try_build "Dockerfile.minimal" "minimal"; then
    echo "🎉 Using minimal configuration"
    exit 0
fi

# Option 3: Full (slim image with all deps)
if try_build "Dockerfile" "full"; then
    echo "🎉 Using full configuration"
    exit 0
fi

echo "❌ All build attempts failed!"
echo "💡 Troubleshooting tips:"
echo "   1. Check your Docker installation"
echo "   2. Ensure you have enough disk space"
echo "   3. Try running 'docker system prune' to clean up"
echo "   4. Check your internet connection for package downloads"
exit 1 