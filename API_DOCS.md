# ANTIGRAVITY API Documentation

Complete API reference for the ANTIGRAVITY pneumonia detection system.

## 📖 Overview

The ANTIGRAVITY API is a RESTful service for pneumonia detection from chest X-ray images.

**Base URL**: `http://localhost:8000`

## 🔗 Endpoints

### 1. Health Check

Check if the server is running.

```
GET /health
```

**Response:**
```json
{
  "status": "running",
  "service": "ANTIGRAVITY API"
}
```

**Status Code**: `200 OK`

---

### 2. Root Information

Get basic API information.

```
GET /
```

**Response:**
```json
{
  "name": "ANTIGRAVITY",
  "tagline": "AI-powered chest X-ray screening for pneumonia detection",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "predict": "/api/predict",
    "docs": "/docs"
  }
}
```

**Status Code**: `200 OK`

---

### 3. Predict Pneumonia

Submit chest X-ray images for pneumonia prediction.

```
POST /api/predict
```

**Headers:**
```
Content-Type: multipart/form-data
```

**Request Body:**
```
files: [file1, file2, ...]  (List of image files)
```

**Supported Formats**: JPG, JPEG, PNG

**Constraints:**
- Maximum 10 files per request
- Maximum 10 MB per file
- Recommended: Clear chest X-ray images

**Example Request (curl):**

```bash
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@xray1.png" \
  -F "files=@xray2.png"
```

**Example Response:**

```json
[
  {
    "filename": "xray1.png",
    "prediction": "Pneumonia",
    "confidence": 96.4,
    "probability_normal": 0.036,
    "probability_pneumonia": 0.964,
    "status": "success"
  },
  {
    "filename": "xray2.png",
    "prediction": "Normal",
    "confidence": 91.2,
    "probability_normal": 0.912,
    "probability_pneumonia": 0.088,
    "status": "success"
  }
]
```

**Status Code**: `200 OK`

**Error Response (400):**

```json
{
  "detail": "Invalid file type: document.pdf. Allowed: JPG, JPEG, PNG"
}
```

**Error Response (413):**

```json
{
  "detail": "File too large: image.png. Maximum size: 10 MB"
}
```

**Error Response (422):**

```json
{
  "detail": "Too many files. Maximum 10 files allowed."
}
```

**Error Response (500):**

```json
{
  "error": "Internal server error",
  "details": "Error message here"
}
```

---

### 4. Prediction Configuration

Get prediction system configuration and constraints.

```
GET /api/predict/config
```

**Response:**

```json
{
  "max_files": 10,
  "allowed_formats": ["jpg", "jpeg", "png"],
  "max_file_size_mb": 10,
  "predictions": {
    "classes": ["Normal", "Pneumonia"],
    "output_format": "confidence percentage (0-100)"
  },
  "preprocessing": {
    "image_width": 224,
    "image_height": 224,
    "channels": 1,
    "note": "Configure preprocessing parameters in utils/preprocess.py"
  }
}
```

**Status Code**: `200 OK`

---

## 📊 Response Format

### Prediction Object

Each prediction in the response contains:

| Field | Type | Description |
|-------|------|-------------|
| `filename` | string | Original uploaded filename |
| `prediction` | string | Prediction result: "Normal" or "Pneumonia" |
| `confidence` | number | Confidence percentage (0-100) |
| `probability_normal` | number | Probability of normal (0-1) |
| `probability_pneumonia` | number | Probability of pneumonia (0-1) |
| `status` | string | Status: "success" or "error" |

### Example Prediction

```json
{
  "filename": "chest_xray_001.png",
  "prediction": "Pneumonia",
  "confidence": 96.4,
  "probability_normal": 0.036,
  "probability_pneumonia": 0.964,
  "status": "success"
}
```

---

## ⚠️ Error Handling

### Error Status Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 413 | Payload Too Large |
| 422 | Validation Error |
| 500 | Internal Server Error |

### Common Errors

#### No Files Provided
```json
{
  "detail": "No files provided"
}
```

#### Invalid File Type
```json
{
  "detail": "Invalid file type: document.pdf. Allowed: JPG, JPEG, PNG"
}
```

#### File Too Large
```json
{
  "detail": "File too large: image.png. Maximum size: 10 MB"
}
```

#### Too Many Files
```json
{
  "detail": "Too many files. Maximum 10 files allowed."
}
```

#### Image Preprocessing Failed
```json
{
  "detail": "Image preprocessing failed: Invalid image format"
}
```

#### Model Inference Failed
```json
{
  "detail": "Prediction failed: Model not loaded"
}
```

---

## 🔐 Security

### Rate Limiting
Currently not implemented. Recommended for production.

### CORS
All origins allowed. Configuration in `main.py`:
```python
allow_origins=["*"],  # Restrict in production
```

### File Validation
- File type checking
- File size validation
- File count validation
- Filename sanitization

---

## 📱 Integration Examples

### Python (requests)

```python
import requests

files = [('files', open('xray1.png', 'rb')), 
         ('files', open('xray2.png', 'rb'))]

response = requests.post('http://localhost:8000/api/predict', files=files)
predictions = response.json()

for pred in predictions:
    print(f"{pred['filename']}: {pred['prediction']} ({pred['confidence']}%)")
```

### JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('files', file1);
formData.append('files', file2);

const response = await fetch('http://localhost:8000/api/predict', {
  method: 'POST',
  body: formData
});

const predictions = await response.json();
predictions.forEach(pred => {
  console.log(`${pred.filename}: ${pred.prediction} (${pred.confidence}%)`);
});
```

### cURL

```bash
# Single file
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@xray1.png"

# Multiple files
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@xray1.png" \
  -F "files=@xray2.png" \
  -F "files=@xray3.png"
```

### React/TypeScript

```typescript
const submitPrediction = async (files: File[]) => {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));

  const response = await fetch('http://localhost:8000/api/predict', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Prediction failed');
  }

  return response.json();
};
```

---

## 🧪 Testing

### Test with Swagger UI
Visit: `http://localhost:8000/docs`

### Test with ReDoc
Visit: `http://localhost:8000/redoc`

### Command Line Test

```bash
# Test health
curl http://localhost:8000/health

# Test with sample image
curl -X POST "http://localhost:8000/api/predict" \
  -F "files=@sample_xray.png" | python -m json.tool
```

---

## 📊 Performance

### Typical Response Times
- Single image: 1-3 seconds
- 5 images: 2-5 seconds
- 10 images: 3-8 seconds

(Varies based on your model and hardware)

### Optimization Tips
1. Process maximum images in batch (10)
2. Avoid sending 1-2 images repeatedly
3. Use appropriate image quality
4. Ensure sufficient server resources

---

## 🔄 Versioning

**Current Version**: 1.0.0

Future versions may include:
- Rate limiting
- Authentication
- Async processing
- Results caching
- Confidence thresholds
- Region of interest analysis

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This API returns AI predictions that must be:
- Used only as a screening aid
- Reviewed by qualified healthcare professionals
- Never used as sole diagnostic tool
- Documented in patient records

Results are not a substitute for professional medical diagnosis.

---

## 📞 Support

For API issues or questions:
1. Check error message details
2. Review this documentation
3. Check server logs
4. Verify model is properly loaded

---

## 🚀 Advanced Usage

### Batch Processing Script

```python
import requests
import os
from pathlib import Path

def predict_directory(image_dir, output_file='results.json'):
    """Predict all images in a directory"""
    images = list(Path(image_dir).glob('*.png')) + \
             list(Path(image_dir).glob('*.jpg'))
    
    for i in range(0, len(images), 10):
        batch = images[i:i+10]
        files = [('files', open(img, 'rb')) for img in batch]
        
        response = requests.post('http://localhost:8000/api/predict', 
                                files=files)
        predictions = response.json()
        
        # Process predictions...
        for pred in predictions:
            print(f"{pred['filename']}: {pred['prediction']}")
```

---

**Last Updated**: 2024
**API Version**: 1.0.0
