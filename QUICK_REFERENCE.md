# ANTIGRAVITY - Quick Reference Card

## ⚡ Start in 30 Seconds

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

**URLs**:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Swagger Docs: http://localhost:8000/docs

---

## 🧠 Integrate Your Model (3 Steps)

1. **Copy Model**
   ```bash
   cp your_model.h5 backend/models/
   ```

2. **Update `backend/services/model_loader.py`**
   ```python
   import tensorflow as tf
   
   def load_model():
       return tf.keras.models.load_model('backend/models/your_model.h5')
   
   def predict(model, preprocessed_images):
       preds = model.predict(preprocessed_images)
       # Format to expected output...
   ```

3. **Install ML Framework**
   ```bash
   pip install tensorflow  # or torch, scikit-learn
   pip install -r requirements.txt
   ```

See [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) for complete examples.

---

## 📊 API Usage

### Test Prediction
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@image1.png" \
  -F "files=@image2.png"
```

### Response Format
```json
[
  {
    "filename": "image1.png",
    "prediction": "Pneumonia",
    "confidence": 96.4,
    "probability_normal": 0.036,
    "probability_pneumonia": 0.964,
    "status": "success"
  }
]
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI server |
| `backend/services/model_loader.py` | **UPDATE WITH YOUR MODEL** |
| `backend/utils/preprocess.py` | **CUSTOMIZE IF NEEDED** |
| `backend/routes/predict.py` | Prediction endpoint |
| `frontend/src/App.jsx` | React app root |
| `frontend/src/components/PredictionInterface.jsx` | Main UI |

---

## 🎯 Environment Setup

**Backend** `.env`:
```
MODEL_PATH=backend/models/pneumonia_model.h5
MODEL_TYPE=tensorflow
IMAGE_WIDTH=224
IMAGE_HEIGHT=224
```

**Frontend** `.env.local`:
```
REACT_APP_API_URL=http://localhost:8000/api
```

---

## ✅ Verification

```bash
# Backend health
curl http://localhost:8000/health
# Returns: {"status": "running"}

# Frontend loads
# Visit: http://localhost:3000

# Upload test image
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@test.png"
# Should return predictions
```

---

## 📚 Documentation

- **Overview**: [README.md](./README.md)
- **Setup**: [SETUP.md](./SETUP.md)
- **API**: [API_DOCS.md](./API_DOCS.md)
- **Model Integration**: [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md)
- **Deployment**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Frontend**: [frontend/README.md](./frontend/README.md)

---

## 🚀 Production Deployment

**Backend** (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

**Frontend** (Build & Deploy):
```bash
npm run build
# Deploy dist/ folder to:
# - Netlify
# - Vercel
# - AWS S3
# - GitHub Pages
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for details.

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` / `kill <PID>` |
| Port 3000 in use | `npm run dev -- --port 3001` |
| Module not found | `pip install -r requirements.txt` |
| CORS error | Check backend CORS config |
| Model not loading | Verify file path and format |
| Predictions wrong format | Check preprocessing + output |

---

## 🎨 Component Structure

```
Frontend/
├── Hero (Landing)
├── PredictionInterface
│   ├── Left: UploadArea
│   ├── Right: PredictionCard(s)
├── HowItWorks
├── Features
└── Footer (Medical Disclaimer)
```

---

## 📊 File Limits

- **Max files per batch**: 10
- **Max file size**: 10 MB
- **Supported formats**: JPG, JPEG, PNG

---

## 💡 Pro Tips

1. **Batch Processing**: Send max 10 images for efficiency
2. **Preprocessing**: Match training pipeline exactly
3. **Model Format**: Convert to checkpoint if needed
4. **GPU Support**: Install CUDA for faster inference
5. **Monitoring**: Add health checks to production

---

## ⚠️ Medical Disclaimer

This is an AI-assisted screening tool. 

- **Required for healthcare use**
- **Not a substitute for professional diagnosis**
- **Always review with qualified professionals**
- **Document all results**

---

## 🔗 Important Links

- **FastAPI Docs**: http://localhost:8000/docs
- **Vite Guide**: https://vitejs.dev/
- **React Guide**: https://react.dev/
- **Tailwind Guide**: https://tailwindcss.com/

---

## 📞 Common Tasks

### Add New Endpoint
Edit: `backend/routes/predict.py`

### Customize UI
Edit: `frontend/src/components/`

### Change Image Size
Edit: `backend/utils/preprocess.py`

### Update Branding
Edit: `frontend/src/components/Navbar.jsx`

### Modify Colors
Edit: `frontend/tailwind.config.js`

---

## ✨ What's Included

✅ Backend API (FastAPI)  
✅ Frontend UI (React)  
✅ Model Placeholder  
✅ Preprocessing Pipeline  
✅ Documentation (5 guides)  
✅ Error Handling  
✅ Responsive Design  
✅ Medical Disclaimer  
✅ Production Ready  

---

**Status**: ✅ Ready to Integrate Your Model  
**Current Version**: 1.0.0  
**Last Updated**: 2024
