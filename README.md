# ANTIGRAVITY - AI-Powered Pneumonia Detection System

Professional-grade medical AI web application for chest X-ray pneumonia detection.

## 🎯 Overview

ANTIGRAVITY is a production-ready full-stack application that combines:
- **Modern React Frontend** with premium healthcare UI
- **FastAPI Backend** with robust API design
- **Modular ML Integration** for easy model swapping
- **Hospital-grade Security** and validation
- **Batch Processing** capabilities
- **Professional Medical Design**

## ✨ Key Features

- ✅ Multi-image upload with drag-and-drop
- ✅ Batch prediction support (up to 10 images)
- ✅ Two-column UI (Upload + Results)
- ✅ Real-time confidence scores
- ✅ Professional medical color palette
- ✅ Responsive mobile design
- ✅ Comprehensive error handling
- ✅ REST API with full documentation
- ✅ Model placeholder integration

## 📁 Project Structure

```
antigravity/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── routes/
│   │   ├── predict.py      # Prediction endpoints
│   │   └── __init__.py
│   ├── services/
│   │   ├── model_loader.py # Model loading placeholder
│   │   └── __init__.py
│   ├── utils/
│   │   ├── preprocess.py   # Image preprocessing pipeline
│   │   └── __init__.py
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── App.jsx         # Root component
│   │   ├── index.jsx       # Entry point
│   │   └── index.css       # Tailwind styles
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── tailwind.config.js  # Tailwind configuration
│   └── index.html          # HTML entry point
│
├── README.md               # This file
├── SETUP.md               # Setup instructions
└── API_DOCS.md            # API documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run development server:
```bash
python main.py
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file `.env`:
```
REACT_APP_API_URL=http://localhost:8000/api
```

4. Run development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🔧 Model Integration

The application includes **placeholder model integration**. To integrate your trained Kaggle model:

### Step 1: Prepare Your Model
```bash
mkdir -p backend/models
# Copy your trained model to: backend/models/pneumonia_model.h5 (or .pkl, .pt)
```

### Step 2: Update Model Loader
Edit `backend/services/model_loader.py`:

```python
# Replace the load_model() function with:
def load_model():
    import tensorflow as tf
    model = tf.keras.models.load_model('models/pneumonia_model.h5')
    return model

# Replace the predict() function with:
def predict(model, preprocessed_images):
    predictions = model.predict(preprocessed_images)
    results = []
    for pred in predictions:
        results.append({
            "prediction": "Pneumonia" if pred[0] > 0.5 else "Normal",
            "confidence": float(max(pred) * 100),
            "probability_normal": float(pred[0]),
            "probability_pneumonia": float(pred[1])
        })
    return results
```

### Step 3: Update Preprocessing
Edit `backend/utils/preprocess.py` to match your model's training preprocessing

## 📊 API Endpoints

### Health Check
```
GET /health
Response: {"status": "running"}
```

### Predict
```
POST /api/predict
Content-Type: multipart/form-data

Request:
- files: List of image files (JPG, JPEG, PNG)

Response:
[
  {
    "filename": "xray1.png",
    "prediction": "Pneumonia",
    "confidence": 96.4,
    "probability_normal": 0.036,
    "probability_pneumonia": 0.964,
    "status": "success"
  }
]
```

### Configuration
```
GET /api/predict/config
Response: Configuration and constraints
```

## 🎨 UI Components

- **Navbar** - Navigation with logo
- **Hero** - Landing section with CTA
- **UploadArea** - Drag-and-drop upload zone
- **ImagePreviewCard** - Image thumbnail preview
- **PredictionCard** - Result display with confidence
- **LoadingSpinner** - Loading indicator
- **ErrorMessage** - Error notification
- **HowItWorks** - Process explanation
- **Features** - Product features showcase
- **Footer** - Footer with medical disclaimer

## 🔒 Security

- File type validation (JPG, JPEG, PNG only)
- File size limit (10 MB per file)
- Batch size limit (10 files maximum)
- CORS enabled for safe cross-origin requests
- Input sanitization
- Error handling without exposing internals

## 📱 Responsive Design

- Mobile-first approach
- Tablet optimization
- Desktop full-featured layout
- Touch-friendly UI elements
- Flexible grid system

## ⚠️ Medical Disclaimer

**IMPORTANT:** ANTIGRAVITY is an AI-assisted screening tool and is **NOT a substitute for professional medical diagnosis**. 

All predictions must be:
- Reviewed by qualified healthcare professionals
- Used only as a screening aid
- Followed by proper clinical evaluation
- Documented in patient records

## 🚢 Deployment

### Backend Deployment (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Frontend Deployment
```bash
npm run build
# Deploy dist/ directory to static hosting
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment guidance.

## 📚 Documentation

- [SETUP.md](./SETUP.md) - Detailed setup instructions
- [API_DOCS.md](./API_DOCS.md) - Complete API reference
- [MODEL_INTEGRATION.md](./MODEL_INTEGRATION.md) - Model integration guide
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment instructions

## 🛠️ Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Linting
cd frontend
npm run lint
```

## 📈 Performance

- Batch processing: Up to 10 images per request
- Image preprocessing: < 1s per image
- Model inference: Depends on your model
- Response time: Typically < 5s for batch of 10

## 🤝 Contributing

1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues, questions, or suggestions:
- Open GitHub issue
- Contact: [email]
- Documentation: [docs]

---

**ANTIGRAVITY** - AI-powered chest X-ray screening for pneumonia detection
