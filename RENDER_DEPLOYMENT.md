# 🚀 Render Deployment Guide for Eye Tracking Backend

## Quick Deploy Options

### Option 1: One-Click Deploy (Recommended)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Nitish0943/backend)

### Option 2: Manual Deployment

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Files Ready**: Ensure all configuration files are in your repo

## 🔧 Deployment Steps

### Step 1: Push Your Code to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository (`Nitish0943/backend`)
4. Configure the service:

#### Basic Settings
- **Name**: `eye-tracking-backend`
- **Region**: `Oregon (US West)` or your preferred region
- **Branch**: `main`
- **Runtime**: `Python 3`

#### Build & Deploy Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

#### Advanced Settings
- **Plan**: `Free` (for testing) or `Starter` (for production)
- **Health Check Path**: `/health`

### Step 3: Environment Variables

Add these environment variables in Render dashboard:

| Key | Value | Description |
|-----|-------|-------------|
| `HOST` | `0.0.0.0` | Listen on all interfaces |
| `LOG_LEVEL` | `INFO` | Logging level |
| `MAX_CONNECTIONS` | `50` | Max WebSocket connections |

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues

## 🌐 Access Your Deployed Application

Once deployed, your application will be available at:

- **Health Check**: `https://your-app-name.onrender.com/health`
- **WebSocket Info**: `https://your-app-name.onrender.com/info`
- **WebSocket Endpoint**: `wss://your-app-name.onrender.com/ws`

## 📱 Client Connection Example

```javascript
// Connect to your deployed WebSocket server
const ws = new WebSocket('wss://your-app-name.onrender.com/ws');

ws.onopen = function(event) {
    console.log('Connected to eye tracking server');
    
    // Send ping to test connection
    ws.send(JSON.stringify({
        type: 'ping',
        timestamp: new Date().toISOString()
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    if (data.type === 'eye_data') {
        // Process eye tracking data
        console.log('Eye tracking data:', data);
    }
};

// Start eye tracking
ws.send(JSON.stringify({
    type: 'start_tracking'
}));
```

## 🎯 Testing Your Deployment

### 1. Health Check Test
```bash
curl https://your-app-name.onrender.com/health
```

Should return:
```json
{
    "status": "healthy",
    "timestamp": "2025-07-13T...",
    "service": "eye-tracking-backend",
    "version": "1.0.0"
}
```

### 2. WebSocket Test
Use a WebSocket testing tool or this simple HTML page:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Eye Tracking Test</title>
</head>
<body>
    <h1>Eye Tracking WebSocket Test</h1>
    <div id="status">Connecting...</div>
    <button onclick="startTracking()">Start Tracking</button>
    <button onclick="stopTracking()">Stop Tracking</button>
    <div id="output"></div>

    <script>
        const ws = new WebSocket('wss://your-app-name.onrender.com/ws');
        const status = document.getElementById('status');
        const output = document.getElementById('output');

        ws.onopen = () => {
            status.textContent = 'Connected ✅';
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            output.innerHTML += `<p>${JSON.stringify(data, null, 2)}</p>`;
        };

        ws.onclose = () => {
            status.textContent = 'Disconnected ❌';
        };

        function startTracking() {
            ws.send(JSON.stringify({ type: 'start_tracking' }));
        }

        function stopTracking() {
            ws.send(JSON.stringify({ type: 'stop_tracking' }));
        }
    </script>
</body>
</html>
```

## 🔧 Configuration Options

### Free Tier Limitations
- **Memory**: 512 MB RAM
- **CPU**: Shared CPU
- **Sleep**: Service sleeps after 15 minutes of inactivity
- **Build Time**: 500 build minutes/month

### Upgrading to Paid Plans
For production use, consider upgrading to:
- **Starter Plan** ($7/month): No sleep, faster builds
- **Standard Plan** ($25/month): More resources, better performance

### Custom Domain
1. Go to your service settings
2. Add your custom domain
3. Configure DNS CNAME record: `your-domain.com` → `your-app-name.onrender.com`

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Render dashboard
   - Ensure `requirements.txt` is correct
   - Verify Python version compatibility

2. **WebSocket Connection Issues**
   - Use `wss://` (secure WebSocket) for HTTPS sites
   - Check browser console for errors
   - Verify firewall/network settings

3. **Service Sleep (Free Tier)**
   - First request after sleep takes ~30 seconds
   - Consider upgrading to paid plan for production

4. **Memory Issues**
   - Monitor resource usage in dashboard
   - Optimize code for lower memory usage
   - Upgrade to higher plan if needed

### Viewing Logs
```bash
# Using Render CLI (optional)
render logs -s your-service-id
```

Or view logs in the Render dashboard under "Logs" tab.

### Health Check Debugging
If health checks fail:
1. Check `/health` endpoint manually
2. Verify the endpoint returns HTTP 200
3. Check application logs for errors

## 📈 Monitoring & Maintenance

### Metrics Available
- **Request count**
- **Response times**
- **Memory usage**
- **CPU usage**
- **Build times**

### Auto-Deploy
Render automatically deploys when you push to your connected Git branch.

### Manual Deploy
Trigger manual deploys from the Render dashboard if needed.

## 🔒 Security Best Practices

1. **Environment Variables**: Store sensitive data as environment variables
2. **HTTPS/WSS**: Always use secure connections in production
3. **Rate Limiting**: Built-in DDoS protection
4. **CORS**: Configure proper CORS headers for your frontend domain

## 💡 Next Steps

1. **Custom Domain**: Add your domain for branding
2. **Frontend Integration**: Connect your React/Vue/Angular app
3. **Monitoring**: Set up uptime monitoring
4. **Scaling**: Monitor usage and scale as needed

## 📞 Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Community Forum**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

Your Eye Tracking WebSocket server is now ready for production on Render! 🎉
