# ANTIGRAVITY Deployment Guide

Complete guide for deploying ANTIGRAVITY to production environments.

## 🚀 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  Internet Clients                        │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│           Nginx/Load Balancer (Optional)                 │
│              Port: 80, 443 (HTTPS)                       │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│         React Frontend (Static Files)                    │
│         CDN or Static Hosting Service                    │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│      FastAPI Backend (Gunicorn + Uvicorn)                │
│         Port: 8000 (or behind reverse proxy)             │
├──────────────────────────────────────────────────────────┤
│   - Model Loading                                        │
│   - Image Preprocessing                                  │
│   - Inference                                            │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│          Trained ML Model (Disk)                         │
│     /backend/models/pneumonia_model.h5                   │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 Backend Deployment

### Option 1: Traditional VPS/Cloud Server

#### Prerequisites
- Ubuntu 20.04+ / CentOS 7+
- Python 3.8+
- Supervisor or systemd
- Nginx (optional, for reverse proxy)

#### Step 1: Server Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3
.9 python3-pip python3-venv
sudo apt-get install -y nginx supervisor

# Create application user
sudo useradd -m antigravity
sudo su - antigravity
```

#### Step 2: Deploy Backend

```bash
# Clone/upload your repository
git clone https://github.com/your-repo/antigravity.git
cd antigravity/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the application
python main.py
```

#### Step 3: Configure Supervisor

Create `/etc/supervisor/conf.d/antigravity.conf`:

```ini
[program:antigravity]
process_name=%(program_name)s_%(process_num)02d
command=/home/antigravity/antigravity/backend/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:8000 \
    main:app
directory=/home/antigravity/antigravity/backend
user=antigravity
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/antigravity/backend.log
environment=PATH="/home/antigravity/antigravity/backend/venv/bin"
```

Start the service:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start antigravity
sudo supervisorctl status
```

#### Step 4: Configure Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/antigravity`:

```nginx
upstream antigravity_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.antigravity.com;

    # Redirect HTTP to HTTPS (uncomment after SSL setup)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://antigravity_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Disable request buffering for file uploads
        proxy_request_buffering off;
        client_max_body_size 100M;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/antigravity \
    /etc/nginx/sites-enabled/antigravity
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d api.antigravity.com
```

Update Nginx config to use SSL:
```nginx
listen 443 ssl http2;
ssl_certificate /etc/letsencrypt/live/api.antigravity.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/api.antigravity.com/privkey.pem;

# SSL security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

### Option 2: Docker Deployment

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Create models directory
RUN mkdir -p models

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
```

Build and run:
```bash
docker build -t antigravity-backend .
docker run -d \
  --name antigravity \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  antigravity-backend
```

Docker Compose (backend + frontend):

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/models:/app/models
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

### Option 3: Cloud Platform Deployment

#### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 20.04)
# Connect and run:

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3.9 python3-pip git supervisor nginx

# Clone repository
git clone <your-repo>
cd antigravity/backend

# Setup virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure supervisor (see above)
# Configure nginx (see above)
```

#### Heroku

1. Create `Procfile` in backend directory:
```
web: gunicorn -w 4 main:app
```

2. Create `runtime.txt`:
```
python-3.9.16
```

3. Deploy:
```bash
heroku login
heroku create antigravity-backend
git push heroku main
```

#### Google Cloud Run

```bash
# Create Dockerfile (see above)

# Deploy
gcloud run deploy antigravity \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --allow-unauthenticated \
  --set-env-vars MODEL_PATH=/models
```

---

## 📱 Frontend Deployment

### Option 1: Static Hosting

Build frontend:
```bash
cd frontend
npm install
npm run build
```

Deploy `dist/` folder to:
- **AWS S3 + CloudFront**
- **Netlify**
- **Vercel**
- **GitHub Pages**
- **Firebase Hosting**

### Option 2: AWS S3 + CloudFront

```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://antigravity-frontend/

# Create CloudFront distribution (via AWS Console)
# Point to S3 bucket
```

### Option 3: Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir dist
```

### Option 4: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

---

## 🔒 Security Checklist

- [ ] Enable HTTPS (SSL/TLS certificate)
- [ ] Set strong CORS policy
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set file upload limits
- [ ] Use environment variables for secrets
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Set up backups
- [ ] Monitor disk space

---

## 📊 Performance Optimization

### Backend Optimization

1. **Enable Caching**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
```

2. **Database Connection Pooling**
- Already handled by SQLAlchemy (if using database)

3. **Model Quantization**
- Reduce model size for faster inference

4. **GPU Support**
- Install CUDA for TensorFlow/PyTorch
- Use GPU in model inference

### Frontend Optimization

1. **Enable Compression**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **CDN for Static Assets**
- CloudFront, CloudFlare, etc.

3. **Lazy Loading**
- Already implemented in React components

4. **Minification**
- Automatic with `npm run build`

---

## 📈 Monitoring & Logging

### Backend Monitoring

```python
# Add to main.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.FileHandler('/var/log/antigravity/app.log')
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

### Monitoring Tools

- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **ELK Stack** - Log analysis
- **New Relic** - APM
- **Sentry** - Error tracking

### Health Checks

```yaml
# Docker health check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

`.github/workflows/deploy.yml`:

```yaml
name: Deploy ANTIGRAVITY

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          ssh ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }}
          cd antigravity/backend
          git pull origin main
          pip install -r requirements.txt
          supervisorctl restart antigravity
      
      - name: Deploy Frontend
        run: |
          npm install
          npm run build
          aws s3 sync dist/ s3://antigravity-frontend/
```

---

## 📋 Deployment Checklist

### Before Deployment

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Model file in production location
- [ ] SSL certificate installed
- [ ] Database migrations completed
- [ ] Monitoring configured
- [ ] Backups scheduled

### After Deployment

- [ ] Health check endpoint responding
- [ ] API endpoints accessible
- [ ] Frontend loading correctly
- [ ] Predictions working
- [ ] Logs monitored
- [ ] Performance baseline recorded

---

## 🚨 Troubleshooting

### Backend Not Starting

```bash
# Check logs
supervisorctl tail antigravity -f

# Verify Python environment
source /home/antigravity/antigravity/backend/venv/bin/activate
python main.py
```

### High Memory Usage

```bash
# Check process memory
ps aux | grep gunicorn

# Reduce worker count in supervisor config
-w 2  # Instead of 4
```

### Slow Predictions

- Verify GPU is enabled
- Check model optimization
- Monitor CPU usage
- Reduce batch size threshold

---

## 📞 Support

For deployment issues:
1. Check logs (above)
2. Verify configuration
3. Test locally first
4. Check documentation
5. Contact support

---

**Deployment Version**: 1.0.0
**Last Updated**: 2024
