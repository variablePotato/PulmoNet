# ANTIGRAVITY Model Integration Guide

Complete guide for integrating your Kaggle-trained pneumonia detection model.

## 📌 Overview

This guide walks you through integrating your trained pneumonia detection model with ANTIGRAVITY.

**Important**: The application includes placeholders designed to be easily replaced with your model.

---

## 🎯 Quick Integration (5 Steps)

### Step 1: Prepare Your Model File

```bash
# Create models directory in backend
mkdir -p backend/models

# Copy your trained model
cp path/to/your/pneumonia_model.h5 backend/models/
```

**Supported formats**:
- TensorFlow/Keras: `.h5`, `.pb`
- PyTorch: `.pt`, `.pth`
- scikit-learn: `.pkl`, `.joblib`
- ONNX: `.onnx`

### Step 2: Update requirements.txt

Add your ML framework to `backend/requirements.txt`:

```text
# Add one of these:
tensorflow==2.14.0
# torch==2.1.0
# scikit-learn==1.3.2
```

Install:
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Update Model Loader

Edit `backend/services/model_loader.py`:

Replace:
```python
def load_model():
    model = ModelPlaceholder()
    model.is_loaded = True
    return model
```

With your actual loading code (see examples below).

### Step 4: Update Preprocessing

Edit `backend/utils/preprocess.py`:

Update configuration values to match your training:
```python
IMG_WIDTH = 224  # Your model input width
IMG_HEIGHT = 224  # Your model input height
IMG_CHANNELS = 1  # 1 for grayscale, 3 for RGB
NORMALIZATION_MEAN = 0.5  # Your training mean
NORMALIZATION_STD = 0.5  # Your training std
```

And update preprocessing functions if needed.

### Step 5: Test

```bash
# Start backend
python backend/main.py

# Test with cURL
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@test_xray.png"
```

---

## 📚 Complete Integration Examples

### Example 1: TensorFlow/Keras Model

**Your model structure**:
```
- pneumonia_model.h5 (trained model)
- Model trained with: Conv2D → Dense → Output (2 classes: Normal, Pneumonia)
```

**Update `backend/services/model_loader.py`**:

```python
import tensorflow as tf
import numpy as np

# Global model cache
_model_instance = None

def load_model():
    """Load TensorFlow/Keras model"""
    global _model_instance
    
    try:
        logger.info("Loading TensorFlow model...")
        
        # Load the model
        model = tf.keras.models.load_model('backend/models/pneumonia_model.h5')
        
        # Verify model
        logger.info(f"Model loaded successfully")
        logger.info(f"Input shape: {model.input_shape}")
        logger.info(f"Output shape: {model.output_shape}")
        
        return model
        
    except FileNotFoundError:
        logger.error("Model file not found at backend/models/pneumonia_model.h5")
        raise
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


def predict(model, preprocessed_images: List) -> List[dict]:
    """Run inference with TensorFlow model"""
    try:
        if not preprocessed_images:
            return []
        
        # Convert list to numpy array
        batch = np.array(preprocessed_images)
        logger.info(f"Running inference on batch shape: {batch.shape}")
        
        # Get predictions (output shape: [batch_size, 2])
        # Assuming your model outputs [prob_normal, prob_pneumonia]
        predictions = model.predict(batch, batch_size=32)
        
        results = []
        for i, pred in enumerate(predictions):
            # Extract probabilities
            prob_normal = float(pred[0])
            prob_pneumonia = float(pred[1])
            
            # Determine prediction
            is_pneumonia = prob_pneumonia > prob_normal
            
            result = {
                "prediction": "Pneumonia" if is_pneumonia else "Normal",
                "confidence": float(max(prob_normal, prob_pneumonia) * 100),
                "probability_normal": prob_normal,
                "probability_pneumonia": prob_pneumonia
            }
            results.append(result)
            
        logger.info(f"Inference complete: {len(results)} predictions")
        return results
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise


def get_model():
    """Singleton pattern for model loading"""
    global _model_instance
    if _model_instance is None:
        _model_instance = load_model()
    return _model_instance
```

**Update `backend/utils/preprocess.py`**:

```python
# If your model was trained with these settings, update:
IMG_WIDTH = 224
IMG_HEIGHT = 224
IMG_CHANNELS = 1  # Grayscale
NORMALIZATION_MEAN = 0.5
NORMALIZATION_STD = 0.5

# If you used ImageDataGenerator or different normalization:
# NORMALIZATION_MEAN = 100.0  # Dataset mean pixel value
# NORMALIZATION_STD = 50.0    # Dataset standard deviation
```

---

### Example 2: PyTorch Model

**Your model structure**:
```python
class PneumoniaNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(224*224, 2)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

**Update `backend/services/model_loader.py`**:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class PneumoniaNet(nn.Module):
    """Define your model architecture"""
    def __init__(self):
        super().__init__()
        # Copy your model architecture here
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
            # ... more layers
        )
        self.classifier = nn.Sequential(
            nn.Linear(32 * 111 * 111, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 2)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def load_model():
    """Load PyTorch model"""
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {device}")
        
        # Load model
        model = PneumoniaNet().to(device)
        checkpoint = torch.load('backend/models/pneumonia_model.pt', 
                               map_location=device)
        model.load_state_dict(checkpoint)
        model.eval()
        
        logger.info("PyTorch model loaded successfully")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


def predict(model, preprocessed_images: List) -> List[dict]:
    """Run inference with PyTorch model"""
    try:
        device = next(model.parameters()).device
        batch = torch.from_numpy(np.array(preprocessed_images)).float().to(device)
        
        with torch.no_grad():
            outputs = model(batch)
            probabilities = F.softmax(outputs, dim=1)
        
        results = []
        for probs in probabilities:
            prob_normal = probs[0].item()
            prob_pneumonia = probs[1].item()
            
            result = {
                "prediction": "Pneumonia" if prob_pneumonia > prob_normal else "Normal",
                "confidence": float(max(prob_normal, prob_pneumonia) * 100),
                "probability_normal": prob_normal,
                "probability_pneumonia": prob_pneumonia
            }
            results.append(result)
        
        return results
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

---

### Example 3: scikit-learn Model

**Your pipeline**:
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])
```

**Update `backend/services/model_loader.py`**:

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


def predict(model, preprocessed_images: List) -> List[dict]:
    """Run inference with scikit-learn model"""
    try:
        # Flatten images for sklearn
        batch_flat = np.array([img.flatten() for img in preprocessed_images])
        
        predictions = model.predict(batch_flat)
        probabilities = model.predict_proba(batch_flat)
        
        results = []
        for pred, probs in zip(predictions, probabilities):
            result = {
                "prediction": "Pneumonia" if pred == 1 else "Normal",
                "confidence": float(max(probs) * 100),
                "probability_normal": float(probs[0]),
                "probability_pneumonia": float(probs[1])
            }
            results.append(result)
        
        return results
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

---

## 🔍 Verification Checklist

### Before Integration

- [ ] Model file is in `backend/models/` directory
- [ ] Model format file extension matches framework
- [ ] ML framework added to `requirements.txt`
- [ ] Backend requirements installed: `pip install -r requirements.txt`

### After Integration

- [ ] Backend starts without errors: `python main.py`
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] API configuration accessible: `curl http://localhost:8000/api/predict/config`
- [ ] Prediction works with single image
- [ ] Prediction works with multiple images
- [ ] Confidence scores are reasonable (0-100%)
- [ ] Results match expected format

### Testing

```bash
# Test 1: Backend starts
python backend/main.py
# Should see: "INFO:     Started server process"

# Test 2: Health check
curl http://localhost:8000/health
# Should return: {"status": "running"}

# Test 3: Prediction
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@test_xray.png"
# Should return JSON with predictions

# Test 4: Multiple images
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@xray1.png" \
  -F "files=@xray2.png"
# Should return 2 predictions
```

---

## 🎓 Model Best Practices

### Input Format
- Ensure images are resized to model's expected dimensions
- Check channel count (grayscale vs RGB)
- Verify normalization matches training

### Output Format
- Model should output 2 values (probabilities for each class)
- Probabilities should sum to 1.0
- First output = Probability of Normal
- Second output = Probability of Pneumonia

### Performance
- Profile inference time
- Optimize for batch processing
- Consider quantization for faster inference

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Check file path and name |
| Import error | Install ML framework: `pip install tensorflow` |
| Shape mismatch | Verify preprocessing matches training |
| Slow predictions | Reduce model size or use GPU |
| Bad accuracy | Check preprocessing pipeline |
| Memory issues | Reduce batch size or use 8-bit quantization |

---

## 📊 Expected Output

Your model predictions should return:

```json
{
  "filename": "xray1.png",
  "prediction": "Pneumonia",
  "confidence": 96.4,
  "probability_normal": 0.036,
  "probability_pneumonia": 0.964,
  "status": "success"
}
```

Verify:
- Confidence is 0-100%
- Probabilities sum to ~1.0
- Prediction matches higher probability

---

## ✅ Integration Complete!

Once tests pass, your model is integrated and ready for:
- ✅ Production deployment
- ✅ Batch predictions
- ✅ API access
- ✅ Frontend usage

---

For detailed backend setup, see [SETUP.md](./SETUP.md)
For API documentation, see [API_DOCS.md](./API_DOCS.md)
For deployment, see [DEPLOYMENT.md](./DEPLOYMENT.md)
