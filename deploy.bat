@echo off
REM Production deployment script for Eye Tracking Backend (Windows)
REM Usage: deploy.bat [environment]

setlocal enabledelayedexpansion

set "ENVIRONMENT=%~1"
if "%ENVIRONMENT%"=="" set "ENVIRONMENT=production"
set "COMPOSE_FILE=docker-compose.%ENVIRONMENT%.yml"

echo 🚀 Deploying Eye Tracking Backend to %ENVIRONMENT%
echo ================================================

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if compose file exists
if not exist "%COMPOSE_FILE%" (
    echo ❌ Compose file not found: %COMPOSE_FILE%
    echo Available environments:
    for %%f in (docker-compose.*.yml) do (
        set "filename=%%f"
        set "env=!filename:docker-compose.=!"
        set "env=!env:.yml=!"
        echo   - !env!
    )
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your production values before deploying!
    pause
)

REM Run health check first
echo 🏥 Running health check...
python health_check.py
if errorlevel 1 (
    echo ❌ Health check failed. Please fix issues before deploying.
    exit /b 1
)

REM Build and deploy
echo 🔨 Building Docker image...
docker-compose -f "%COMPOSE_FILE%" build --no-cache

echo 📦 Starting services...
docker-compose -f "%COMPOSE_FILE%" up -d

REM Wait for services to start
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service status...
docker-compose -f "%COMPOSE_FILE%" ps

REM Test the deployment
echo 🧪 Testing deployment...
timeout /t 5 /nobreak >nul

REM Run health check against the running service
echo 🏥 Running post-deployment health check...
docker-compose -f "%COMPOSE_FILE%" exec eye-tracking-backend python health_check.py
if errorlevel 1 (
    echo ❌ Post-deployment health check failed
    echo 📋 Service logs:
    docker-compose -f "%COMPOSE_FILE%" logs eye-tracking-backend
    exit /b 1
) else (
    echo ✅ Deployment successful!
    echo.
    echo 🌐 Your Eye Tracking Backend is now running:
    echo    WebSocket: ws://localhost:5000
    echo    Health: http://localhost:5000/health
    echo.
    echo 📊 To monitor logs: docker-compose -f %COMPOSE_FILE% logs -f
    echo 🛑 To stop: docker-compose -f %COMPOSE_FILE% down
)
