# ANTIGRAVITY Backend - Setup & Integration Guide

Complete guide for setting up and integrating your pneumonia detection model.

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

## 📦 Installation

### 1. Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -c "import fastapi; import uvicorn; print('All dependencies installed!')"
```

## 🚀 Running the Backend

### Development Mode

```bash
python main.py
```

Server will start at `http://localhost:8000`

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧠 Model Integration

### Step 1: Prepare Your Model File

Create a `models` directory in the backend folder:

```bash
mkdir -p backend/models
```

Copy your trained model to this directory. Supported formats:
- TensorFlow/Keras: `.h5`, `.pb`
- PyTorch: `.pt`, `.pth`
- scikit-learn: `.pkl`, `.joblib`
- ONNX: `.onnx`

Example:
```bash
cp path/to/your/pneumonia_model.h5 backend/models/
```

### Step 2: Update Requirements

Add your ML framework to `backend/requirements.txt`:

```text
# For TensorFlow:
tensorflow==2.14.0

# For PyTorch:
torch==2.1.0

# For scikit-learn:
scikit-learn==1.3.2
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### Step 3: Update model_loader.py

Edit `backend/services/model_loader.py` and replace the placeholder functions:

#### Example 1: TensorFlow/Keras Model

```python
import tensorflow as tf

def load_model():
    """Load TensorFlow/Keras model"""
    try:
        model = tf.keras.models.load_model('backend/models/pneumonia_model.h5')
        logger.info("TensorFlow model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

def predict(model, preprocessed_images):
    """Run inference with TensorFlow model"""
    try:
        predictions = model.predict(preprocessed_images)
        results = []
        
        for pred in predictions:
            prob = pred[0] if isinstance(pred, (list, np.ndarray)) else pred
            
            results.append({
                "prediction": "Pneumonia" if prob > 0.5 else "Normal",
                "confidence": float(max(prob, 1-prob) * 100),
                "probability_normal": float(1 - prob),
                "probability_pneumonia": float(prob)
            })
        
        return results
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

#### Example 2: PyTorch Model

```python
import torch
import torch.nn.functional as F

def load_model():
    """Load PyTorch model"""
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = torch.load('backend/models/pneumonia_model.pt', map_location=device)
        model.eval()
        logger.info("PyTorch model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

def predict(model, preprocessed_images):
    """Run inference with PyTorch model"""
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        tensor = torch.from_numpy(preprocessed_images).float().to(device)
        
        with torch.no_grad():
            outputs = model(tensor)
            probs = F.softmax(outputs, dim=1)
        
        results = []
        for prob in probs:
            pneumonia_prob = prob[1].item()
            results.append({
                "prediction": "Pneumonia" if pneumonia_prob > 0.5 else "Normal",
                "confidence": float(pneumonia_prob * 100),
                "probability_normal": float(prob[0].item()),
                "probability_pneumonia": float(pneumonia_prob)
            })
        
        return results
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

#### Example 3: scikit-learn Model

```python
import pickle

def load_model():
    """Load scikit-learn model"""
    try:
        with open('backend/models/pneumonia_model.pkl', 'rb') as f:
            model = pickle.load(f)
        logger.info("scikit-learn model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

def predict(model, preprocessed_images):
    """Run inference with scikit-learn model"""
    try:
        predictions = model.predict(preprocessed_images)
        probabilities = model.predict_proba(preprocessed_images)
        
        results = []
        for pred, prob in zip(predictions, probabilities):
            results.append({
                "prediction": "Pneumonia" if pred == 1 else "Normal",
                "confidence": float(max(prob) * 100),
                "probability_normal": float(prob[0]),
                "probability_pneumonia": float(prob[1])
            })
        
        return results
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

### Step 4: Update Preprocessing Pipeline

Edit `backend/utils/preprocess.py` to match your model's training preprocessing:

```python
# Update these configuration values to match your training pipeline
IMG_WIDTH = 224  # Your model's input width
IMG_HEIGHT = 224  # Your model's input height
IMG_CHANNELS = 1  # 1 for grayscale, 3 for RGB
NORMALIZATION_MEAN = 0.5  # Your training data mean
NORMALIZATION_STD = 0.5   # Your training data std

# Update preprocessing functions if needed
def normalize_image(image: np.ndarray, mean: float = NORMALIZATION_MEAN, std: float = NORMALIZATION_STD) -> np.ndarray:
    # Your custom normalization logic
    pass
```

## 📝 File Structure After Integration

```
backend/
├── models/
│   └── pneumonia_model.h5  # Your trained model
├── main.py
├── routes/
│   └── predict.py
├── services/
│   └── model_loader.py     # Updated with your model
├── utils/
│   └── preprocess.py       # Updated with your preprocessing
└── requirements.txt        # Updated with ML framework
```

## 🧪 Testing Your Setup

### 1. Test Backend Server

```bash
# In Python shell or script
import requests
import json

response = requests.get('http://localhost:8000/health')
print(response.json())
```

### 2. Test with Sample Images

```python
import requests

# Prepare files
with open('sample_xray.jpg', 'rb') as f:
    files = {'files': f}
    response = requests.post('http://localhost:8000/api/predict', files=files)
    print(response.json())
```

### 3. Check Configuration

```bash
curl http://localhost:8000/api/predict/config
```

## 🐛 Troubleshooting

### Model Not Found
```
FileNotFoundError: Model file not found
```
**Solution:** Ensure your model file is in `backend/models/` directory

### Module Import Error
```
ModuleNotFoundError: No module named 'tensorflow'
```
**Solution:** Install the required ML framework:
```bash
pip install tensorflow  # or torch, scikit-learn, etc.
```

### CUDA/GPU Issues
```
RuntimeError: CUDA out of memory
```
**Solution:** Use CPU or reduce batch size. In model loading:
```python
device = torch.device('cpu')  # Force CPU
```

### Image Preprocessing Error
```
ValueError: Cannot reshape array
```
**Solution:** Check image dimensions match your model's input size

## 📊 Performance Optimization

### Enable GPU Support

For TensorFlow:
```bash
pip install tensorflow-gpu
```

For PyTorch:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Batch Processing

The system supports up to 10 images per request. Larger batches are more efficient:

```python
# Optimal: Process 8-10 images at once
# Avoid: Sending 1-2 images repeatedly
```

## 🔒 Security Best Practices

1. **Validate Input**: Already implemented in `routes/predict.py`
2. **Limit File Size**: Maximum 10 MB per file (configurable)
3. **Sanitize Paths**: Never trust user-provided file paths
4. **Error Handling**: Never expose model details in error messages

## 📈 Monitoring

### View Logs

```bash
# Backend logs are printed to console
# For file logging, add to main.py:
logging.basicConfig(
    filename='backend.log',
    level=logging.INFO
)
```

### Performance Metrics

Add to your model_loader.py:
```python
import time

def predict(model, preprocessed_images):
    start_time = time.time()
    results = model.predict(preprocessed_images)
    inference_time = time.time() - start_time
    logger.info(f"Inference took {inference_time:.2f}s for {len(preprocessed_images)} images")
    return results
```

## 🚀 Production Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for production setup.

## 📞 Support

For issues specific to your model:
1. Check model compatibility
2. Verify preprocessing matches training
3. Ensure model file format is correct
4. Check framework version compatibility
