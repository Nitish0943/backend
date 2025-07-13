# 📋 Render Deployment Checklist

## ✅ Pre-Deployment Checklist

### Files Ready
- [ ] `app.py` - Main application server
- [ ] `requirements.txt` - All dependencies listed
- [ ] `render.yaml` - Render configuration (optional)
- [ ] `Procfile` - Process definition
- [ ] `health_check.py` - Health verification
- [ ] `test_server.py` - Testing script
- [ ] `RENDER_DEPLOYMENT.md` - Deployment guide

### Repository Setup
- [ ] Code pushed to GitHub repository
- [ ] Repository is public or accessible to Render
- [ ] All files committed and pushed

### Configuration Verified
- [ ] `HOST=0.0.0.0` (accept external connections)
- [ ] `PORT` will be set by Render automatically
- [ ] Health check endpoint at `/health`
- [ ] WebSocket endpoint at `/ws`

## 🚀 Deployment Steps

### 1. Test Locally (Optional but Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Test in another terminal
python test_server.py http://localhost:10000
```

### 2. Deploy to Render

#### Option A: Using Render Dashboard
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository: `Nitish0943/backend`
4. Configure:
   - **Name**: `eye-tracking-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Health Check Path**: `/health`

#### Option B: Using render.yaml (Blueprint)
1. Push `render.yaml` to your repository
2. Go to Render → "New +" → "Blueprint"
3. Connect your repository
4. Render will use the configuration in `render.yaml`

### 3. Environment Variables (Set in Render Dashboard)
```
HOST=0.0.0.0
LOG_LEVEL=INFO
MAX_CONNECTIONS=50
```

### 4. Wait for Deployment
- Monitor build logs for any errors
- First deployment takes 2-5 minutes
- Service will be available at: `https://your-app-name.onrender.com`

## 🧪 Post-Deployment Testing

### 1. Health Check
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
    "status": "healthy",
    "timestamp": "...",
    "service": "eye-tracking-backend",
    "version": "1.0.0"
}
```

### 2. WebSocket Test
```bash
python test_server.py https://your-app-name.onrender.com
```

### 3. Manual WebSocket Test
Use browser console or WebSocket testing tool:
```javascript
const ws = new WebSocket('wss://your-app-name.onrender.com/ws');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', JSON.parse(e.data));
ws.send(JSON.stringify({type: 'ping'}));
```

## 🔧 Configuration Options

### Free Tier (Recommended for Testing)
- ✅ No cost
- ✅ 512MB RAM
- ✅ Shared CPU
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ 500 build minutes/month

### Starter Tier ($7/month) - Recommended for Production
- ✅ No sleep
- ✅ 512MB RAM
- ✅ Faster builds
- ✅ Custom domains
- ✅ Better support

### Standard Tier ($25/month) - High Traffic
- ✅ 2GB RAM
- ✅ Dedicated CPU
- ✅ Faster performance
- ✅ Priority support

## 🌐 URL Structure

Once deployed, your service will be available at:

| Endpoint | URL | Purpose |
|----------|-----|---------|
| Health Check | `https://your-app.onrender.com/health` | Service health |
| Info | `https://your-app.onrender.com/info` | WebSocket info |
| WebSocket | `wss://your-app.onrender.com/ws` | WebSocket connection |

## 🔍 Monitoring & Debugging

### View Logs
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Monitor real-time logs

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` syntax
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **Service Won't Start**
   - Verify `python app.py` works locally
   - Check environment variables
   - Review startup logs

3. **Health Check Fails**
   - Ensure `/health` endpoint returns HTTP 200
   - Check if server is binding to correct port
   - Verify HOST=0.0.0.0

4. **WebSocket Connection Issues**
   - Use `wss://` (secure) for HTTPS sites
   - Check browser console for errors
   - Verify WebSocket endpoint path `/ws`

### Performance Monitoring
- Monitor response times in Render dashboard
- Check memory usage
- Monitor connection counts

## 🔄 Continuous Deployment

Render automatically deploys when you push to your connected Git branch:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main
# Render automatically rebuilds and deploys
```

## 🔒 Security Considerations

### Free Tier
- ✅ HTTPS/WSS automatically enabled
- ✅ DDoS protection included
- ✅ No sensitive data in logs

### Production Recommendations
- Use environment variables for secrets
- Enable custom domain with your SSL certificate
- Monitor access logs
- Implement rate limiting in your application

## 📞 Support Resources

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Status**: [status.render.com](https://status.render.com)
- **Support**: Email support@render.com

## ✅ Final Verification

Your deployment is successful when:
- [ ] Health check returns `{"status": "healthy"}`
- [ ] WebSocket connection establishes successfully
- [ ] Can send/receive WebSocket messages
- [ ] No errors in deployment logs
- [ ] Service stays running (doesn't crash)

## 🎉 You're Done!

Your Eye Tracking WebSocket server is now live on Render!

**Next Steps:**
1. Share your WebSocket URL: `wss://your-app-name.onrender.com/ws`
2. Integrate with your frontend application
3. Monitor usage and performance
4. Scale up when needed

**Sample Integration:**
```javascript
// Frontend JavaScript
const ws = new WebSocket('wss://your-app-name.onrender.com/ws');

ws.onopen = () => {
    console.log('🎉 Connected to Eye Tracking Server');
    // Start tracking
    ws.send(JSON.stringify({type: 'start_tracking'}));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'eye_data') {
        // Process eye tracking data
        console.log('👁️ Eye data:', data);
    }
};
```

Congratulations! Your eye tracking backend is now production-ready! 🚀
