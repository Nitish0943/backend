# Eye Tracking Backend - Production Deployment Guide

## 🚀 Quick Start

Your eye tracking WebSocket server is now production-ready! Here's how to deploy it:

### 1. Local Production Testing

```bash
# Windows
deploy.bat production

# Linux/Mac
chmod +x deploy.sh
./deploy.sh production
```

### 2. Cloud Deployment Options

#### Option A: Docker-based Cloud (Recommended)
- **DigitalOcean App Platform**
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**

#### Option B: VPS Deployment
- **DigitalOcean Droplet**
- **AWS EC2**
- **Linode**
- **Vultr**

#### Option C: Heroku (Platform-as-a-Service)
- Already configured with `Procfile`
- Just push to Heroku Git

## 🔧 Environment Configuration

### Required Environment Variables

```bash
# Server Configuration
HOST=0.0.0.0              # Allow external connections
PORT=5000                 # Your preferred port
LOG_LEVEL=INFO            # INFO, WARNING, ERROR

# Performance Settings
MAX_CONNECTIONS=100       # Maximum concurrent WebSocket connections
PING_INTERVAL=20          # WebSocket ping interval (seconds)
PING_TIMEOUT=20           # WebSocket ping timeout (seconds)
```

### Production .env File

1. Copy the example: `cp .env.example .env`
2. Edit values for your production environment
3. **Never commit .env files to version control**

## 🌐 Cloud Platform Specific Instructions

### DigitalOcean App Platform

1. Create new App from GitHub repository
2. Set environment variables in the console
3. App will auto-deploy on code changes

```yaml
# app.yaml (DigitalOcean App Platform)
name: eye-tracking-backend
services:
- name: web
  source_dir: /
  github:
    repo: your-username/intervue-ai-backend
    branch: master
  run_command: python eye_gaze.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: HOST
    value: "0.0.0.0"
  - key: PORT
    value: "5000"
  health_check:
    http_path: /health
```

### AWS ECS/Fargate

1. Build and push Docker image to ECR
2. Create ECS task definition
3. Deploy with Fargate

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -f Dockerfile.production -t eye-tracking-backend .
docker tag eye-tracking-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/eye-tracking-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/eye-tracking-backend:latest
```

### Google Cloud Run

```bash
# Deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT-ID/eye-tracking-backend
gcloud run deploy eye-tracking-backend \
  --image gcr.io/PROJECT-ID/eye-tracking-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars HOST=0.0.0.0,PORT=8080
```

### Heroku

```bash
# Deploy to Heroku (uses existing Procfile)
heroku create your-app-name
heroku config:set HOST=0.0.0.0 PORT=80
git push heroku master
```

## 🔒 Security Considerations

### 1. SSL/TLS Configuration

For production, use HTTPS/WSS:

```javascript
// Client connection for production
const ws = new WebSocket('wss://your-domain.com');
```

### 2. CORS Configuration

Configure CORS in your reverse proxy (nginx.conf included):

```nginx
add_header Access-Control-Allow-Origin "https://your-frontend-domain.com";
```

### 3. Rate Limiting

The nginx configuration includes rate limiting:
- 10 requests per second per IP
- Burst of 20 requests allowed

### 4. Firewall Rules

Only expose necessary ports:
- Port 80 (HTTP) - for redirects
- Port 443 (HTTPS) - for WebSocket connections

## 📊 Monitoring & Health Checks

### Health Check Endpoint

The server includes comprehensive health checks:

```bash
# Test locally
python health_check.py

# Test deployed service
curl http://your-domain.com/health
```

### Monitoring

Set up monitoring for:
- WebSocket connection count
- Memory usage
- CPU usage
- Error rates

### Logging

Logs include:
- Connection events
- Error tracking
- Performance metrics

Access logs:
```bash
# Docker logs
docker-compose -f docker-compose.production.yml logs -f

# Application logs
tail -f /var/log/eye-tracking.log
```

## 🚨 Troubleshooting

### Common Issues

1. **Camera Access**: Production servers typically don't have cameras
   - Eye tracking will work with uploaded images/video streams
   - For real camera access, deploy on edge devices

2. **WebSocket Connection Issues**:
   ```bash
   # Test WebSocket connectivity
   wscat -c ws://your-domain.com
   ```

3. **Memory Issues**:
   - Monitor memory usage with `docker stats`
   - Adjust `MAX_CONNECTIONS` if needed

4. **Permission Errors**:
   - Ensure Docker has proper permissions
   - Check if running as non-root user

### Performance Optimization

1. **Resource Limits**: Set appropriate CPU/memory limits
2. **Connection Pooling**: Use `MAX_CONNECTIONS` to limit concurrent users
3. **Load Balancing**: For high traffic, deploy multiple instances behind a load balancer

## 📈 Scaling

### Horizontal Scaling

For high-traffic applications:

1. Deploy multiple instances
2. Use a load balancer (nginx, HAProxy, or cloud LB)
3. Consider Redis for session management

### Vertical Scaling

Increase resources:
- More CPU cores for concurrent processing
- More RAM for handling multiple connections

## 🔧 Maintenance

### Updates

1. Test changes locally first
2. Use blue-green deployment for zero downtime
3. Monitor health checks after deployment

### Backup

Backup configuration files:
- `.env` (without sensitive data)
- `nginx.conf`
- Docker configurations

## 📞 Support

For production issues:
1. Check logs first
2. Run health checks
3. Monitor resource usage
4. Test WebSocket connectivity

Your eye tracking backend is now production-ready! 🎉
