From e1dfe4936fbb2591a85bf737955c467b21e05db4 Mon Sep 17 00:00:00 2001
From: ARYAN RAJ <191250587+ARYAN10227@users.noreply.github.com>
Date: Tue, 20 Oct 2026 14:17:39 +0000
Subject: [PATCH] Rewrite README and rebrand project as PulmoNet

- New README covering architecture, model, setup, API and team
- Remove outdated scaffold docs
- Replace old project names with PulmoNet across frontend and backend
- Point footer links to the GitHub repo
---
 API_DOCS.md                          | 466 ----------------------
 DEPLOYMENT.md                        | 568 ---------------------------
 MODEL_INTEGRATION.md                 | 468 ----------------------
 PROJECT_SUMMARY.md                   | 498 -----------------------
 QUICK_REFERENCE.md                   | 262 ------------
 README.md                            | 386 ++++++++----------
 SETUP.md                             | 391 ------------------
 backend/PYTORCH_MODEL_INTEGRATION.md | 144 -------
 backend/XRAY_MODEL_INTEGRATION.md    | 235 -----------
 backend/main.py                      |  10 +-
 backend/requirements.txt             |   2 +-
 backend/routes/predict.py            |   2 +-
 backend/services/model_loader.py     |   4 +-
 backend/test_model.py                |   2 +-
 backend/utils/preprocess.py          |   2 +-
 frontend/README.md                   | 433 --------------------
 frontend/index.html                  |   4 +-
 frontend/package.json                |   4 +-
 frontend/src/App.jsx                 |   2 +-
 frontend/src/components/Footer.jsx   |  10 +-
 frontend/src/components/Hero.jsx     |   2 +-
 frontend/src/components/Navbar.jsx   |   2 +-
 frontend/src/index.css               |   2 +-
 23 files changed, 195 insertions(+), 3704 deletions(-)
 delete mode 100644 API_DOCS.md
 delete mode 100644 DEPLOYMENT.md
 delete mode 100644 MODEL_INTEGRATION.md
 delete mode 100644 PROJECT_SUMMARY.md
 delete mode 100644 QUICK_REFERENCE.md
 delete mode 100644 SETUP.md
 delete mode 100644 backend/PYTORCH_MODEL_INTEGRATION.md
 delete mode 100644 backend/XRAY_MODEL_INTEGRATION.md
 delete mode 100644 frontend/README.md

diff --git a/API_DOCS.md b/API_DOCS.md
deleted file mode 100644
index e7b7a2e..0000000
--- a/API_DOCS.md
+++ /dev/null
@@ -1,466 +0,0 @@
-# ANTIGRAVITY API Documentation
-
-Complete API reference for the ANTIGRAVITY pneumonia detection system.
-
-## 📖 Overview
-
-The ANTIGRAVITY API is a RESTful service for pneumonia detection from chest X-ray images.
-
-**Base URL**: `http://localhost:8000`
-
-## 🔗 Endpoints
-
-### 1. Health Check
-
-Check if the server is running.
-
-```
-GET /health
-```
-
-**Response:**
-```json
-{
-  "status": "running",
-  "service": "ANTIGRAVITY API"
-}
-```
-
-**Status Code**: `200 OK`
-
----
-
-### 2. Root Information
-
-Get basic API information.
-
-```
-GET /
-```
-
-**Response:**
-```json
-{
-  "name": "ANTIGRAVITY",
-  "tagline": "AI-powered chest X-ray screening for pneumonia detection",
-  "version": "1.0.0",
-  "endpoints": {
-    "health": "/health",
-    "predict": "/api/predict",
-    "docs": "/docs"
-  }
-}
-```
-
-**Status Code**: `200 OK`
-
----
-
-### 3. Predict Pneumonia
-
-Submit chest X-ray images for pneumonia prediction.
-
-```
-POST /api/predict
-```
-
-**Headers:**
-```
-Content-Type: multipart/form-data
-```
-
-**Request Body:**
-```
-files: [file1, file2, ...]  (List of image files)
-```
-
-**Supported Formats**: JPG, JPEG, PNG
-
-**Constraints:**
-- Maximum 10 files per request
-- Maximum 10 MB per file
-- Recommended: Clear chest X-ray images
-
-**Example Request (curl):**
-
-```bash
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@xray1.png" \
-  -F "files=@xray2.png"
-```
-
-**Example Response:**
-
-```json
-[
-  {
-    "filename": "xray1.png",
-    "prediction": "Pneumonia",
-    "confidence": 96.4,
-    "probability_normal": 0.036,
-    "probability_pneumonia": 0.964,
-    "status": "success"
-  },
-  {
-    "filename": "xray2.png",
-    "prediction": "Normal",
-    "confidence": 91.2,
-    "probability_normal": 0.912,
-    "probability_pneumonia": 0.088,
-    "status": "success"
-  }
-]
-```
-
-**Status Code**: `200 OK`
-
-**Error Response (400):**
-
-```json
-{
-  "detail": "Invalid file type: document.pdf. Allowed: JPG, JPEG, PNG"
-}
-```
-
-**Error Response (413):**
-
-```json
-{
-  "detail": "File too large: image.png. Maximum size: 10 MB"
-}
-```
-
-**Error Response (422):**
-
-```json
-{
-  "detail": "Too many files. Maximum 10 files allowed."
-}
-```
-
-**Error Response (500):**
-
-```json
-{
-  "error": "Internal server error",
-  "details": "Error message here"
-}
-```
-
----
-
-### 4. Prediction Configuration
-
-Get prediction system configuration and constraints.
-
-```
-GET /api/predict/config
-```
-
-**Response:**
-
-```json
-{
-  "max_files": 10,
-  "allowed_formats": ["jpg", "jpeg", "png"],
-  "max_file_size_mb": 10,
-  "predictions": {
-    "classes": ["Normal", "Pneumonia"],
-    "output_format": "confidence percentage (0-100)"
-  },
-  "preprocessing": {
-    "image_width": 224,
-    "image_height": 224,
-    "channels": 1,
-    "note": "Configure preprocessing parameters in utils/preprocess.py"
-  }
-}
-```
-
-**Status Code**: `200 OK`
-
----
-
-## 📊 Response Format
-
-### Prediction Object
-
-Each prediction in the response contains:
-
-| Field | Type | Description |
-|-------|------|-------------|
-| `filename` | string | Original uploaded filename |
-| `prediction` | string | Prediction result: "Normal" or "Pneumonia" |
-| `confidence` | number | Confidence percentage (0-100) |
-| `probability_normal` | number | Probability of normal (0-1) |
-| `probability_pneumonia` | number | Probability of pneumonia (0-1) |
-| `status` | string | Status: "success" or "error" |
-
-### Example Prediction
-
-```json
-{
-  "filename": "chest_xray_001.png",
-  "prediction": "Pneumonia",
-  "confidence": 96.4,
-  "probability_normal": 0.036,
-  "probability_pneumonia": 0.964,
-  "status": "success"
-}
-```
-
----
-
-## ⚠️ Error Handling
-
-### Error Status Codes
-
-| Status | Meaning |
-|--------|---------|
-| 200 | Success |
-| 400 | Bad Request (invalid input) |
-| 413 | Payload Too Large |
-| 422 | Validation Error |
-| 500 | Internal Server Error |
-
-### Common Errors
-
-#### No Files Provided
-```json
-{
-  "detail": "No files provided"
-}
-```
-
-#### Invalid File Type
-```json
-{
-  "detail": "Invalid file type: document.pdf. Allowed: JPG, JPEG, PNG"
-}
-```
-
-#### File Too Large
-```json
-{
-  "detail": "File too large: image.png. Maximum size: 10 MB"
-}
-```
-
-#### Too Many Files
-```json
-{
-  "detail": "Too many files. Maximum 10 files allowed."
-}
-```
-
-#### Image Preprocessing Failed
-```json
-{
-  "detail": "Image preprocessing failed: Invalid image format"
-}
-```
-
-#### Model Inference Failed
-```json
-{
-  "detail": "Prediction failed: Model not loaded"
-}
-```
-
----
-
-## 🔐 Security
-
-### Rate Limiting
-Currently not implemented. Recommended for production.
-
-### CORS
-All origins allowed. Configuration in `main.py`:
-```python
-allow_origins=["*"],  # Restrict in production
-```
-
-### File Validation
-- File type checking
-- File size validation
-- File count validation
-- Filename sanitization
-
----
-
-## 📱 Integration Examples
-
-### Python (requests)
-
-```python
-import requests
-
-files = [('files', open('xray1.png', 'rb')), 
-         ('files', open('xray2.png', 'rb'))]
-
-response = requests.post('http://localhost:8000/api/predict', files=files)
-predictions = response.json()
-
-for pred in predictions:
-    print(f"{pred['filename']}: {pred['prediction']} ({pred['confidence']}%)")
-```
-
-### JavaScript (fetch)
-
-```javascript
-const formData = new FormData();
-formData.append('files', file1);
-formData.append('files', file2);
-
-const response = await fetch('http://localhost:8000/api/predict', {
-  method: 'POST',
-  body: formData
-});
-
-const predictions = await response.json();
-predictions.forEach(pred => {
-  console.log(`${pred.filename}: ${pred.prediction} (${pred.confidence}%)`);
-});
-```
-
-### cURL
-
-```bash
-# Single file
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@xray1.png"
-
-# Multiple files
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@xray1.png" \
-  -F "files=@xray2.png" \
-  -F "files=@xray3.png"
-```
-
-### React/TypeScript
-
-```typescript
-const submitPrediction = async (files: File[]) => {
-  const formData = new FormData();
-  files.forEach(file => formData.append('files', file));
-
-  const response = await fetch('http://localhost:8000/api/predict', {
-    method: 'POST',
-    body: formData,
-  });
-
-  if (!response.ok) {
-    throw new Error('Prediction failed');
-  }
-
-  return response.json();
-};
-```
-
----
-
-## 🧪 Testing
-
-### Test with Swagger UI
-Visit: `http://localhost:8000/docs`
-
-### Test with ReDoc
-Visit: `http://localhost:8000/redoc`
-
-### Command Line Test
-
-```bash
-# Test health
-curl http://localhost:8000/health
-
-# Test with sample image
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@sample_xray.png" | python -m json.tool
-```
-
----
-
-## 📊 Performance
-
-### Typical Response Times
-- Single image: 1-3 seconds
-- 5 images: 2-5 seconds
-- 10 images: 3-8 seconds
-
-(Varies based on your model and hardware)
-
-### Optimization Tips
-1. Process maximum images in batch (10)
-2. Avoid sending 1-2 images repeatedly
-3. Use appropriate image quality
-4. Ensure sufficient server resources
-
----
-
-## 🔄 Versioning
-
-**Current Version**: 1.0.0
-
-Future versions may include:
-- Rate limiting
-- Authentication
-- Async processing
-- Results caching
-- Confidence thresholds
-- Region of interest analysis
-
----
-
-## ⚠️ Medical Disclaimer
-
-**IMPORTANT**: This API returns AI predictions that must be:
-- Used only as a screening aid
-- Reviewed by qualified healthcare professionals
-- Never used as sole diagnostic tool
-- Documented in patient records
-
-Results are not a substitute for professional medical diagnosis.
-
----
-
-## 📞 Support
-
-For API issues or questions:
-1. Check error message details
-2. Review this documentation
-3. Check server logs
-4. Verify model is properly loaded
-
----
-
-## 🚀 Advanced Usage
-
-### Batch Processing Script
-
-```python
-import requests
-import os
-from pathlib import Path
-
-def predict_directory(image_dir, output_file='results.json'):
-    """Predict all images in a directory"""
-    images = list(Path(image_dir).glob('*.png')) + \
-             list(Path(image_dir).glob('*.jpg'))
-    
-    for i in range(0, len(images), 10):
-        batch = images[i:i+10]
-        files = [('files', open(img, 'rb')) for img in batch]
-        
-        response = requests.post('http://localhost:8000/api/predict', 
-                                files=files)
-        predictions = response.json()
-        
-        # Process predictions...
-        for pred in predictions:
-            print(f"{pred['filename']}: {pred['prediction']}")
-```
-
----
-
-**Last Updated**: 2024
-**API Version**: 1.0.0
diff --git a/DEPLOYMENT.md b/DEPLOYMENT.md
deleted file mode 100644
index 996dd5b..0000000
--- a/DEPLOYMENT.md
+++ /dev/null
@@ -1,568 +0,0 @@
-# ANTIGRAVITY Deployment Guide
-
-Complete guide for deploying ANTIGRAVITY to production environments.
-
-## 🚀 Architecture Overview
-
-```
-┌─────────────────────────────────────────────────────────┐
-│                  Internet Clients                        │
-└──────────────────────────────────────────────────────────┘
-                          ↓
-┌──────────────────────────────────────────────────────────┐
-│           Nginx/Load Balancer (Optional)                 │
-│              Port: 80, 443 (HTTPS)                       │
-└──────────────────────────────────────────────────────────┘
-                          ↓
-┌──────────────────────────────────────────────────────────┐
-│         React Frontend (Static Files)                    │
-│         CDN or Static Hosting Service                    │
-└──────────────────────────────────────────────────────────┘
-                          ↓
-┌──────────────────────────────────────────────────────────┐
-│      FastAPI Backend (Gunicorn + Uvicorn)                │
-│         Port: 8000 (or behind reverse proxy)             │
-├──────────────────────────────────────────────────────────┤
-│   - Model Loading                                        │
-│   - Image Preprocessing                                  │
-│   - Inference                                            │
-└──────────────────────────────────────────────────────────┘
-                          ↓
-┌──────────────────────────────────────────────────────────┐
-│          Trained ML Model (Disk)                         │
-│     /backend/models/pneumonia_model.h5                   │
-└──────────────────────────────────────────────────────────┘
-```
-
----
-
-## 🔧 Backend Deployment
-
-### Option 1: Traditional VPS/Cloud Server
-
-#### Prerequisites
-- Ubuntu 20.04+ / CentOS 7+
-- Python 3.8+
-- Supervisor or systemd
-- Nginx (optional, for reverse proxy)
-
-#### Step 1: Server Setup
-
-```bash
-# Update system
-sudo apt-get update
-sudo apt-get upgrade -y
-
-# Install Python and dependencies
-sudo apt-get install -y python3
-.9 python3-pip python3-venv
-sudo apt-get install -y nginx supervisor
-
-# Create application user
-sudo useradd -m antigravity
-sudo su - antigravity
-```
-
-#### Step 2: Deploy Backend
-
-```bash
-# Clone/upload your repository
-git clone https://github.com/your-repo/antigravity.git
-cd antigravity/backend
-
-# Create virtual environment
-python3 -m venv venv
-source venv/bin/activate
-
-# Install dependencies
-pip install -r requirements.txt
-
-# Test the application
-python main.py
-```
-
-#### Step 3: Configure Supervisor
-
-Create `/etc/supervisor/conf.d/antigravity.conf`:
-
-```ini
-[program:antigravity]
-process_name=%(program_name)s_%(process_num)02d
-command=/home/antigravity/antigravity/backend/venv/bin/gunicorn \
-    -w 4 \
-    -b 127.0.0.1:8000 \
-    main:app
-directory=/home/antigravity/antigravity/backend
-user=antigravity
-autostart=true
-autorestart=true
-redirect_stderr=true
-stdout_logfile=/var/log/antigravity/backend.log
-environment=PATH="/home/antigravity/antigravity/backend/venv/bin"
-```
-
-Start the service:
-```bash
-sudo supervisorctl reread
-sudo supervisorctl update
-sudo supervisorctl start antigravity
-sudo supervisorctl status
-```
-
-#### Step 4: Configure Nginx (Reverse Proxy)
-
-Create `/etc/nginx/sites-available/antigravity`:
-
-```nginx
-upstream antigravity_backend {
-    server 127.0.0.1:8000;
-}
-
-server {
-    listen 80;
-    server_name api.antigravity.com;
-
-    # Redirect HTTP to HTTPS (uncomment after SSL setup)
-    # return 301 https://$server_name$request_uri;
-
-    location / {
-        proxy_pass http://antigravity_backend;
-        proxy_set_header Host $host;
-        proxy_set_header X-Real-IP $remote_addr;
-        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
-        proxy_set_header X-Forwarded-Proto $scheme;
-        
-        # Disable request buffering for file uploads
-        proxy_request_buffering off;
-        client_max_body_size 100M;
-    }
-}
-```
-
-Enable the site:
-```bash
-sudo ln -s /etc/nginx/sites-available/antigravity \
-    /etc/nginx/sites-enabled/antigravity
-sudo nginx -t
-sudo systemctl restart nginx
-```
-
-#### Step 5: SSL Certificate (Let's Encrypt)
-
-```bash
-sudo apt-get install -y certbot python3-certbot-nginx
-sudo certbot certonly --nginx -d api.antigravity.com
-```
-
-Update Nginx config to use SSL:
-```nginx
-listen 443 ssl http2;
-ssl_certificate /etc/letsencrypt/live/api.antigravity.com/fullchain.pem;
-ssl_certificate_key /etc/letsencrypt/live/api.antigravity.com/privkey.pem;
-
-# SSL security headers
-add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
-```
-
----
-
-### Option 2: Docker Deployment
-
-Create `backend/Dockerfile`:
-
-```dockerfile
-FROM python:3.9-slim
-
-WORKDIR /app
-
-# Install system dependencies
-RUN apt-get update && apt-get install -y \
-    build-essential \
-    && rm -rf /var/lib/apt/lists/*
-
-# Copy requirements
-COPY requirements.txt .
-RUN pip install --no-cache-dir -r requirements.txt
-RUN pip install gunicorn
-
-# Copy application
-COPY . .
-
-# Create models directory
-RUN mkdir -p models
-
-# Expose port
-EXPOSE 8000
-
-# Run gunicorn
-CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
-```
-
-Build and run:
-```bash
-docker build -t antigravity-backend .
-docker run -d \
-  --name antigravity \
-  -p 8000:8000 \
-  -v $(pwd)/models:/app/models \
-  antigravity-backend
-```
-
-Docker Compose (backend + frontend):
-
-`docker-compose.yml`:
-```yaml
-version: '3.8'
-
-services:
-  backend:
-    build: ./backend
-    ports:
-      - "8000:8000"
-    volumes:
-      - ./backend/models:/app/models
-    environment:
-      - PYTHONUNBUFFERED=1
-    restart: unless-stopped
-
-  frontend:
-    build: ./frontend
-    ports:
-      - "3000:3000"
-    environment:
-      - REACT_APP_API_URL=http://localhost:8000/api
-    depends_on:
-      - backend
-    restart: unless-stopped
-
-  nginx:
-    image: nginx:alpine
-    ports:
-      - "80:80"
-      - "443:443"
-    volumes:
-      - ./nginx.conf:/etc/nginx/nginx.conf
-      - ./ssl:/etc/nginx/ssl
-    depends_on:
-      - backend
-      - frontend
-    restart: unless-stopped
-```
-
-Run:
-```bash
-docker-compose up -d
-```
-
----
-
-### Option 3: Cloud Platform Deployment
-
-#### AWS EC2
-
-```bash
-# Launch EC2 instance (Ubuntu 20.04)
-# Connect and run:
-
-sudo apt-get update && sudo apt-get upgrade -y
-sudo apt-get install -y python3.9 python3-pip git supervisor nginx
-
-# Clone repository
-git clone <your-repo>
-cd antigravity/backend
-
-# Setup virtual environment
-python3.9 -m venv venv
-source venv/bin/activate
-pip install -r requirements.txt
-
-# Configure supervisor (see above)
-# Configure nginx (see above)
-```
-
-#### Heroku
-
-1. Create `Procfile` in backend directory:
-```
-web: gunicorn -w 4 main:app
-```
-
-2. Create `runtime.txt`:
-```
-python-3.9.16
-```
-
-3. Deploy:
-```bash
-heroku login
-heroku create antigravity-backend
-git push heroku main
-```
-
-#### Google Cloud Run
-
-```bash
-# Create Dockerfile (see above)
-
-# Deploy
-gcloud run deploy antigravity \
-  --source . \
-  --platform managed \
-  --region us-central1 \
-  --memory 2Gi \
-  --allow-unauthenticated \
-  --set-env-vars MODEL_PATH=/models
-```
-
----
-
-## 📱 Frontend Deployment
-
-### Option 1: Static Hosting
-
-Build frontend:
-```bash
-cd frontend
-npm install
-npm run build
-```
-
-Deploy `dist/` folder to:
-- **AWS S3 + CloudFront**
-- **Netlify**
-- **Vercel**
-- **GitHub Pages**
-- **Firebase Hosting**
-
-### Option 2: AWS S3 + CloudFront
-
-```bash
-# Build
-npm run build
-
-# Upload to S3
-aws s3 sync dist/ s3://antigravity-frontend/
-
-# Create CloudFront distribution (via AWS Console)
-# Point to S3 bucket
-```
-
-### Option 3: Netlify
-
-```bash
-# Install Netlify CLI
-npm install -g netlify-cli
-
-# Deploy
-netlify deploy --prod --dir dist
-```
-
-### Option 4: Vercel
-
-```bash
-# Install Vercel CLI
-npm install -g vercel
-
-# Deploy
-vercel --prod
-```
-
----
-
-## 🔒 Security Checklist
-
-- [ ] Enable HTTPS (SSL/TLS certificate)
-- [ ] Set strong CORS policy
-- [ ] Configure firewall rules
-- [ ] Enable rate limiting
-- [ ] Set file upload limits
-- [ ] Use environment variables for secrets
-- [ ] Enable logging and monitoring
-- [ ] Regular security updates
-- [ ] Set up backups
-- [ ] Monitor disk space
-
----
-
-## 📊 Performance Optimization
-
-### Backend Optimization
-
-1. **Enable Caching**
-```python
-from fastapi_cache import FastAPICache
-from fastapi_cache.backends.redis import RedisBackend
-from redis import asyncio as aioredis
-```
-
-2. **Database Connection Pooling**
-- Already handled by SQLAlchemy (if using database)
-
-3. **Model Quantization**
-- Reduce model size for faster inference
-
-4. **GPU Support**
-- Install CUDA for TensorFlow/PyTorch
-- Use GPU in model inference
-
-### Frontend Optimization
-
-1. **Enable Compression**
-```nginx
-gzip on;
-gzip_types text/plain text/css application/json application/javascript;
-```
-
-2. **CDN for Static Assets**
-- CloudFront, CloudFlare, etc.
-
-3. **Lazy Loading**
-- Already implemented in React components
-
-4. **Minification**
-- Automatic with `npm run build`
-
----
-
-## 📈 Monitoring & Logging
-
-### Backend Monitoring
-
-```python
-# Add to main.py
-import logging
-from pythonjsonlogger import jsonlogger
-
-logHandler = logging.FileHandler('/var/log/antigravity/app.log')
-formatter = jsonlogger.JsonFormatter()
-logHandler.setFormatter(formatter)
-logger.addHandler(logHandler)
-```
-
-### Monitoring Tools
-
-- **Prometheus** - Metrics collection
-- **Grafana** - Visualization
-- **ELK Stack** - Log analysis
-- **New Relic** - APM
-- **Sentry** - Error tracking
-
-### Health Checks
-
-```yaml
-# Docker health check
-healthcheck:
-  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
-  interval: 30s
-  timeout: 10s
-  retries: 3
-  start_period: 40s
-```
-
----
-
-## 🔄 CI/CD Pipeline
-
-### GitHub Actions Example
-
-`.github/workflows/deploy.yml`:
-
-```yaml
-name: Deploy ANTIGRAVITY
-
-on:
-  push:
-    branches: [main]
-
-jobs:
-  deploy:
-    runs-on: ubuntu-latest
-    
-    steps:
-      - uses: actions/checkout@v2
-      
-      - name: Deploy Backend
-        run: |
-          ssh ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }}
-          cd antigravity/backend
-          git pull origin main
-          pip install -r requirements.txt
-          supervisorctl restart antigravity
-      
-      - name: Deploy Frontend
-        run: |
-          npm install
-          npm run build
-          aws s3 sync dist/ s3://antigravity-frontend/
-```
-
----
-
-## 📋 Deployment Checklist
-
-### Before Deployment
-
-- [ ] All tests passing
-- [ ] Environment variables configured
-- [ ] Model file in production location
-- [ ] SSL certificate installed
-- [ ] Database migrations completed
-- [ ] Monitoring configured
-- [ ] Backups scheduled
-
-### After Deployment
-
-- [ ] Health check endpoint responding
-- [ ] API endpoints accessible
-- [ ] Frontend loading correctly
-- [ ] Predictions working
-- [ ] Logs monitored
-- [ ] Performance baseline recorded
-
----
-
-## 🚨 Troubleshooting
-
-### Backend Not Starting
-
-```bash
-# Check logs
-supervisorctl tail antigravity -f
-
-# Verify Python environment
-source /home/antigravity/antigravity/backend/venv/bin/activate
-python main.py
-```
-
-### High Memory Usage
-
-```bash
-# Check process memory
-ps aux | grep gunicorn
-
-# Reduce worker count in supervisor config
--w 2  # Instead of 4
-```
-
-### Slow Predictions
-
-- Verify GPU is enabled
-- Check model optimization
-- Monitor CPU usage
-- Reduce batch size threshold
-
----
-
-## 📞 Support
-
-For deployment issues:
-1. Check logs (above)
-2. Verify configuration
-3. Test locally first
-4. Check documentation
-5. Contact support
-
----
-
-**Deployment Version**: 1.0.0
-**Last Updated**: 2024
diff --git a/MODEL_INTEGRATION.md b/MODEL_INTEGRATION.md
deleted file mode 100644
index ef97133..0000000
--- a/MODEL_INTEGRATION.md
+++ /dev/null
@@ -1,468 +0,0 @@
-# ANTIGRAVITY Model Integration Guide
-
-Complete guide for integrating your Kaggle-trained pneumonia detection model.
-
-## 📌 Overview
-
-This guide walks you through integrating your trained pneumonia detection model with ANTIGRAVITY.
-
-**Important**: The application includes placeholders designed to be easily replaced with your model.
-
----
-
-## 🎯 Quick Integration (5 Steps)
-
-### Step 1: Prepare Your Model File
-
-```bash
-# Create models directory in backend
-mkdir -p backend/models
-
-# Copy your trained model
-cp path/to/your/pneumonia_model.h5 backend/models/
-```
-
-**Supported formats**:
-- TensorFlow/Keras: `.h5`, `.pb`
-- PyTorch: `.pt`, `.pth`
-- scikit-learn: `.pkl`, `.joblib`
-- ONNX: `.onnx`
-
-### Step 2: Update requirements.txt
-
-Add your ML framework to `backend/requirements.txt`:
-
-```text
-# Add one of these:
-tensorflow==2.14.0
-# torch==2.1.0
-# scikit-learn==1.3.2
-```
-
-Install:
-```bash
-cd backend
-pip install -r requirements.txt
-```
-
-### Step 3: Update Model Loader
-
-Edit `backend/services/model_loader.py`:
-
-Replace:
-```python
-def load_model():
-    model = ModelPlaceholder()
-    model.is_loaded = True
-    return model
-```
-
-With your actual loading code (see examples below).
-
-### Step 4: Update Preprocessing
-
-Edit `backend/utils/preprocess.py`:
-
-Update configuration values to match your training:
-```python
-IMG_WIDTH = 224  # Your model input width
-IMG_HEIGHT = 224  # Your model input height
-IMG_CHANNELS = 1  # 1 for grayscale, 3 for RGB
-NORMALIZATION_MEAN = 0.5  # Your training mean
-NORMALIZATION_STD = 0.5  # Your training std
-```
-
-And update preprocessing functions if needed.
-
-### Step 5: Test
-
-```bash
-# Start backend
-python backend/main.py
-
-# Test with cURL
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@test_xray.png"
-```
-
----
-
-## 📚 Complete Integration Examples
-
-### Example 1: TensorFlow/Keras Model
-
-**Your model structure**:
-```
-- pneumonia_model.h5 (trained model)
-- Model trained with: Conv2D → Dense → Output (2 classes: Normal, Pneumonia)
-```
-
-**Update `backend/services/model_loader.py`**:
-
-```python
-import tensorflow as tf
-import numpy as np
-
-# Global model cache
-_model_instance = None
-
-def load_model():
-    """Load TensorFlow/Keras model"""
-    global _model_instance
-    
-    try:
-        logger.info("Loading TensorFlow model...")
-        
-        # Load the model
-        model = tf.keras.models.load_model('backend/models/pneumonia_model.h5')
-        
-        # Verify model
-        logger.info(f"Model loaded successfully")
-        logger.info(f"Input shape: {model.input_shape}")
-        logger.info(f"Output shape: {model.output_shape}")
-        
-        return model
-        
-    except FileNotFoundError:
-        logger.error("Model file not found at backend/models/pneumonia_model.h5")
-        raise
-    except Exception as e:
-        logger.error(f"Failed to load model: {str(e)}")
-        raise
-
-
-def predict(model, preprocessed_images: List) -> List[dict]:
-    """Run inference with TensorFlow model"""
-    try:
-        if not preprocessed_images:
-            return []
-        
-        # Convert list to numpy array
-        batch = np.array(preprocessed_images)
-        logger.info(f"Running inference on batch shape: {batch.shape}")
-        
-        # Get predictions (output shape: [batch_size, 2])
-        # Assuming your model outputs [prob_normal, prob_pneumonia]
-        predictions = model.predict(batch, batch_size=32)
-        
-        results = []
-        for i, pred in enumerate(predictions):
-            # Extract probabilities
-            prob_normal = float(pred[0])
-            prob_pneumonia = float(pred[1])
-            
-            # Determine prediction
-            is_pneumonia = prob_pneumonia > prob_normal
-            
-            result = {
-                "prediction": "Pneumonia" if is_pneumonia else "Normal",
-                "confidence": float(max(prob_normal, prob_pneumonia) * 100),
-                "probability_normal": prob_normal,
-                "probability_pneumonia": prob_pneumonia
-            }
-            results.append(result)
-            
-        logger.info(f"Inference complete: {len(results)} predictions")
-        return results
-        
-    except Exception as e:
-        logger.error(f"Prediction failed: {str(e)}")
-        raise
-
-
-def get_model():
-    """Singleton pattern for model loading"""
-    global _model_instance
-    if _model_instance is None:
-        _model_instance = load_model()
-    return _model_instance
-```
-
-**Update `backend/utils/preprocess.py`**:
-
-```python
-# If your model was trained with these settings, update:
-IMG_WIDTH = 224
-IMG_HEIGHT = 224
-IMG_CHANNELS = 1  # Grayscale
-NORMALIZATION_MEAN = 0.5
-NORMALIZATION_STD = 0.5
-
-# If you used ImageDataGenerator or different normalization:
-# NORMALIZATION_MEAN = 100.0  # Dataset mean pixel value
-# NORMALIZATION_STD = 50.0    # Dataset standard deviation
-```
-
----
-
-### Example 2: PyTorch Model
-
-**Your model structure**:
-```python
-class PneumoniaNet(nn.Module):
-    def __init__(self):
-        super().__init__()
-        self.fc = nn.Linear(224*224, 2)
-    
-    def forward(self, x):
-        x = x.view(x.size(0), -1)
-        return self.fc(x)
-```
-
-**Update `backend/services/model_loader.py`**:
-
-```python
-import torch
-import torch.nn as nn
-import torch.nn.functional as F
-
-class PneumoniaNet(nn.Module):
-    """Define your model architecture"""
-    def __init__(self):
-        super().__init__()
-        # Copy your model architecture here
-        self.features = nn.Sequential(
-            nn.Conv2d(1, 32, kernel_size=3),
-            nn.ReLU(inplace=True),
-            nn.MaxPool2d(kernel_size=2),
-            # ... more layers
-        )
-        self.classifier = nn.Sequential(
-            nn.Linear(32 * 111 * 111, 128),
-            nn.ReLU(inplace=True),
-            nn.Linear(128, 2)
-        )
-    
-    def forward(self, x):
-        x = self.features(x)
-        x = x.view(x.size(0), -1)
-        x = self.classifier(x)
-        return x
-
-
-def load_model():
-    """Load PyTorch model"""
-    try:
-        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
-        logger.info(f"Using device: {device}")
-        
-        # Load model
-        model = PneumoniaNet().to(device)
-        checkpoint = torch.load('backend/models/pneumonia_model.pt', 
-                               map_location=device)
-        model.load_state_dict(checkpoint)
-        model.eval()
-        
-        logger.info("PyTorch model loaded successfully")
-        return model
-        
-    except Exception as e:
-        logger.error(f"Failed to load model: {str(e)}")
-        raise
-
-
-def predict(model, preprocessed_images: List) -> List[dict]:
-    """Run inference with PyTorch model"""
-    try:
-        device = next(model.parameters()).device
-        batch = torch.from_numpy(np.array(preprocessed_images)).float().to(device)
-        
-        with torch.no_grad():
-            outputs = model(batch)
-            probabilities = F.softmax(outputs, dim=1)
-        
-        results = []
-        for probs in probabilities:
-            prob_normal = probs[0].item()
-            prob_pneumonia = probs[1].item()
-            
-            result = {
-                "prediction": "Pneumonia" if prob_pneumonia > prob_normal else "Normal",
-                "confidence": float(max(prob_normal, prob_pneumonia) * 100),
-                "probability_normal": prob_normal,
-                "probability_pneumonia": prob_pneumonia
-            }
-            results.append(result)
-        
-        return results
-        
-    except Exception as e:
-        logger.error(f"Prediction failed: {str(e)}")
-        raise
-```
-
----
-
-### Example 3: scikit-learn Model
-
-**Your pipeline**:
-```python
-from sklearn.pipeline import Pipeline
-from sklearn.preprocessing import StandardScaler
-from sklearn.ensemble import RandomForestClassifier
-
-pipeline = Pipeline([
-    ('scaler', StandardScaler()),
-    ('classifier', RandomForestClassifier())
-])
-```
-
-**Update `backend/services/model_loader.py`**:
-
-```python
-import pickle
-
-def load_model():
-    """Load scikit-learn model"""
-    try:
-        with open('backend/models/pneumonia_model.pkl', 'rb') as f:
-            model = pickle.load(f)
-        
-        logger.info("scikit-learn model loaded successfully")
-        return model
-        
-    except Exception as e:
-        logger.error(f"Failed to load model: {str(e)}")
-        raise
-
-
-def predict(model, preprocessed_images: List) -> List[dict]:
-    """Run inference with scikit-learn model"""
-    try:
-        # Flatten images for sklearn
-        batch_flat = np.array([img.flatten() for img in preprocessed_images])
-        
-        predictions = model.predict(batch_flat)
-        probabilities = model.predict_proba(batch_flat)
-        
-        results = []
-        for pred, probs in zip(predictions, probabilities):
-            result = {
-                "prediction": "Pneumonia" if pred == 1 else "Normal",
-                "confidence": float(max(probs) * 100),
-                "probability_normal": float(probs[0]),
-                "probability_pneumonia": float(probs[1])
-            }
-            results.append(result)
-        
-        return results
-        
-    except Exception as e:
-        logger.error(f"Prediction failed: {str(e)}")
-        raise
-```
-
----
-
-## 🔍 Verification Checklist
-
-### Before Integration
-
-- [ ] Model file is in `backend/models/` directory
-- [ ] Model format file extension matches framework
-- [ ] ML framework added to `requirements.txt`
-- [ ] Backend requirements installed: `pip install -r requirements.txt`
-
-### After Integration
-
-- [ ] Backend starts without errors: `python main.py`
-- [ ] Health check passes: `curl http://localhost:8000/health`
-- [ ] API configuration accessible: `curl http://localhost:8000/api/predict/config`
-- [ ] Prediction works with single image
-- [ ] Prediction works with multiple images
-- [ ] Confidence scores are reasonable (0-100%)
-- [ ] Results match expected format
-
-### Testing
-
-```bash
-# Test 1: Backend starts
-python backend/main.py
-# Should see: "INFO:     Started server process"
-
-# Test 2: Health check
-curl http://localhost:8000/health
-# Should return: {"status": "running"}
-
-# Test 3: Prediction
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@test_xray.png"
-# Should return JSON with predictions
-
-# Test 4: Multiple images
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@xray1.png" \
-  -F "files=@xray2.png"
-# Should return 2 predictions
-```
-
----
-
-## 🎓 Model Best Practices
-
-### Input Format
-- Ensure images are resized to model's expected dimensions
-- Check channel count (grayscale vs RGB)
-- Verify normalization matches training
-
-### Output Format
-- Model should output 2 values (probabilities for each class)
-- Probabilities should sum to 1.0
-- First output = Probability of Normal
-- Second output = Probability of Pneumonia
-
-### Performance
-- Profile inference time
-- Optimize for batch processing
-- Consider quantization for faster inference
-
----
-
-## 🐛 Troubleshooting
-
-| Issue | Solution |
-|-------|----------|
-| Model not found | Check file path and name |
-| Import error | Install ML framework: `pip install tensorflow` |
-| Shape mismatch | Verify preprocessing matches training |
-| Slow predictions | Reduce model size or use GPU |
-| Bad accuracy | Check preprocessing pipeline |
-| Memory issues | Reduce batch size or use 8-bit quantization |
-
----
-
-## 📊 Expected Output
-
-Your model predictions should return:
-
-```json
-{
-  "filename": "xray1.png",
-  "prediction": "Pneumonia",
-  "confidence": 96.4,
-  "probability_normal": 0.036,
-  "probability_pneumonia": 0.964,
-  "status": "success"
-}
-```
-
-Verify:
-- Confidence is 0-100%
-- Probabilities sum to ~1.0
-- Prediction matches higher probability
-
----
-
-## ✅ Integration Complete!
-
-Once tests pass, your model is integrated and ready for:
-- ✅ Production deployment
-- ✅ Batch predictions
-- ✅ API access
-- ✅ Frontend usage
-
----
-
-For detailed backend setup, see [SETUP.md](./SETUP.md)
-For API documentation, see [API_DOCS.md](./API_DOCS.md)
-For deployment, see [DEPLOYMENT.md](./DEPLOYMENT.md)
diff --git a/PROJECT_SUMMARY.md b/PROJECT_SUMMARY.md
deleted file mode 100644
index 45fccf4..0000000
--- a/PROJECT_SUMMARY.md
+++ /dev/null
@@ -1,498 +0,0 @@
-# ANTIGRAVITY - Project Summary & Quick Reference
-
-## 🎉 Project Status: COMPLETE ✅
-
-Your **ANTIGRAVITY** medical AI web application is fully built and ready for model integration.
-
----
-
-## 📦 What's Included
-
-### ✅ Backend (FastAPI + Python)
-- [x] REST API server with health check
-- [x] POST `/api/predict` endpoint for batch image processing
-- [x] Model loader placeholder (ready for your model)
-- [x] Image preprocessing pipeline (ready to customize)
-- [x] Comprehensive file validation
-- [x] Error handling and logging
-- [x] CORS enabled
-- [x] Gunicorn-ready production format
-
-### ✅ Frontend (React + Tailwind CSS)
-- [x] Professional medical UI design
-- [x] Two-column prediction interface
-- [x] Drag-and-drop upload area
-- [x] Image preview cards
-- [x] Real-time prediction results
-- [x] Confidence score visualization
-- [x] Responsive mobile design
-- [x] Loading states and error messages
-- [x] Smooth animations
-- [x] How It Works section
-- [x] Features showcase
-- [x] Medical disclaimer footer
-
-### ✅ Components
-**Backend**:
-- `main.py` - FastAPI application
-- `routes/predict.py` - Prediction endpoints
-- `services/model_loader.py` - Model placeholder
-- `utils/preprocess.py` - Image preprocessing
-
-**Frontend**:
-- `Navbar.jsx` - Navigation bar
-- `Hero.jsx` - Hero section
-- `PredictionInterface.jsx` - Main two-column layout
-- `UploadArea.jsx` - Drag-and-drop upload
-- `ImagePreviewCard.jsx` - Image thumbnail preview
-- `PredictionCard.jsx` - Result display
-- `LoadingSpinner.jsx` - Loading indicator
-- `ErrorMessage.jsx` - Error display
-- `HowItWorks.jsx` - Process explanation
-- `Features.jsx` - Feature showcase
-- `Footer.jsx` - Footer with medical disclaimer
-
-### ✅ Documentation
-- [x] README.md - Project overview
-- [x] SETUP.md - Setup and integration guide
-- [x] API_DOCS.md - Complete API reference
-- [x] MODEL_INTEGRATION.md - Model integration guide
-- [x] DEPLOYMENT.md - Production deployment guide
-- [x] frontend/README.md - Frontend setup guide
-
----
-
-## 🚀 Quick Start (3 Steps)
-
-### 1. Install Backend
-
-```bash
-cd backend
-python -m venv venv
-source venv/bin/activate  # Windows: venv\Scripts\activate
-pip install -r requirements.txt
-python main.py
-```
-
-Backend available at: `http://localhost:8000`
-
-### 2. Install Frontend
-
-```bash
-cd frontend
-npm install
-npm run dev
-```
-
-Frontend available at: `http://localhost:3000`
-
-### 3. Integrate Your Model
-
-1. Copy your trained model to `backend/models/`
-2. Update `backend/services/model_loader.py` with your model loading code
-3. Update `backend/utils/preprocess.py` if needed
-4. Add ML framework to `backend/requirements.txt`
-5. Restart backend server
-
-See [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) for detailed examples.
-
----
-
-## 📁 Project Structure
-
-```
-antigravity/
-├── backend/
-│   ├── main.py                   # FastAPI entry point
-│   ├── requirements.txt          # Python packages
-│   ├── routes/predict.py         # Prediction endpoints
-│   ├── services/model_loader.py  # Model placeholder
-│   ├── utils/preprocess.py       # Preprocessing pipeline
-│   └── .env.example              # Environment template
-│
-├── frontend/
-│   ├── src/
-│   │   ├── components/           # React components
-│   │   ├── services/apiService.js # API client
-│   │   ├── App.jsx               # Root component
-│   │   ├── index.jsx             # Entry point
-│   │   └── index.css             # Tailwind styles
-│   ├── package.json              # Node packages
-│   ├── vite.config.js            # Vite config
-│   ├── tailwind.config.js        # Tailwind config
-│   ├── index.html                # HTML entry
-│   ├── .env.example              # Environment template
-│   └── README.md                 # Frontend guide
-│
-├── README.md                     # Project overview
-├── SETUP.md                      # Setup instructions
-├── API_DOCS.md                   # API reference
-├── MODEL_INTEGRATION.md          # Model integration guide
-├── DEPLOYMENT.md                 # Deployment guide
-└── .gitignore                    # Git ignore rules
-```
-
----
-
-## 🔧 API Endpoints
-
-| Method | Endpoint | Purpose |
-|--------|----------|---------|
-| GET | `/health` | Server health check |
-| GET | `/` | API info |
-| POST | `/api/predict` | Submit images for prediction |
-| GET | `/api/predict/config` | Get API configuration |
-
----
-
-## 📊 Input/Output Format
-
-### Request (POST /api/predict)
-```
-multipart/form-data
-files: image1.png, image2.png, ...
-```
-
-### Response
-```json
-[
-  {
-    "filename": "xray1.png",
-    "prediction": "Pneumonia",
-    "confidence": 96.4,
-    "probability_normal": 0.036,
-    "probability_pneumonia": 0.964,
-    "status": "success"
-  }
-]
-```
-
----
-
-## 🧠 Model Integration Examples
-
-### TensorFlow/Keras
-```python
-import tensorflow as tf
-
-def load_model():
-    return tf.keras.models.load_model('backend/models/pneumonia_model.h5')
-
-def predict(model, images):
-    preds = model.predict(images)
-    # Format results...
-    return results
-```
-
-### PyTorch
-```python
-import torch
-
-def load_model():
-    model = MyModel()
-    model.load_state_dict(torch.load('backend/models/model.pt'))
-    return model
-
-def predict(model, images):
-    with torch.no_grad():
-        preds = model(torch.tensor(images))
-    # Format results...
-    return results
-```
-
-### scikit-learn
-```python
-import pickle
-
-def load_model():
-    with open('backend/models/model.pkl', 'rb') as f:
-        return pickle.load(f)
-
-def predict(model, images):
-    preds = model.predict(images)
-    # Format results...
-    return results
-```
-
-See [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) for complete examples.
-
----
-
-## 🎨 UI Features
-
-### Two-Column Layout
-- **Left**: Upload area with drag-and-drop
-- **Right**: Results display with predictions
-
-### Upload Features
-- Drag-and-drop support
-- Click-to-upload option
-- Multiple file upload (max 10)
-- File format validation (JPG, JPEG, PNG)
-- File size limit (10 MB each)
-- Image previews in grid
-- Individual image removal
-- Clear all button
-
-### Results Features
-- Image preview for each result
-- Prediction label (Pneumonia/Normal)
-- Confidence percentage
-- Probability breakdown
-- Color-coded badges
-- Progress bars for confidence
-- Scrollable results list
-
-### Design
-- Professional medical UI
-- Responsive mobile layout
-- Smooth animations
-- Tailwind CSS styling
-- Healthcare color palette
-- Accessible components
-
----
-
-## 🔒 Security Features
-
-- ✅ File type validation
-- ✅ File size validation
-- ✅ Batch size limits
-- ✅ CORS configuration
-- ✅ Input sanitization
-- ✅ Error handling
-- ✅ Model placeholder (no pre-trained model in repo)
-- ✅ Environment variables for sensitive config
-
----
-
-## 📈 Performance
-
-- **Preprocessing**: < 1s per image
-- **Inference**: Depends on your model
-- **Response time**: Typically < 5s for 10 images
-- **Batch processing**: Up to 10 images per request
-- **Frontend bundle**: ~150KB (gzipped)
-
----
-
-## 🚢 Deployment Ready
-
-### Backend
-- Gunicorn ASGI server format
-- Environment variable configuration
-- Docker support (create Dockerfile)
-- Production-ready error handling
-- Logging configured
-
-### Frontend
-- Vite build optimization
-- Environment variable support
-- Static file ready
-- CDN deployable
-- HTTPS ready
-
-See [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup.
-
----
-
-## ⚠️ Important Notes
-
-### Model Placeholder
-- **Model loading is a placeholder** - Replace with your actual model
-- **Preprocessing is customizable** - Adjust to match your training pipeline
-- **Predictions return mock data** - Update predict() function with real inference
-- **No pre-trained model included** - You must bring your own model
-
-### Medical Compliance
-- Medical disclaimer included in footer
-- Required for healthcare applications
-- Always review results with qualified professionals
-- Use only as screening aid, not diagnostic tool
-- Document all predictions in medical records
-
-### Production Checklist
-- [ ] Model file placed in backend/models/
-- [ ] ML framework installed
-- [ ] model_loader.py updated
-- [ ] preprocess.py customized
-- [ ] Backend tested locally
-- [ ] Frontend tested locally
-- [ ] Environment variables configured
-- [ ] HTTPS enabled
-- [ ] CORS configured for your domain
-- [ ] Logging enabled
-- [ ] Monitoring configured
-- [ ] Backups scheduled
-
----
-
-## 📞 Integration Support
-
-### For Each ML Framework
-
-**TensorFlow/Keras Requirements**:
-```bash
-pip install tensorflow
-```
-
-**PyTorch Requirements**:
-```bash
-pip install torch torchvision
-```
-
-**scikit-learn Requirements**:
-```bash
-pip install scikit-learn
-```
-
-See [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) for complete integration code.
-
----
-
-## 🧪 Testing Your Setup
-
-### Test Backend
-```bash
-# Health check
-curl http://localhost:8000/health
-
-# Configuration
-curl http://localhost:8000/api/predict/config
-
-# Prediction with test image
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@test_xray.png"
-```
-
-### Test Frontend
-```bash
-# Browser: http://localhost:3000
-# Upload test images
-# Verify results display
-# Check console for errors
-```
-
----
-
-## 📚 Documentation Files
-
-| File | Purpose |
-|------|---------|
-| README.md | Project overview |
-| SETUP.md | Backend & integration setup |
-| API_DOCS.md | Complete API reference |
-| MODEL_INTEGRATION.md | Model integration examples |
-| DEPLOYMENT.md | Production deployment |
-| frontend/README.md | Frontend setup |
-
----
-
-## 🎯 Next Steps
-
-1. **Prepare Your Model**
-   - Ensure model can process images
-   - Note input dimensions
-   - Note output format
-
-2. **Set Up Backend**
-   - Follow [SETUP.md](./SETUP.md)
-   - Install dependencies
-   - Integrate your model
-
-3. **Test Locally**
-   - Run backend on port 8000
-   - Run frontend on port 3000
-   - Upload test images
-   - Verify predictions
-
-4. **Deploy**
-   - Follow [DEPLOYMENT.md](./DEPLOYMENT.md)
-   - Choose deployment platform
-   - Configure production settings
-   - Monitor health
-
----
-
-## ✨ Features Summary
-
-### Functionality
-- ✅ Multiple image upload
-- ✅ Batch predictions
-- ✅ Real-time results
-- ✅ Confidence scoring
-- ✅ Error handling
-- ✅ Progress indication
-
-### Design
-- ✅ Professional UI
-- ✅ Responsive layout
-- ✅ Smooth animations
-- ✅ Medical branding
-- ✅ Accessible components
-- ✅ Dark mode ready
-
-### Architecture
-- ✅ Modular backend
-- ✅ Reusable components
-- ✅ Clean code structure
-- ✅ Proper separation of concerns
-- ✅ Scalable design
-- ✅ Production-ready
-
----
-
-## 📞 Support Resources
-
-### Documentation
-- Backend setup: [SETUP.md](./SETUP.md)
-- API reference: [API_DOCS.md](./API_DOCS.md)
-- Model integration: [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md)
-- Deployment: [DEPLOYMENT.md](./DEPLOYMENT.md)
-- Frontend: [frontend/README.md](./frontend/README.md)
-
-### Troubleshooting
-1. Check relevant documentation file
-2. Review code comments
-3. Check backend logs: `tail -f app.log`
-4. Check frontend console: F12 in browser
-5. Verify backend running: `curl http://localhost:8000/health`
-6. Verify frontend running: Visit `http://localhost:3000`
-
----
-
-## 🎓 Learning Resources
-
-- **FastAPI**: https://fastapi.tiangolo.com/
-- **React**: https://react.dev/
-- **Tailwind CSS**: https://tailwindcss.com/
-- **Vite**: https://vitejs.dev/
-
----
-
-## ✅ Project Checklist
-
-- [x] Backend API complete
-- [x] Frontend UI complete
-- [x] Model placeholder created
-- [x] Preprocessing pipeline created
-- [x] Documentation complete
-- [x] Error handling implemented
-- [x] Responsive design implemented
-- [x] Security features included
-- [x] Production-ready code
-- [x] Integration guide provided
-
----
-
-## 🚀 Ready to Deploy!
-
-ANTIGRAVITY is fully built and ready for your pneumonia detection model. 
-
-**Next action**: Integrate your Kaggle model following [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md)
-
----
-
-**Project Version**: 1.0.0  
-**Last Updated**: 2024  
-**Status**: Production Ready ✅
diff --git a/QUICK_REFERENCE.md b/QUICK_REFERENCE.md
deleted file mode 100644
index 57311b6..0000000
--- a/QUICK_REFERENCE.md
+++ /dev/null
@@ -1,262 +0,0 @@
-# ANTIGRAVITY - Quick Reference Card
-
-## ⚡ Start in 30 Seconds
-
-```bash
-# Terminal 1: Backend
-cd backend
-python -m venv venv
-source venv/bin/activate  # Windows: venv\Scripts\activate
-pip install -r requirements.txt
-python main.py
-
-# Terminal 2: Frontend
-cd frontend
-npm install
-npm run dev
-```
-
-**URLs**:
-- Backend: http://localhost:8000
-- Frontend: http://localhost:3000
-- Swagger Docs: http://localhost:8000/docs
-
----
-
-## 🧠 Integrate Your Model (3 Steps)
-
-1. **Copy Model**
-   ```bash
-   cp your_model.h5 backend/models/
-   ```
-
-2. **Update `backend/services/model_loader.py`**
-   ```python
-   import tensorflow as tf
-   
-   def load_model():
-       return tf.keras.models.load_model('backend/models/your_model.h5')
-   
-   def predict(model, preprocessed_images):
-       preds = model.predict(preprocessed_images)
-       # Format to expected output...
-   ```
-
-3. **Install ML Framework**
-   ```bash
-   pip install tensorflow  # or torch, scikit-learn
-   pip install -r requirements.txt
-   ```
-
-See [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) for complete examples.
-
----
-
-## 📊 API Usage
-
-### Test Prediction
-```bash
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@image1.png" \
-  -F "files=@image2.png"
-```
-
-### Response Format
-```json
-[
-  {
-    "filename": "image1.png",
-    "prediction": "Pneumonia",
-    "confidence": 96.4,
-    "probability_normal": 0.036,
-    "probability_pneumonia": 0.964,
-    "status": "success"
-  }
-]
-```
-
----
-
-## 📁 Key Files
-
-| File | Purpose |
-|------|---------|
-| `backend/main.py` | FastAPI server |
-| `backend/services/model_loader.py` | **UPDATE WITH YOUR MODEL** |
-| `backend/utils/preprocess.py` | **CUSTOMIZE IF NEEDED** |
-| `backend/routes/predict.py` | Prediction endpoint |
-| `frontend/src/App.jsx` | React app root |
-| `frontend/src/components/PredictionInterface.jsx` | Main UI |
-
----
-
-## 🎯 Environment Setup
-
-**Backend** `.env`:
-```
-MODEL_PATH=backend/models/pneumonia_model.h5
-MODEL_TYPE=tensorflow
-IMAGE_WIDTH=224
-IMAGE_HEIGHT=224
-```
-
-**Frontend** `.env.local`:
-```
-REACT_APP_API_URL=http://localhost:8000/api
-```
-
----
-
-## ✅ Verification
-
-```bash
-# Backend health
-curl http://localhost:8000/health
-# Returns: {"status": "running"}
-
-# Frontend loads
-# Visit: http://localhost:3000
-
-# Upload test image
-curl -X POST "http://localhost:8000/api/predict" \
-  -F "files=@test.png"
-# Should return predictions
-```
-
----
-
-## 📚 Documentation
-
-- **Overview**: [README.md](./README.md)
-- **Setup**: [SETUP.md](./SETUP.md)
-- **API**: [API_DOCS.md](./API_DOCS.md)
-- **Model Integration**: [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md)
-- **Deployment**: [DEPLOYMENT.md](./DEPLOYMENT.md)
-- **Frontend**: [frontend/README.md](./frontend/README.md)
-
----
-
-## 🚀 Production Deployment
-
-**Backend** (Gunicorn):
-```bash
-pip install gunicorn
-gunicorn -w 4 -b 0.0.0.0:8000 main:app
-```
-
-**Frontend** (Build & Deploy):
-```bash
-npm run build
-# Deploy dist/ folder to:
-# - Netlify
-# - Vercel
-# - AWS S3
-# - GitHub Pages
-```
-
-See [DEPLOYMENT.md](./DEPLOYMENT.md) for details.
-
----
-
-## 🔧 Troubleshooting
-
-| Issue | Solution |
-|-------|----------|
-| Port 8000 in use | `lsof -i :8000` / `kill <PID>` |
-| Port 3000 in use | `npm run dev -- --port 3001` |
-| Module not found | `pip install -r requirements.txt` |
-| CORS error | Check backend CORS config |
-| Model not loading | Verify file path and format |
-| Predictions wrong format | Check preprocessing + output |
-
----
-
-## 🎨 Component Structure
-
-```
-Frontend/
-├── Hero (Landing)
-├── PredictionInterface
-│   ├── Left: UploadArea
-│   ├── Right: PredictionCard(s)
-├── HowItWorks
-├── Features
-└── Footer (Medical Disclaimer)
-```
-
----
-
-## 📊 File Limits
-
-- **Max files per batch**: 10
-- **Max file size**: 10 MB
-- **Supported formats**: JPG, JPEG, PNG
-
----
-
-## 💡 Pro Tips
-
-1. **Batch Processing**: Send max 10 images for efficiency
-2. **Preprocessing**: Match training pipeline exactly
-3. **Model Format**: Convert to checkpoint if needed
-4. **GPU Support**: Install CUDA for faster inference
-5. **Monitoring**: Add health checks to production
-
----
-
-## ⚠️ Medical Disclaimer
-
-This is an AI-assisted screening tool. 
-
-- **Required for healthcare use**
-- **Not a substitute for professional diagnosis**
-- **Always review with qualified professionals**
-- **Document all results**
-
----
-
-## 🔗 Important Links
-
-- **FastAPI Docs**: http://localhost:8000/docs
-- **Vite Guide**: https://vitejs.dev/
-- **React Guide**: https://react.dev/
-- **Tailwind Guide**: https://tailwindcss.com/
-
----
-
-## 📞 Common Tasks
-
-### Add New Endpoint
-Edit: `backend/routes/predict.py`
-
-### Customize UI
-Edit: `frontend/src/components/`
-
-### Change Image Size
-Edit: `backend/utils/preprocess.py`
-
-### Update Branding
-Edit: `frontend/src/components/Navbar.jsx`
-
-### Modify Colors
-Edit: `frontend/tailwind.config.js`
-
----
-
-## ✨ What's Included
-
-✅ Backend API (FastAPI)  
-✅ Frontend UI (React)  
-✅ Model Placeholder  
-✅ Preprocessing Pipeline  
-✅ Documentation (5 guides)  
-✅ Error Handling  
-✅ Responsive Design  
-✅ Medical Disclaimer  
-✅ Production Ready  
-
----
-
-**Status**: ✅ Ready to Integrate Your Model  
-**Current Version**: 1.0.0  
-**Last Updated**: 2024
diff --git a/README.md b/README.md
index a61d597..8ee2309 100644
--- a/README.md
+++ b/README.md
@@ -1,176 +1,181 @@
-AI-Powered Pneumonia Detection System
+<div align="center">
 
-Professional-grade medical AI web application for chest X-ray pneumonia detection.
+# 🫁 PulmoNet
 
-## 🎯 Overview
-- **Modern React Frontend** with premium healthcare UI
-- **FastAPI Backend** with robust API design
-- **Modular ML Integration** for easy model swapping
-- **Hospital-grade Security** and validation
-- **Batch Processing** capabilities
-- **Professional Medical Design**
+### Pneumonia screening from chest X-rays — upload a scan, get a result in seconds.
 
-## ✨ Key Features
+A full-stack deep learning application that pairs a **ResNet-50 classifier** with a **classical computer-vision pipeline** (CLAHE enhancement, bilateral denoising, lung segmentation) behind a fast REST API and a clean React interface.
 
-- ✅ Multi-image upload with drag-and-drop
-- ✅ Batch prediction support (up to 10 images)
-- ✅ Two-column UI (Upload + Results)
-- ✅ Real-time confidence scores
-- ✅ Professional medical color palette
-- ✅ Responsive mobile design
-- ✅ Comprehensive error handling
-- ✅ REST API with full documentation
-- ✅ Model placeholder integration
+![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
+![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?logo=pytorch&logoColor=white)
+![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)
+![OpenCV](https://img.shields.io/badge/OpenCV-4.8-5C3EE8?logo=opencv&logoColor=white)
+![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
+![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
+![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss&logoColor=white)
 
-## 📁 Project Structure
+[Features](#-features) · [How it works](#-how-it-works) · [Getting started](#-getting-started) · [API](#-api-reference) · [Team](#-team)
+
+</div>
+
+---
+
+## 📖 Why PulmoNet?
+
+Pneumonia is one of the leading causes of death worldwide, especially among children and the elderly, and chest X-rays are the frontline tool for diagnosing it. Reading them takes trained radiologists — who are scarce in many regions — and time that patients don't always have.
+
+PulmoNet is our attempt at a **second pair of eyes**: a screening tool that flags likely pneumonia cases so they can be prioritised for expert review. It is built end to end — from image preprocessing and a trained CNN to a production-style API and a web interface anyone can use.
+
+> ⚠️ PulmoNet is a research and educational project. It is **not** a medical device and must not be used as a substitute for diagnosis by a qualified clinician.
+
+---
+
+## ✨ Features
+
+| | |
+|---|---|
+| 🧠 **Deep learning inference** | ResNet-50 backbone with a dropout + single-logit head, fine-tuned for binary Normal / Pneumonia classification |
+| 🔬 **Medical-grade preprocessing** | Min-max normalisation → resize to 256×256 → CLAHE contrast enhancement → bilateral denoising |
+| 🫁 **Lung segmentation** | Threshold + morphology + connected-component filtering isolates the lung fields from the spine, heart and shoulders |
+| 🔁 **Graceful fallback** | If the model weights or PyTorch are unavailable, a feature-based classifier (intensity, histogram, texture, lung-area features) keeps the API serving |
+| 📦 **Batch analysis** | Upload up to 10 X-rays at once, each scored independently with its own confidence |
+| 🖱️ **Drag-and-drop UI** | Instant previews, per-image result cards, confidence bars and clear error states |
+| 🛡️ **Input validation** | Extension + MIME checks, 10 MB per-file cap, batch-size limits, sanitised error responses |
+| ⚙️ **Swappable checkpoints** | Two trained variants ship in the repo; choose one with a single env var |
+| 🪶 **Lightweight deploys** | CPU-only PyTorch build so the backend fits on free-tier hosts (≈512 MB RAM) |
+
+---
+
+## 🔍 How it works
+
+```
+ ┌──────────────┐     multipart/form-data     ┌───────────────────────────────────────────────┐
+ │  React UI    │ ──────────────────────────▶ │ FastAPI  /api/predict                          │
+ │  (Vite +     │                             │                                                │
+ │  Tailwind)   │ ◀────────────────────────── │  1. Validate type / size / count               │
+ └──────────────┘     JSON predictions        │  2. Decode → grayscale                         │
+                                              │  3. Normalise → 256×256 → CLAHE → bilateral    │
+                                              │  4. Segment lungs (fallback-safe)              │
+                                              │  5. ResNet-50 → sigmoid → probability          │
+                                              │     └─ no model? feature-based classifier      │
+                                              └───────────────────────────────────────────────┘
+```
+
+**Model.** A ResNet-50 (bottleneck blocks, layers `3-4-6-3`) whose classifier head is replaced with `Dropout(0.5) → Linear(2048, 1)`. The grayscale scan is replicated across three channels, passed through the network, and the sigmoid of the output logit gives the pneumonia probability. Predictions at or above 0.5 are labelled *Pneumonia*.
+
+**Checkpoints.** Two trained weight files live in `backend/models/`:
+
+| File | Description |
+|---|---|
+| `model_clahe.pth` | Trained on CLAHE-enhanced images (default, `MODEL_VARIANT=clahe`) |
+| `best_model.pth` | Best checkpoint from the baseline training run |
+
+The loader understands plain `state_dict`s, full pickled modules, and multi-variant checkpoint dictionaries, so you can drop in new weights without touching code.
+
+---
+
+## 🗂️ Project structure
 
 ```
-antigravity/
-├── backend/                 # FastAPI backend
-│   ├── main.py             # Application entry point
+PulmoNet/
+├── backend/
+│   ├── main.py                 # FastAPI app, CORS, logging, error handlers
+│   ├── schemas.py              # Pydantic response models
 │   ├── routes/
-│   │   ├── predict.py      # Prediction endpoints
-│   │   └── __init__.py
+│   │   └── predict.py          # /api/predict, /api/analyze, /api/predict/config, /api/health
 │   ├── services/
-│   │   ├── model_loader.py # Model loading placeholder
-│   │   └── __init__.py
+│   │   ├── xray_model.py       # ResNet-50, preprocessing, lung segmentation, feature fallback
+│   │   └── model_loader.py     # Singleton model loading + warm-up
 │   ├── utils/
-│   │   ├── preprocess.py   # Image preprocessing pipeline
-│   │   └── __init__.py
-│   └── requirements.txt     # Python dependencies
-│
-├── frontend/                # React frontend
-│   ├── src/
-│   │   ├── components/      # Reusable components
-│   │   ├── pages/          # Page components
-│   │   ├── services/       # API services
-│   │   ├── App.jsx         # Root component
-│   │   ├── index.jsx       # Entry point
-│   │   └── index.css       # Tailwind styles
-│   ├── public/             # Static assets
-│   ├── package.json        # Node dependencies
-│   ├── vite.config.js      # Vite configuration
-│   ├── tailwind.config.js  # Tailwind configuration
-│   └── index.html          # HTML entry point
+│   │   └── preprocess.py       # Image validation & preprocessing helpers
+│   ├── models/                 # Trained .pth checkpoints
+│   ├── test_model.py           # Model integration tests
+│   └── requirements.txt
 │
-├── README.md               # This file
-├── SETUP.md               # Setup instructions
-└── API_DOCS.md            # API documentation
+└── frontend/
+    ├── src/
+    │   ├── components/         # Navbar, Hero, UploadArea, PredictionCard, …
+    │   ├── services/apiService.js
+    │   ├── App.jsx
+    │   └── index.jsx
+    ├── index.html
+    ├── vite.config.js
+    └── tailwind.config.js
 ```
 
-## 🚀 Quick Start
+---
+
+## 🚀 Getting started
 
 ### Prerequisites
-- Python 3.8+
-- Node.js 16+
-- npm or yarn
 
-### Backend Setup
+- Python **3.10+**
+- Node.js **18+** and npm
 
-1. Navigate to backend directory:
-```bash
-cd backend
-```
+### 1 · Clone
 
-2. Create virtual environment:
 ```bash
-python -m venv venv
-source venv/bin/activate  # On Windows: venv\Scripts\activate
+git clone https://github.com/variablePotato/PulmoNet.git
+cd PulmoNet
 ```
 
-3. Install dependencies:
-```bash
-pip install -r requirements.txt
-```
+### 2 · Backend
 
-4. Run development server:
 ```bash
+cd backend
+python -m venv venv
+source venv/bin/activate          # Windows: venv\Scripts\activate
+pip install -r requirements.txt
+cp .env.example .env              # optional: tweak MODEL_VARIANT, PORT, CORS
 python main.py
 ```
 
-Backend will be available at `http://localhost:8000`
+The API is now live at **http://localhost:8000** — interactive docs at **http://localhost:8000/docs**.
 
-### Frontend Setup
+### 3 · Frontend
 
-1. Navigate to frontend directory:
 ```bash
 cd frontend
-```
-
-2. Install dependencies:
-```bash
 npm install
-```
-
-3. Create environment file `.env`:
-```
-REACT_APP_API_URL=http://localhost:8000/api
-```
-
-4. Run development server:
-```bash
+cp .env.example .env              # VITE_API_URL=http://localhost:8000/api
 npm run dev
 ```
 
-Frontend will be available at `http://localhost:3000`
-
-## 🔧 Model Integration
+Open **http://localhost:3000**, drop in a chest X-ray, and hit analyse.
 
-The application includes **placeholder model integration**. To integrate your trained Kaggle model:
+### Configuration
 
-### Step 1: Prepare Your Model
-```bash
-mkdir -p backend/models
-# Copy your trained model to: backend/models/pneumonia_model.h5 (or .pkl, .pt)
-```
+| Variable | Where | Default | Purpose |
+|---|---|---|---|
+| `PORT` | backend | `8000` | API port |
+| `MODEL_VARIANT` | backend | `clahe` | Which checkpoint variant to load |
+| `VITE_API_URL` | frontend | `http://localhost:8000/api` | Backend base URL |
+| `VITE_API_TIMEOUT_MS` | frontend | `60000` | Request timeout |
+| `VITE_API_RETRIES` | frontend | `1` | Retries on network failure |
 
-### Step 2: Update Model Loader
-Edit `backend/services/model_loader.py`:
-
-```python
-# Replace the load_model() function with:
-def load_model():
-    import tensorflow as tf
-    model = tf.keras.models.load_model('models/pneumonia_model.h5')
-    return model
-
-# Replace the predict() function with:
-def predict(model, preprocessed_images):
-    predictions = model.predict(preprocessed_images)
-    results = []
-    for pred in predictions:
-        results.append({
-            "prediction": "Pneumonia" if pred[0] > 0.5 else "Normal",
-            "confidence": float(max(pred) * 100),
-            "probability_normal": float(pred[0]),
-            "probability_pneumonia": float(pred[1])
-        })
-    return results
-```
+---
 
-### Step 3: Update Preprocessing
-Edit `backend/utils/preprocess.py` to match your model's training preprocessing
+## 📡 API reference
 
-## 📊 API Endpoints
+| Method | Endpoint | Description |
+|---|---|---|
+| `GET` | `/api/health` | Service and model status |
+| `GET` | `/api/predict/config` | Accepted formats and upload limits |
+| `POST` | `/api/predict` | Classify one or more X-rays |
+| `POST` | `/api/analyze` | Alias of `/predict` |
 
-### Health Check
-```
-GET /health
-Response: {"status": "running"}
-```
+**Example**
 
-### Predict
+```bash
+curl -X POST http://localhost:8000/api/predict \
+  -F "files=@chest_xray_1.png" \
+  -F "files=@chest_xray_2.jpg"
 ```
-POST /api/predict
-Content-Type: multipart/form-data
 
-Request:
-- files: List of image files (JPG, JPEG, PNG)
-
-Response:
+```json
 [
   {
-    "filename": "xray1.png",
+    "filename": "chest_xray_1.png",
     "prediction": "Pneumonia",
     "confidence": 96.4,
     "probability_normal": 0.036,
@@ -180,119 +185,70 @@ Response:
 ]
 ```
 
-### Configuration
-```
-GET /api/predict/config
-Response: Configuration and constraints
-```
-
-## 🎨 UI Components
+**Limits:** JPG / JPEG / PNG only · max 10 MB per file · max 10 files per request.
 
-- **Navbar** - Navigation with logo
-- **Hero** - Landing section with CTA
-- **UploadArea** - Drag-and-drop upload zone
-- **ImagePreviewCard** - Image thumbnail preview
-- **PredictionCard** - Result display with confidence
-- **LoadingSpinner** - Loading indicator
-- **ErrorMessage** - Error notification
-- **HowItWorks** - Process explanation
-- **Features** - Product features showcase
-- **Footer** - Footer with medical disclaimer
-
-## 🔒 Security
-
-- File type validation (JPG, JPEG, PNG only)
-- File size limit (10 MB per file)
-- Batch size limit (10 files maximum)
-- CORS enabled for safe cross-origin requests
-- Input sanitization
-- Error handling without exposing internals
+---
 
-## 📱 Responsive Design
+## 🧪 Testing
 
-- Mobile-first approach
-- Tablet optimization
-- Desktop full-featured layout
-- Touch-friendly UI elements
-- Flexible grid system
+```bash
+cd backend
+python test_model.py
+```
 
-## ⚠️ Medical Disclaimer
+Verifies that the checkpoint loads, the preprocessing pipeline produces the expected tensor shape, and inference returns well-formed predictions.
 
-**IMPORTANT:** ANTIGRAVITY is an AI-assisted screening tool and is **NOT a substitute for professional medical diagnosis**. 
+---
 
-All predictions must be:
-- Reviewed by qualified healthcare professionals
-- Used only as a screening aid
-- Followed by proper clinical evaluation
-- Documented in patient records
+## ☁️ Deployment
 
-## 🚢 Deployment
+**Backend** — any Python host works. The CPU-only PyTorch wheel keeps memory low enough for free tiers such as Render:
 
-### Backend Deployment (Gunicorn)
 ```bash
-gunicorn -w 4 -b 0.0.0.0:8000 main:app
+uvicorn main:app --host 0.0.0.0 --port $PORT
 ```
 
-### Frontend Deployment
+**Frontend** — build static assets and serve them from Vercel, Netlify or any CDN:
+
 ```bash
-npm run build
-# Deploy dist/ directory to static hosting
+npm run build      # outputs to frontend/dist
 ```
 
-See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment guidance.
+Remember to set `VITE_API_URL` to your deployed backend and add the frontend origin to the backend's CORS list.
 
-## 📚 Documentation
-
-- [SETUP.md](./SETUP.md) - Detailed setup instructions
-- [API_DOCS.md](./API_DOCS.md) - Complete API reference
-- [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) - Model integration guide
-- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment instructions
+---
 
-## 🛠️ Development
+## 🛣️ Roadmap
 
-### Running Tests
-```bash
-# Backend tests
-cd backend
-pytest
+- [ ] Grad-CAM heatmaps to show *where* the model is looking
+- [ ] Multi-class output (bacterial vs. viral pneumonia)
+- [ ] Downloadable PDF screening report per scan
+- [ ] Docker Compose setup for one-command local runs
+- [ ] Published evaluation metrics (accuracy, sensitivity, specificity, AUC) on a held-out test set
 
-# Frontend tests
-cd frontend
-npm test
-```
+---
 
-### Code Quality
-```bash
-# Linting
-cd frontend
-npm run lint
-```
+## 👥 Team
 
-## 📈 Performance
+PulmoNet was designed and built by:
 
-- Batch processing: Up to 10 images per request
-- Image preprocessing: < 1s per image
-- Model inference: Depends on your model
-- Response time: Typically < 5s for batch of 10
+| | Name | GitHub |
+|---|---|---|
+| 🧑‍💻 | **Aryan Raj** | [@ARYAN10227](https://github.com/ARYAN10227) |
+| 🧑‍💻 | **Ayush Kumar** | [@variablePotato](https://github.com/variablePotato) |
 
-## 🤝 Contributing
+Found a bug or have an idea? [Open an issue](https://github.com/variablePotato/PulmoNet/issues) — contributions are welcome.
 
-1. Create feature branch
-2. Implement changes
-3. Test thoroughly
-4. Submit pull request
+---
 
-## 📄 License
+## ⚕️ Medical disclaimer
 
-This project is licensed under the MIT License.
+PulmoNet is intended for research and educational purposes only. Its outputs are probabilistic screening signals, **not diagnoses**. Every result must be reviewed by a qualified healthcare professional before any clinical decision is made.
 
-## 📞 Support
+<div align="center">
 
-For issues, questions, or suggestions:
-- Open GitHub issue
-- Contact: [email]
-- Documentation: [docs]
+<br>
 
----
+Made with ☕ and a lot of chest X-rays.
 
-**ANTIGRAVITY** - AI-powered chest X-ray screening for pneumonia detectio.
+</div>
diff --git a/SETUP.md b/SETUP.md
deleted file mode 100644
index 4dd390b..0000000
--- a/SETUP.md
+++ /dev/null
@@ -1,391 +0,0 @@
-# ANTIGRAVITY Backend - Setup & Integration Guide
-
-Complete guide for setting up and integrating your pneumonia detection model.
-
-## 🔧 Prerequisites
-
-- Python 3.8 or higher
-- pip (Python package manager)
-- Virtual environment support
-
-## 📦 Installation
-
-### 1. Create Virtual Environment
-
-```bash
-# Navigate to backend directory
-cd backend
-
-# Create virtual environment
-python -m venv venv
-
-# Activate virtual environment
-# On Windows:
-venv\Scripts\activate
-
-# On macOS/Linux:
-source venv/bin/activate
-```
-
-### 2. Install Dependencies
-
-```bash
-pip install -r requirements.txt
-```
-
-### 3. Verify Installation
-
-```bash
-python -c "import fastapi; import uvicorn; print('All dependencies installed!')"
-```
-
-## 🚀 Running the Backend
-
-### Development Mode
-
-```bash
-python main.py
-```
-
-Server will start at `http://localhost:8000`
-
-### Production Mode
-
-```bash
-gunicorn -w 4 -b 0.0.0.0:8000 main:app
-```
-
-## 📊 API Documentation
-
-Once the server is running, visit:
-- **Swagger UI**: `http://localhost:8000/docs`
-- **ReDoc**: `http://localhost:8000/redoc`
-
-## 🧠 Model Integration
-
-### Step 1: Prepare Your Model File
-
-Create a `models` directory in the backend folder:
-
-```bash
-mkdir -p backend/models
-```
-
-Copy your trained model to this directory. Supported formats:
-- TensorFlow/Keras: `.h5`, `.pb`
-- PyTorch: `.pt`, `.pth`
-- scikit-learn: `.pkl`, `.joblib`
-- ONNX: `.onnx`
-
-Example:
-```bash
-cp path/to/your/pneumonia_model.h5 backend/models/
-```
-
-### Step 2: Update Requirements
-
-Add your ML framework to `backend/requirements.txt`:
-
-```text
-# For TensorFlow:
-tensorflow==2.14.0
-
-# For PyTorch:
-torch==2.1.0
-
-# For scikit-learn:
-scikit-learn==1.3.2
-```
-
-Then reinstall:
-```bash
-pip install -r requirements.txt
-```
-
-### Step 3: Update model_loader.py
-
-Edit `backend/services/model_loader.py` and replace the placeholder functions:
-
-#### Example 1: TensorFlow/Keras Model
-
-```python
-import tensorflow as tf
-
-def load_model():
-    """Load TensorFlow/Keras model"""
-    try:
-        model = tf.keras.models.load_model('backend/models/pneumonia_model.h5')
-        logger.info("TensorFlow model loaded successfully")
-        return model
-    except Exception as e:
-        logger.error(f"Failed to load model: {str(e)}")
-        raise
-
-def predict(model, preprocessed_images):
-    """Run inference with TensorFlow model"""
-    try:
-        predictions = model.predict(preprocessed_images)
-        results = []
-        
-        for pred in predictions:
-            prob = pred[0] if isinstance(pred, (list, np.ndarray)) else pred
-            
-            results.append({
-                "prediction": "Pneumonia" if prob > 0.5 else "Normal",
-                "confidence": float(max(prob, 1-prob) * 100),
-                "probability_normal": float(1 - prob),
-                "probability_pneumonia": float(prob)
-            })
-        
-        return results
-    except Exception as e:
-        logger.error(f"Prediction failed: {str(e)}")
-        raise
-```
-
-#### Example 2: PyTorch Model
-
-```python
-import torch
-import torch.nn.functional as F
-
-def load_model():
-    """Load PyTorch model"""
-    try:
-        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
-        model = torch.load('backend/models/pneumonia_model.pt', map_location=device)
-        model.eval()
-        logger.info("PyTorch model loaded successfully")
-        return model
-    except Exception as e:
-        logger.error(f"Failed to load model: {str(e)}")
-        raise
-
-def predict(model, preprocessed_images):
-    """Run inference with PyTorch model"""
-    try:
-        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
-        tensor = torch.from_numpy(preprocessed_images).float().to(device)
-        
-        with torch.no_grad():
-            outputs = model(tensor)
-            probs = F.softmax(outputs, dim=1)
-        
-        results = []
-        for prob in probs:
-            pneumonia_prob = prob[1].item()
-            results.append({
-                "prediction": "Pneumonia" if pneumonia_prob > 0.5 else "Normal",
-                "confidence": float(pneumonia_prob * 100),
-                "probability_normal": float(prob[0].item()),
-                "probability_pneumonia": float(pneumonia_prob)
-            })
-        
-        return results
-    except Exception as e:
-        logger.error(f"Prediction failed: {str(e)}")
-        raise
-```
-
-#### Example 3: scikit-learn Model
-
-```python
-import pickle
-
-def load_model():
-    """Load scikit-learn model"""
-    try:
-        with open('backend/models/pneumonia_model.pkl', 'rb') as f:
-            model = pickle.load(f)
-        logger.info("scikit-learn model loaded successfully")
-        return model
-    except Exception as e:
-        logger.error(f"Failed to load model: {str(e)}")
-        raise
-
-def predict(model, preprocessed_images):
-    """Run inference with scikit-learn model"""
-    try:
-        predictions = model.predict(preprocessed_images)
-        probabilities = model.predict_proba(preprocessed_images)
-        
-        results = []
-        for pred, prob in zip(predictions, probabilities):
-            results.append({
-                "prediction": "Pneumonia" if pred == 1 else "Normal",
-                "confidence": float(max(prob) * 100),
-                "probability_normal": float(prob[0]),
-                "probability_pneumonia": float(prob[1])
-            })
-        
-        return results
-    except Exception as e:
-        logger.error(f"Prediction failed: {str(e)}")
-        raise
-```
-
-### Step 4: Update Preprocessing Pipeline
-
-Edit `backend/utils/preprocess.py` to match your model's training preprocessing:
-
-```python
-# Update these configuration values to match your training pipeline
-IMG_WIDTH = 224  # Your model's input width
-IMG_HEIGHT = 224  # Your model's input height
-IMG_CHANNELS = 1  # 1 for grayscale, 3 for RGB
-NORMALIZATION_MEAN = 0.5  # Your training data mean
-NORMALIZATION_STD = 0.5   # Your training data std
-
-# Update preprocessing functions if needed
-def normalize_image(image: np.ndarray, mean: float = NORMALIZATION_MEAN, std: float = NORMALIZATION_STD) -> np.ndarray:
-    # Your custom normalization logic
-    pass
-```
-
-## 📝 File Structure After Integration
-
-```
-backend/
-├── models/
-│   └── pneumonia_model.h5  # Your trained model
-├── main.py
-├── routes/
-│   └── predict.py
-├── services/
-│   └── model_loader.py     # Updated with your model
-├── utils/
-│   └── preprocess.py       # Updated with your preprocessing
-└── requirements.txt        # Updated with ML framework
-```
-
-## 🧪 Testing Your Setup
-
-### 1. Test Backend Server
-
-```bash
-# In Python shell or script
-import requests
-import json
-
-response = requests.get('http://localhost:8000/health')
-print(response.json())
-```
-
-### 2. Test with Sample Images
-
-```python
-import requests
-
-# Prepare files
-with open('sample_xray.jpg', 'rb') as f:
-    files = {'files': f}
-    response = requests.post('http://localhost:8000/api/predict', files=files)
-    print(response.json())
-```
-
-### 3. Check Configuration
-
-```bash
-curl http://localhost:8000/api/predict/config
-```
-
-## 🐛 Troubleshooting
-
-### Model Not Found
-```
-FileNotFoundError: Model file not found
-```
-**Solution:** Ensure your model file is in `backend/models/` directory
-
-### Module Import Error
-```
-ModuleNotFoundError: No module named 'tensorflow'
-```
-**Solution:** Install the required ML framework:
-```bash
-pip install tensorflow  # or torch, scikit-learn, etc.
-```
-
-### CUDA/GPU Issues
-```
-RuntimeError: CUDA out of memory
-```
-**Solution:** Use CPU or reduce batch size. In model loading:
-```python
-device = torch.device('cpu')  # Force CPU
-```
-
-### Image Preprocessing Error
-```
-ValueError: Cannot reshape array
-```
-**Solution:** Check image dimensions match your model's input size
-
-## 📊 Performance Optimization
-
-### Enable GPU Support
-
-For TensorFlow:
-```bash
-pip install tensorflow-gpu
-```
-
-For PyTorch:
-```bash
-pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
-```
-
-### Batch Processing
-
-The system supports up to 10 images per request. Larger batches are more efficient:
-
-```python
-# Optimal: Process 8-10 images at once
-# Avoid: Sending 1-2 images repeatedly
-```
-
-## 🔒 Security Best Practices
-
-1. **Validate Input**: Already implemented in `routes/predict.py`
-2. **Limit File Size**: Maximum 10 MB per file (configurable)
-3. **Sanitize Paths**: Never trust user-provided file paths
-4. **Error Handling**: Never expose model details in error messages
-
-## 📈 Monitoring
-
-### View Logs
-
-```bash
-# Backend logs are printed to console
-# For file logging, add to main.py:
-logging.basicConfig(
-    filename='backend.log',
-    level=logging.INFO
-)
-```
-
-### Performance Metrics
-
-Add to your model_loader.py:
-```python
-import time
-
-def predict(model, preprocessed_images):
-    start_time = time.time()
-    results = model.predict(preprocessed_images)
-    inference_time = time.time() - start_time
-    logger.info(f"Inference took {inference_time:.2f}s for {len(preprocessed_images)} images")
-    return results
-```
-
-## 🚀 Production Deployment
-
-See [DEPLOYMENT.md](../DEPLOYMENT.md) for production setup.
-
-## 📞 Support
-
-For issues specific to your model:
-1. Check model compatibility
-2. Verify preprocessing matches training
-3. Ensure model file format is correct
-4. Check framework version compatibility
diff --git a/backend/PYTORCH_MODEL_INTEGRATION.md b/backend/PYTORCH_MODEL_INTEGRATION.md
deleted file mode 100644
index 57c016f..0000000
--- a/backend/PYTORCH_MODEL_INTEGRATION.md
+++ /dev/null
@@ -1,144 +0,0 @@
-# PyTorch Model Integration - SYNAPSE-X
-
-## Overview
-Successfully integrated the PyTorch neural network model (`best_model.pth`) into the SYNAPSE-X pneumonia detection backend.
-
-## Files Modified
-
-### 1. **requirements.txt**
-- ✅ Uncommented `torch==2.1.0` to enable PyTorch support
-- Model will be installed as a dependency
-
-### 2. **services/xray_model.py**
-Major updates:
-- ✅ Added PyTorch imports (`torch`, `torch.nn`)
-- ✅ Created `PyTorchPneumoniaClassifier` class that:
-  - Loads the trained model from disk
-  - Converts grayscale images to 3-channel format for the model
-  - Normalizes images to 0-1 range
-  - Performs inference with proper tensor handling
-  - Returns structured predictions with probabilities
-- ✅ Updated `PneumoniaClassifier` to support both:
-  - PyTorch neural network (primary)
-  - Feature-based classification (fallback)
-- ✅ Modified `PneumoniaDetectionPipeline` to:
-  - Accept model path parameter
-  - Automatically find model at `backend/models/best_model.pth`
-  - Use PyTorch classification when available
-- ✅ Updated `init_pipeline()` to load model automatically
-- ✅ Updated `detect_pneumonia()` to support model path parameter
-
-### 3. **services/model_loader.py**
-- ✅ Updated `ModelWrapper.__init__()` to load PyTorch model
-- ✅ Added `_load_pipeline()` method for proper initialization
-- ✅ Enhanced logging to show model status
-- ✅ Updated `load_model()` to initialize with PyTorch support
-- ✅ Maintains backward compatibility with existing API
-
-### 4. **test_model.py**
-- ✅ Added comprehensive test suite with:
-  - `test_model_loading()` - Verifies model loads correctly
-  - `test_model_with_synthetic_images()` - Tests inference on synthetic X-rays
-  - `test_batch_prediction()` - Tests batch processing
-  - Detailed logging and results reporting
-
-## Model File
-
-### Location
-- **Path**: `backend/models/best_model.pth`
-- **Source**: `c:\Users\BIT\OneDrive\Desktop\minor_proj\best_model.pth`
-- **Status**: ✅ Copied to backend
-
-### Expected Architecture
-The model should have:
-- Input: 3-channel images (256×256) or similar resolution
-- Output: 2-class classification (Normal/Pneumonia) with softmax
-- Preprocessing: Handles normalized float tensors [0, 1]
-
-## How It Works
-
-### Pipeline Flow
-1. **Image Loading** - Converts bytes to grayscale numpy array
-2. **Preprocessing** - Normalizes, resizes (256×256), applies CLAHE, denoise
-3. **Classification** - Two modes:
-   - **PyTorch Mode (Preferred)**: Passes preprocessed image to neural network
-   - **Feature Mode (Fallback)**: Extracts traditional CV features
-4. **Output** - Structured prediction with:
-   - `prediction`: "Normal" or "Affected"
-   - `confidence`: 0-100%
-   - `probability_normal`: 0-100%
-   - `probability_pneumonia`: 0-100%
-
-### Preprocessing
-- Grayscale image → float32 (0-1 range)
-- Repeat across RGB channels (grayscale → 3-channel)
-- Add batch dimension
-- Convert to PyTorch tensor on appropriate device (GPU/CPU)
-
-## Device Support
-- ✅ Automatically detects CUDA GPU if available
-- ✅ Falls back to CPU if GPU not available
-- ✅ Efficient memory usage with inference mode (`torch.no_grad()`)
-
-## Testing
-
-### Run Tests
-```bash
-cd backend
-python test_model.py
-```
-
-### Expected Output
-- Model loading verification
-- Synthetic image inference results
-- Batch prediction results
-- Overall test summary
-
-## Configuration
-
-### Manual Model Loading
-If needed to specify a different model path:
-```python
-from services.xray_model import init_pipeline
-pipeline = init_pipeline(model_path="/path/to/model.pth")
-```
-
-### Model Fallback Behavior
-- If PyTorch model fails to load, system automatically falls back to feature-based classification
-- Feature-based mode ensures 100% uptime
-- Logs clearly indicate which mode is active
-
-## API Compatibility
-- ✅ No changes to existing `/api/predict` endpoint
-- ✅ Seamless integration with existing frontend
-- ✅ Backward compatible with all routes
-- ✅ Automatic model initialization on first request
-
-## Dependencies Added
-- `torch==2.1.0` - PyTorch framework for neural network inference
-
-## Future Improvements
-- [ ] Add model versioning system
-- [ ] Implement model hot-swapping without restart
-- [ ] Add performance metrics logging
-- [ ] Support for different model architectures
-- [ ] Batch inference optimization
-
-## Troubleshooting
-
-### Model not found
-- Verify `backend/models/best_model.pth` exists
-- Check file permissions
-- Ensure model is valid PyTorch format
-
-### Out of Memory
-- Model will fallback to CPU automatically
-- Consider reducing batch size for very large models
-
-### Slow inference
-- Check if GPU is available and PyTorch is using it
-- Verify image preprocessing isn't bottleneck
-- Consider model optimization/quantization
-
-## Status
-✅ **Integration Complete** - PyTorch model is fully integrated and ready for deployment
diff --git a/backend/XRAY_MODEL_INTEGRATION.md b/backend/XRAY_MODEL_INTEGRATION.md
deleted file mode 100644
index 25b88ad..0000000
--- a/backend/XRAY_MODEL_INTEGRATION.md
+++ /dev/null
@@ -1,235 +0,0 @@
-# SYNAPSE-X Model Integration Guide
-
-Your X-Ray pneumonia detection model from `xray2.ipynb` has been successfully integrated into SYNAPSE-X!
-
-## What's Integrated
-
-### From Your Notebook (xray2.ipynb)
-✅ **Image Preprocessing Pipeline**
-- Image loading (JPEG, PNG, DICOM)
-- CLAHE contrast enhancement
-- Bilateral filtering for denoising
-- Normalization
-
-✅ **Lung Segmentation**
-- Adaptive thresholding for body detection
-- Percentile-based lung region detection
-- Morphological cleanup (opening, closing)
-- Connected component analysis
-- Anatomical filtering (removes spine, heart, borders)
-
-✅ **Feature Extraction**
-- Intensity statistics (mean, std, min, max)
-- Histogram analysis
-- Edge/texture features (Sobel operator)
-- Lung coverage ratio
-
-✅ **Pneumonia Classification**
-- Feature-based scoring system
-- Confidence calculation
-- Probability outputs
-
-## File Structure
-
-```
-backend/
-├── services/
-│   ├── model_loader.py      ← Updated to use xray_model
-│   └── xray_model.py        ← NEW: Your model integration
-├── routes/
-│   └── predict.py           ← Updated to pass raw bytes
-└── requirements.txt         ← Added opencv-python, scipy
-```
-
-## Setup Instructions
-
-### 1. Install Dependencies
-```bash
-cd backend
-pip install -r requirements.txt
-```
-
-**New packages added:**
-- `opencv-python==4.8.1.78` - Image processing (from your notebook)
-- `scipy==1.11.4` - Scientific computing for segmentation
-
-### 2. Start the Backend Server
-```bash
-cd backend
-python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
-```
-
-You should see output like:
-```
-✓ SYNAPSE-X Model loaded successfully
-  - Preprocessing: Image enhancement, resizing, denoising
-  - Segmentation: Lung extraction using adaptive thresholding
-  - Classification: Feature-based pneumonia detection
-```
-
-### 3. Test the Model
-
-**Using cURL:**
-```bash
-curl -X POST http://localhost:8000/api/predict \
-  -F "files=@/path/to/xray.png" \
-  -F "files=@/path/to/xray2.jpg"
-```
-
-**Using Python:**
-```python
-import requests
-
-files = [
-    ('files', open('/path/to/xray1.png', 'rb')),
-    ('files', open('/path/to/xray2.png', 'rb'))
-]
-
-response = requests.post('http://localhost:8000/api/predict', files=files)
-predictions = response.json()
-
-for pred in predictions:
-    print(f"{pred['filename']}: {pred['prediction']} ({pred['confidence']:.1f}%)")
-```
-
-## API Response Format
-
-```json
-[
-  {
-    "filename": "xray1.png",
-    "prediction": "Pneumonia",
-    "confidence": 78.5,
-    "probability_normal": 0.215,
-    "probability_pneumonia": 0.785,
-    "status": "success"
-  }
-]
-```
-
-## How The Model Works
-
-### Step 1: Image Loading
-- Accepts JPG, JPEG, PNG formats
-- Converts to grayscale
-- Handles multiple images in one request
-
-### Step 2: Preprocessing
-```
-Original Image → CLAHE Enhancement → Bilateral Denoising → Resizing
-```
-- CLAHE improves contrast
-- Bilateral filter preserves edges while reducing noise
-- Resizes to 256x256 for consistent processing
-
-### Step 3: Lung Segmentation
-```
-Enhanced Image → Body Detection → Lung Region Detection → Connected Components → Morphological Cleanup
-```
-
-1. **Body Detection**: Find non-black pixels (body boundary)
-2. **Lung Detection**: Find bright regions within body (lungs are bright)
-3. **Component Analysis**: Identify largest two components (left & right lung)
-4. **Anatomical Filtering**: Remove edges, spine, heart areas
-5. **Morphological Cleanup**: Smooth mask using opening/closing operations
-
-### Step 4: Feature Extraction
-Extracts from segmented lungs:
-- Mean/std pixel intensity
-- Histogram statistics
-- Edge intensity (Sobel gradients)
-- Lung coverage percentage
-
-### Step 5: Classification
-Pneumonia scoring:
-- Lower intensity → +0.15 to score
-- High std deviation → +0.10
-- High edge intensity → +0.20
-- Final score determines probability
-
-## Customization
-
-### Adjust Segmentation Sensitivity
-
-Edit `backend/services/xray_model.py`, in the `LungSegmentor.segment_lungs()` method:
-
-```python
-# Adjust percentile threshold (lower = more aggressive)
-threshold = np.percentile(body_pixels, 40)  # Change 40 to 30-50
-
-# Adjust component area size filter (in percents)
-if (8 < area_pct < 35 and ...  # Change 8-35 range
-```
-
-### Adjust Classification Thresholds
-
-Edit `backend/services/xray_model.py`, in `PneumoniaClassifier.__init__()`:
-
-```python
-self.intensity_threshold = 80      # Lower = more pneumonia detections
-self.edge_threshold = 15           # Higher = more pneumonia detections
-```
-
-### Add Your Own Model
-
-To replace the feature-based classifier with a trained deep learning model:
-
-1. Train your model (TensorFlow/PyTorch) on chest X-ray dataset
-2. Replace the `PneumoniaClassifier.classify()` method with your model
-3. Keep the same return format (prediction, confidence, probabilities)
-
-Example:
-```python
-class PneumoniaClassifier:
-    def __init__(self):
-        # Load your trained model
-        import tensorflow as tf
-        self.model = tf.keras.models.load_model('models/pneumonia_classifier.h5')
-    
-    def classify(self, features):
-        # Convert features to model input
-        # Get model predictions
-        # Return standardized format
-```
-
-## Performance Notes
-
-- **Speed**: ~100-200ms per image on CPU
-- **Accuracy**: Feature-based approach ~70-80% (baseline)
-- **Improvement**: Add trained deep learning model for 95%+ accuracy
-
-## Next Steps
-
-1. ✅ Integrated preprocessing from xray2.ipynb
-2. ✅ Integrated lung segmentation (traditional CV)
-3. ✅ Created feature-based classifier
-4. ⏭️ **Optional**: Train/integrate your deep learning model for better accuracy
-5. ⏭️ **Optional**: Fine-tune segmentation parameters on your dataset
-6. ⏭️ **Optional**: Collect more data for feature-based classifier training
-
-## Troubleshooting
-
-### Model not loading
-- Check `requirements.txt` installed: `pip install -r requirements.txt`
-- Verify OpenCV works: `python -c "import cv2; print(cv2.__version__)"`
-
-### Poor predictions on your X-rays
-- **Option 1**: Adjust segmentation thresholds (see Customization)
-- **Option 2**: Retrain with feature-based classifier on your data
-- **Option 3**: Integrate deep learning model (U-Net, ResNet, etc.)
-
-### Images not segmenting properly
-- Adjust contrast thresholds in `ImagePreprocessor` or `LungSegmentor`
-- Try different percentile values for lung detection
-- Add image visualization to debug segmentation
-
-## Support
-
-If you need to integrate a different model format or add more preprocessing:
-- All code is modular in `backend/services/xray_model.py`
-- Easy to extend with new preprocessing steps
-- Keep the same API contract (image bytes in, predictions out)
-
----
-
-**SYNAPSE-X** - AI-Powered Chest X-Ray Screening for Pneumonia Detection
diff --git a/backend/main.py b/backend/main.py
index 454d017..6a22c6e 100644
--- a/backend/main.py
+++ b/backend/main.py
@@ -1,5 +1,5 @@
 """
-SYNAPSE-X backend API.
+PulmoNet backend API.
 
 The API loads the pneumonia model once on startup, exposes structured
 inference endpoints, and centralizes request/error logging.
@@ -24,7 +24,7 @@ logging.basicConfig(
 logger = logging.getLogger(__name__)
 
 app = FastAPI(
-    title="SYNAPSE-X API",
+    title="PulmoNet API",
     description="AI-powered chest X-ray screening for pneumonia detection",
     version="1.0.0",
 )
@@ -62,7 +62,7 @@ async def request_logging_middleware(request: Request, call_next):
 
 @app.on_event("startup")
 async def startup_event():
-    logger.info("Starting SYNAPSE-X backend")
+    logger.info("Starting PulmoNet backend")
     try:
         get_model()
         if os.getenv("MODEL_WARMUP", "true").lower() == "true":
@@ -77,7 +77,7 @@ async def health_check():
     return {
         "success": True,
         "status": "running",
-        "service": "SYNAPSE-X API",
+        "service": "PulmoNet API",
         "model": model.metadata(),
     }
 
@@ -86,7 +86,7 @@ async def health_check():
 async def root():
     return {
         "success": True,
-        "name": "SYNAPSE-X",
+        "name": "PulmoNet",
         "tagline": "AI-powered chest X-ray screening for pneumonia detection",
         "version": "1.0.0",
         "endpoints": {
diff --git a/backend/requirements.txt b/backend/requirements.txt
index d26e72e..5492209 100644
--- a/backend/requirements.txt
+++ b/backend/requirements.txt
@@ -1,4 +1,4 @@
-# SYNAPSE-X Backend Requirements
+# PulmoNet Backend Requirements
 # All Python packages needed for the backend API.
 
 # Web Framework
diff --git a/backend/routes/predict.py b/backend/routes/predict.py
index 4f28959..faa7bdc 100644
--- a/backend/routes/predict.py
+++ b/backend/routes/predict.py
@@ -200,6 +200,6 @@ async def api_health_check():
     return {
         "success": True,
         "status": "running",
-        "service": "SYNAPSE-X API",
+        "service": "PulmoNet API",
         "model": model.metadata(),
     }
diff --git a/backend/services/model_loader.py b/backend/services/model_loader.py
index c8bdeba..2f40dd0 100644
--- a/backend/services/model_loader.py
+++ b/backend/services/model_loader.py
@@ -1,5 +1,5 @@
 """
-Model service for SYNAPSE-X.
+Model service for PulmoNet.
 
 The backend keeps one model wrapper in memory and reuses it for every request.
 The provided model file is a PyTorch checkpoint saved as ``best_model.pth``.
@@ -62,7 +62,7 @@ class ModelWrapper:
             if self.model_path and not Path(self.model_path).exists():
                 logger.warning(f"Model file not found at {self.model_path}; fallback classifier will be used")
 
-            logger.info(f"Loading SYNAPSE-X model from {self.model_path}")
+            logger.info(f"Loading PulmoNet model from {self.model_path}")
             self.pipeline = init_pipeline(model_path=self.model_path)
             self.is_loaded = self.pipeline is not None
             self.load_time_ms = round((time.perf_counter() - started_at) * 1000, 2)
diff --git a/backend/test_model.py b/backend/test_model.py
index 197efbd..c4ea07d 100644
--- a/backend/test_model.py
+++ b/backend/test_model.py
@@ -117,7 +117,7 @@ def test_batch_prediction():
 def main():
     """Run all tests"""
     print("\n" + "="*60)
-    print("SYNAPSE-X PyTorch Model Integration Tests")
+    print("PulmoNet PyTorch Model Integration Tests")
     print("="*60)
     
     results = []
diff --git a/backend/utils/preprocess.py b/backend/utils/preprocess.py
index aa03efb..e2e8ede 100644
--- a/backend/utils/preprocess.py
+++ b/backend/utils/preprocess.py
@@ -1,5 +1,5 @@
 """
-ANTIGRAVITY - Image Preprocessing Pipeline
+PulmoNet - Image Preprocessing Pipeline
 
 This module handles image preprocessing for pneumonia detection.
 
diff --git a/frontend/README.md b/frontend/README.md
deleted file mode 100644
index efd5829..0000000
--- a/frontend/README.md
+++ /dev/null
@@ -1,433 +0,0 @@
-# ANTIGRAVITY Frontend - React Setup Guide
-
-Professional React application with Tailwind CSS for medical AI platform.
-
-## 🎨 Technology Stack
-
-- **React 18.2** - UI library
-- **Vite** - Build tool
-- **Tailwind CSS** - Styling
-- **Fetch API** - HTTP requests
-
-## 🚀 Quick Start
-
-### Prerequisites
-- Node.js 16+
-- npm or yarn
-
-### Installation
-
-1. Navigate to frontend directory:
-```bash
-cd frontend
-```
-
-2. Install dependencies:
-```bash
-npm install
-```
-
-3. Create environment configuration:
-```bash
-echo "REACT_APP_API_URL=http://localhost:8000/api" > .env.local
-```
-
-4. Start development server:
-```bash
-npm run dev
-```
-
-Frontend will be available at `http://localhost:3000`
-
-## 📁 Project Structure
-
-```
-frontend/
-├── src/
-│   ├── components/              # React components
-│   │   ├── Navbar.jsx          # Navigation bar
-│   │   ├── Hero.jsx            # Hero section
-│   │   ├── UploadArea.jsx      # File upload
-│   │   ├── ImagePreviewCard.jsx # Image preview
-│   │   ├── PredictionCard.jsx  # Results display
-│   │   ├── LoadingSpinner.jsx  # Loading indicator
-│   │   ├── ErrorMessage.jsx    # Error display
-│   │   ├── HowItWorks.jsx      # Process section
-│   │   ├── Features.jsx        # Features section
-│   │   └── Footer.jsx          # Footer with disclaimer
-│   ├── services/
-│   │   └── apiService.js       # Backend API calls
-│   ├── App.jsx                 # Root component
-│   ├── index.jsx               # Entry point
-│   └── index.css               # Tailwind styles
-├── public/                     # Static files
-├── package.json               # Dependencies
-├── vite.config.js            # Vite config
-├── tailwind.config.js        # Tailwind config
-├── postcss.config.js         # PostCSS config
-└── index.html                # HTML entry
-```
-
-## 🧩 Component Overview
-
-### Navbar
-- Logo with branding
-- Navigation links
-- Sticky positioning
-- Responsive menu
-
-### Hero Section
-- Large headline
-- Subheadline
-- Call-to-action buttons
-- Feature statistics
-- Animated background
-
-### PredictionInterface
-- Two-column layout
-- Left: Upload area
-- Right: Results display
-- Handles file validation
-- Manages prediction state
-
-### UploadArea
-- Drag-and-drop zone
-- File input
-- Visual feedback
-- Format validation
-
-### PredictionCard
-- Image preview
-- Prediction result
-- Confidence score
-- Probability bars
-- Status badge
-
-### LoadingSpinner
-- Animated spinner
-- Size variants
-- Smooth animation
-
-### ErrorMessage
-- Error display
-- Dismissible
-- User-friendly text
-- Alert styling
-
-### HowItWorks
-- 3-step process
-- Animated cards
-- Process diagram
-
-### Features
-- Feature cards
-- Icon display
-- Responsive grid
-
-### Footer
-- Medical disclaimer
-- Links
-- Copyright
-- Social media
-
-## 🎨 Styling
-
-### Tailwind CSS
-
-Custom colors defined in `tailwind.config.js`:
-```javascript
-colors: {
-  'medical-red': '#ef4444',
-  'medical-green': '#10b981',
-  'medical-blue': '#0ea5e9',
-}
-```
-
-Custom animations:
-- `fadeInUp` - Fade in with upward movement
-- `shimmer` - Skeleton loading animation
-- `pulse-ring` - Pulsing ring effect
-
-### Custom Styles
-
-Defined in `src/index.css`:
-```css
-.card-medical { /* Medical card styling */ }
-.btn-primary { /* Primary button */ }
-.btn-secondary { /* Secondary button */ }
-.badge-pneumonia { /* Pneumonia badge */ }
-.badge-normal { /* Normal badge */ }
-```
-
-## 🔌 API Integration
-
-### apiService.js Functions
-
-```javascript
-submitPrediction(files)  // POST /predict
-getPredictionConfig()    // GET /predict/config
-healthCheck()            // GET /health
-```
-
-### Usage Example
-
-```javascript
-import { submitPrediction } from '../services/apiService';
-
-const handlePredict = async (files) => {
-  try {
-    const results = await submitPrediction(files);
-    console.log(results);
-  } catch (error) {
-    console.error('Prediction failed:', error);
-  }
-};
-```
-
-## 📱 Responsive Design
-
-### Breakpoints
-
-```css
-/* Mobile first */
-.component { /* Mobile styles */ }
-
-/* Tablet */
-@media (min-width: 768px) { /* md */ }
-
-/* Desktop */
-@media (min-width: 1024px) { /* lg */ }
-
-/* Large desktop */
-@media (min-width: 1280px) { /* xl */ }
-```
-
-### Mobile Optimization
-
-- Stack columns vertically on mobile
-- Touch-friendly buttons (48px minimum)
-- Readable font sizes
-- Adequate spacing
-- Optimized images
-
-## 🔨 Build & Deploy
-
-### Development
-
-```bash
-npm run dev
-```
-
-### Production Build
-
-```bash
-npm run build
-```
-
-Output directory: `dist/`
-
-### Preview Build
-
-```bash
-npm run preview
-```
-
-### Environment Variables
-
-Create `.env.local`:
-```
-REACT_APP_API_URL=http://localhost:8000/api
-```
-
-Or for production:
-```
-REACT_APP_API_URL=https://api.antigravity.com
-```
-
-## 📦 Dependencies
-
-Core dependencies:
-- `react@^18.2.0`
-- `react-dom@^18.2.0`
-
-Dev dependencies:
-- `vite@^5.0.0`
-- `@vitejs/plugin-react@^4.2.0`
-- `tailwindcss@^3.3.6`
-- `postcss@^8.4.31`
-- `autoprefixer@^10.4.16`
-
-## 🚀 Performance
-
-### Code Splitting
-
-Vite automatically handles code splitting for:
-- Vendor libraries
-- Individual routes (if using React Router)
-- Lazy-loaded components
-
-### Image Optimization
-
-Images in components are:
-- Lazy-loaded
-- Responsive
-- Compressed
-- In modern formats
-
-### Caching
-
-- Service worker ready (add if needed)
-- Static asset caching
-- Browser caching headers
-
-## 🧪 Testing
-
-To add testing (not included by default):
-
-```bash
-npm install --save-dev vitest @testing-library/react
-```
-
-## 🔒 Security
-
-- No sensitive data in client-side code
-- All API requests HTTPS in production
-- CSRF protection (handled by backend)
-- Content Security Policy recommended
-
-## 📊 Browser Support
-
-- Chrome (latest)
-- Firefox (latest)
-- Safari (latest)
-- Edge (latest)
-
-## 🐛 Troubleshooting
-
-### Port Already in Use
-
-```bash
-npm run dev -- --port 3001
-```
-
-### API Connection Error
-
-Check `.env.local`:
-```
-REACT_APP_API_URL=http://localhost:8000/api
-```
-
-Backend must be running on port 8000.
-
-### Build Errors
-
-```bash
-rm -rf node_modules package-lock.json
-npm install
-npm run build
-```
-
-### CORS Issues
-
-Frontend: `http://localhost:3000`
-Backend: `http://localhost:8000`
-
-Backend CORS configured in `main.py`:
-```python
-allow_origins=["*"]
-```
-
-Update for production domains.
-
-## 📚 Component Usage
-
-### Basic Example
-
-```jsx
-import PredictionInterface from './components/PredictionInterface';
-
-function App() {
-  return <PredictionInterface />;
-}
-```
-
-### With Error Handling
-
-```jsx
-import ErrorMessage from './components/ErrorMessage';
-
-function MyComponent() {
-  const [error, setError] = useState(null);
-
-  return (
-    <>
-      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}
-      {/* Component content */}
-    </>
-  );
-}
-```
-
-## 🚀 Deployment Options
-
-### Netlify
-
-```bash
-npm run build
-# Deploy dist/ folder to Netlify
-```
-
-### Vercel
-
-```bash
-npm install -g vercel
-vercel --prod
-```
-
-### AWS S3 + CloudFront
-
-```bash
-npm run build
-aws s3 sync dist/ s3://bucket-name/
-```
-
-### GitHub Pages
-
-```bash
-npm run build
-git push origin main
-```
-
-## 📈 Performance Metrics
-
-- **Build time**: ~2-3 seconds
-- **Bundle size**: ~150KB (gzipped)
-- **First contentful paint**: < 1s
-- **Time to interactive**: < 2s
-
-## 🔄 State Management
-
-Current implementation uses React hooks:
-- `useState` - Local state
-- `useEffect` - Side effects
-- `useRef` - DOM references
-
-For complex state, consider:
-- Redux
-- Zustand
-- Recoil
-
-## 📞 Support
-
-For frontend issues:
-1. Check browser console for errors
-2. Verify environment variables
-3. Ensure backend is running
-4. Clear browser cache
-5. Check API endpoint configuration
-
----
-
-For backend setup, see [SETUP.md](../SETUP.md)
-For API documentation, see [API_DOCS.md](../API_DOCS.md)
-For deployment, see [DEPLOYMENT.md](../DEPLOYMENT.md)
diff --git a/frontend/index.html b/frontend/index.html
index 6f823ee..be44706 100644
--- a/frontend/index.html
+++ b/frontend/index.html
@@ -4,8 +4,8 @@
     <meta charset="UTF-8" />
     <link rel="icon" type="image/svg+xml" href="/logo.svg" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
-    <meta name="description" content="SYNAPSE-X - AI-powered chest X-ray screening for pneumonia detection" />
-    <title>SYNAPSE-X - Pneumonia Detection AI</title>
+    <meta name="description" content="PulmoNet - AI-powered chest X-ray screening for pneumonia detection" />
+    <title>PulmoNet - Pneumonia Detection AI</title>
   </head>
   <body>
     <div id="root"></div>
diff --git a/frontend/package.json b/frontend/package.json
index 361b9f9..ae1fb81 100644
--- a/frontend/package.json
+++ b/frontend/package.json
@@ -1,8 +1,8 @@
 {
-  "name": "synapse-x-frontend",
+  "name": "pulmonet-frontend",
   "version": "1.0.0",
   "type": "module",
-  "description": "SYNAPSE-X - AI-Powered Pneumonia Detection Frontend",
+  "description": "PulmoNet - AI-Powered Pneumonia Detection Frontend",
   "main": "src/index.jsx",
   "scripts": {
     "dev": "vite",
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index 72a1818..510d28b 100644
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1,5 +1,5 @@
 /**
- * SYNAPSE-X Frontend
+ * PulmoNet Frontend
  */
 
 import React, { useEffect } from 'react';
diff --git a/frontend/src/components/Footer.jsx b/frontend/src/components/Footer.jsx
index 6039ccd..d8b72ff 100644
--- a/frontend/src/components/Footer.jsx
+++ b/frontend/src/components/Footer.jsx
@@ -20,7 +20,7 @@ export default function Footer() {
                 <span className="text-white font-bold">X</span>
               </div>
               <div>
-                <h3 className="font-bold text-white">SYNAPSE-X</h3>
+                <h3 className="font-bold text-white">PulmoNet</h3>
                 <p className="text-xs">AI Pneumonia Detection</p>
               </div>
             </div>
@@ -44,7 +44,7 @@ export default function Footer() {
             <ul className="space-y-2 text-sm">
               <li><button onClick={() => alert('About page coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">About</button></li>
               <li><button onClick={() => alert('Blog coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Blog</button></li>
-              <li><button onClick={() => alert('Contact us at info@synapse-x.ai')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Contact</button></li>
+              <li><button onClick={() => window.open('https://github.com/variablePotato/PulmoNet/issues', '_blank')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Contact</button></li>
               <li><button onClick={() => alert('Careers page coming soon!')} className="hover:text-white transition-colors bg-none border-none cursor-pointer">Careers</button></li>
             </ul>
           </div>
@@ -63,7 +63,7 @@ export default function Footer() {
         <div className="border-t border-slate-800 pt-12">
           <div className="bg-blue-900/30 border border-blue-700/30 rounded-lg p-4 mb-8">
             <p className="text-xs text-slate-300 leading-relaxed">
-              <strong>Medical Disclaimer:</strong> SYNAPSE-X is an AI-assisted screening tool designed to support radiologists and healthcare professionals. 
+              <strong>Medical Disclaimer:</strong> PulmoNet is an AI-assisted screening tool designed to support radiologists and healthcare professionals. 
               It is not a substitute for professional medical diagnosis, treatment, or advice. Always consult qualified healthcare professionals for medical decisions. 
               Results should be interpreted in clinical context by licensed medical practitioners.
             </p>
@@ -71,10 +71,10 @@ export default function Footer() {
 
           <div className="flex flex-col sm:flex-row justify-between items-center">
             <p className="text-sm text-slate-400">
-              © {currentYear} SYNAPSE-X. All rights reserved.
+              © {currentYear} PulmoNet. All rights reserved.
             </p>
             <div className="flex items-center gap-6 mt-4 sm:mt-0">
-              <button onClick={() => alert('Twitter: @SYNAPSE_X')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">Twitter</button>
+              <button onClick={() => window.open('https://github.com/variablePotato/PulmoNet', '_blank')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">GitHub</button>
               <button onClick={() => alert('GitHub: coming soon')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">GitHub</button>
               <button onClick={() => alert('LinkedIn: coming soon')} className="text-slate-400 hover:text-white transition-colors bg-none border-none cursor-pointer">LinkedIn</button>
             </div>
diff --git a/frontend/src/components/Hero.jsx b/frontend/src/components/Hero.jsx
index fe09b2d..e555b97 100644
--- a/frontend/src/components/Hero.jsx
+++ b/frontend/src/components/Hero.jsx
@@ -172,7 +172,7 @@ export default function Hero() {
                       <div className="absolute inset-0 bg-gradient-to-br from-slate-900 to-blue-900 p-4 flex flex-col justify-between">
                         {/* Screen header */}
                         <div className="text-xs text-cyan-400 font-mono mb-2">
-                          <p>SYNAPSE-X ANALYSIS v1.0</p>
+                          <p>PULMONET ANALYSIS v1.0</p>
                           <p className="text-green-400">&gt; Status: COMPLETE</p>
                         </div>
 
diff --git a/frontend/src/components/Navbar.jsx b/frontend/src/components/Navbar.jsx
index 2ee3638..f798e25 100644
--- a/frontend/src/components/Navbar.jsx
+++ b/frontend/src/components/Navbar.jsx
@@ -26,7 +26,7 @@ export default function Navbar() {
               <span className="text-white font-bold text-lg">X</span>
             </div>
             <div>
-              <h1 className="text-xl font-bold text-slate-900">SYNAPSE-X</h1>
+              <h1 className="text-xl font-bold text-slate-900">PulmoNet</h1>
               <p className="text-xs text-slate-500">Pneumonia Detection</p>
             </div>
           </div>
diff --git a/frontend/src/index.css b/frontend/src/index.css
index cf67787..6594b5f 100644
--- a/frontend/src/index.css
+++ b/frontend/src/index.css
@@ -1,6 +1,6 @@
 /**
  * Tailwind CSS Configuration
- * Custom styles for SYNAPSE-X medical AI platform
+ * Custom styles for PulmoNet medical AI platform
  */
 
 @import 'tailwindcss/base';
-- 
2.43.0
