"""
X-Ray Pneumonia Detection Model
Extracted and adapted from xray2.ipynb
Integrates preprocessing, segmentation, and classification
Now integrated with PyTorch neural network model
"""

import cv2
import numpy as np
from PIL import Image
import io
import logging
import os
from pathlib import Path

try:
    import torch
    import torch.nn as nn
except ImportError:
    torch = None
    nn = None

logger = logging.getLogger(__name__)


if nn is not None:
    class Bottleneck(nn.Module):
        expansion = 4

        def __init__(self, inplanes, planes, stride=1, downsample=None):
            super().__init__()
            self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
            self.bn1 = nn.BatchNorm2d(planes)
            self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
            self.bn2 = nn.BatchNorm2d(planes)
            self.conv3 = nn.Conv2d(planes, planes * self.expansion, kernel_size=1, bias=False)
            self.bn3 = nn.BatchNorm2d(planes * self.expansion)
            self.relu = nn.ReLU(inplace=True)
            self.downsample = downsample
            self.stride = stride

        def forward(self, x):
            identity = x

            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu(out)

            out = self.conv2(out)
            out = self.bn2(out)
            out = self.relu(out)

            out = self.conv3(out)
            out = self.bn3(out)

            if self.downsample is not None:
                identity = self.downsample(x)

            out += identity
            out = self.relu(out)
            return out


    class ResNetBinaryClassifier(nn.Module):
        """Minimal ResNet-50 compatible with the provided state_dict checkpoint."""

        def __init__(self, layers=(3, 4, 6, 3), dropout=0.5):
            super().__init__()
            self.inplanes = 64
            self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
            self.bn1 = nn.BatchNorm2d(64)
            self.relu = nn.ReLU(inplace=True)
            self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
            self.layer1 = self._make_layer(64, layers[0])
            self.layer2 = self._make_layer(128, layers[1], stride=2)
            self.layer3 = self._make_layer(256, layers[2], stride=2)
            self.layer4 = self._make_layer(512, layers[3], stride=2)
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
            self.fc = nn.Sequential(nn.Dropout(p=dropout), nn.Linear(512 * Bottleneck.expansion, 1))

        def _make_layer(self, planes, blocks, stride=1):
            downsample = None
            if stride != 1 or self.inplanes != planes * Bottleneck.expansion:
                downsample = nn.Sequential(
                    nn.Conv2d(self.inplanes, planes * Bottleneck.expansion, kernel_size=1, stride=stride, bias=False),
                    nn.BatchNorm2d(planes * Bottleneck.expansion),
                )

            layers = [Bottleneck(self.inplanes, planes, stride, downsample)]
            self.inplanes = planes * Bottleneck.expansion
            for _ in range(1, blocks):
                layers.append(Bottleneck(self.inplanes, planes))

            return nn.Sequential(*layers)

        def forward(self, x):
            x = self.conv1(x)
            x = self.bn1(x)
            x = self.relu(x)
            x = self.maxpool(x)

            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            x = self.layer4(x)

            x = self.avgpool(x)
            x = torch.flatten(x, 1)
            x = self.fc(x)
            return x

# ========================================
# IMAGE LOADING
# ========================================

class ImageLoader:
    """Load images from various formats"""
    
    @staticmethod
    def load_image(image_bytes):
        """
        Load image from bytes
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            Grayscale numpy array
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'L':
                img = img.convert('L')
            return np.array(img)
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")


# ========================================
# IMAGE PREPROCESSING
# ========================================

class ImagePreprocessor:
    """Preprocess X-ray images"""
    
    def __init__(self, target_size=(256, 256)):
        self.target_size = target_size
    
    def normalize(self, image):
        """Normalize image to 0-255 range"""
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    def resize(self, image, size=None):
        """Resize image"""
        if size is None:
            size = self.target_size
        return cv2.resize(image, size)
    
    def enhance_clahe(self, image):
        """Apply CLAHE enhancement"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)
    
    def denoise_bilateral(self, image):
        """Apply bilateral filter for denoising"""
        return cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    
    def preprocess(self, image):
        """Full preprocessing pipeline"""
        # Normalize
        normalized = self.normalize(image)
        
        # Resize
        resized = self.resize(normalized)
        
        # Enhance contrast
        enhanced = self.enhance_clahe(resized)
        
        # Denoise
        denoised = self.denoise_bilateral(enhanced)
        
        return denoised


# ========================================
# LUNG SEGMENTATION
# ========================================

class LungSegmentor:
    """Segment lungs from chest X-rays"""
    
    def __init__(self):
        pass
    
    def segment_lungs(self, image):
        """
        Segment lungs using traditional CV techniques
        
        Args:
            image: Grayscale X-ray image
            
        Returns:
            Segmented image, lung mask
        """
        h, w = image.shape
        
        # Step 1: CLAHE enhancement
        normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(normalized)
        
        # Step 2: Find body region
        _, body = cv2.threshold(enhanced, 10, 255, cv2.THRESH_BINARY)
        
        # Clean body mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        body = cv2.morphologyEx(body, cv2.MORPH_CLOSE, kernel, iterations=3)
        body = cv2.GaussianBlur(body, (5, 5), 0) > 128
        body = body.astype(np.uint8) * 255
        
        # Step 3: Find bright regions (lungs)
        body_pixels = enhanced[body > 0]
        if len(body_pixels) > 0:
            threshold = np.percentile(body_pixels, 40)
        else:
            threshold = 100
        
        _, bright_regions = cv2.threshold(enhanced, threshold, 255, cv2.THRESH_BINARY)
        
        # Only keep bright regions inside body
        lung_candidates = cv2.bitwise_and(bright_regions, body)
        
        # Step 4: Remove borders and center spine
        border = 50
        lung_candidates[:border, :] = 0
        lung_candidates[-border:, :] = 0
        lung_candidates[:, :border] = 0
        lung_candidates[:, -border:] = 0
        
        # Remove center strip (spine, heart)
        center_strip = 80
        lung_candidates[:, w//2 - center_strip//2 : w//2 + center_strip//2] = 0
        
        # Remove top shoulders
        lung_candidates[:int(h*0.15), :] = 0
        
        # Step 5: Morphological cleanup
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        lung_candidates = cv2.morphologyEx(lung_candidates, cv2.MORPH_OPEN, kernel, iterations=2)
        lung_candidates = cv2.morphologyEx(lung_candidates, cv2.MORPH_CLOSE, kernel, iterations=3)
        
        # Step 6: Find connected components
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(lung_candidates, connectivity=8)
        
        lung_mask = np.zeros(image.shape, dtype=np.uint8)
        
        if num_labels > 1:
            valid_components = []
            
            for i in range(1, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                comp_w = stats[i, cv2.CC_STAT_WIDTH]
                comp_h = stats[i, cv2.CC_STAT_HEIGHT]
                cx = x + comp_w // 2
                cy = y + comp_h // 2
                
                area_pct = area / (h * w) * 100
                aspect_ratio = comp_h / comp_w if comp_w > 0 else 0
                
                if (8 < area_pct < 35 and
                    0.25 * h < cy < 0.75 * h and
                    (cx < 0.38 * w or cx > 0.62 * w) and
                    0.8 < aspect_ratio < 4.0):
                    valid_components.append((i, area))
            
            valid_components.sort(key=lambda x: x[1], reverse=True)
            
            for label_id, _ in valid_components[:2]:
                lung_mask[labels == label_id] = 255
        
        # Step 7: Final smoothing
        if np.count_nonzero(lung_mask) > 0:
            kernel_smooth = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            lung_mask = cv2.morphologyEx(lung_mask, cv2.MORPH_CLOSE, kernel_smooth, iterations=2)
            lung_mask = cv2.GaussianBlur(lung_mask, (7, 7), 0)
            _, lung_mask = cv2.threshold(lung_mask, 127, 255, cv2.THRESH_BINARY)
        
        # Apply mask
        segmented = cv2.bitwise_and(image, image, mask=lung_mask)
        
        return segmented, lung_mask


# ========================================
# FEATURE EXTRACTION
# ========================================

class FeatureExtractor:
    """Extract features from segmented lungs"""
    
    @staticmethod
    def extract_features(image, lung_mask):
        """
        Extract shape, intensity, and texture features
        
        Args:
            image: Original image
            lung_mask: Binary lung mask
            
        Returns:
            Feature dictionary
        """
        import logging
        logger = logging.getLogger(__name__)
        
        features = {}
        
        # Mask-based features
        segmented = cv2.bitwise_and(image, image, mask=lung_mask)
        lung_pixels = segmented[lung_mask > 0]
        
        # If segmentation failed, use the entire image as fallback
        if len(lung_pixels) == 0:
            logger.warning("Lung segmentation failed or empty, using entire image")
            lung_pixels = image.flatten()
        
        # Intensity features
        features['mean_intensity'] = float(np.mean(lung_pixels))
        features['std_intensity'] = float(np.std(lung_pixels))
        features['min_intensity'] = float(np.min(lung_pixels))
        features['max_intensity'] = float(np.max(lung_pixels))
        
        # Histogram features
        hist = cv2.calcHist([segmented], [0], lung_mask if np.count_nonzero(lung_mask) > 0 else None, [32], [0, 256])
        features['hist_mean'] = float(np.mean(hist))
        features['hist_std'] = float(np.std(hist))
        hist_centered = hist - np.mean(hist)
        hist_std = np.std(hist)
        features['hist_skew'] = float(np.mean(hist_centered**3) / (hist_std**3 + 1e-6))
        
        # Shape features
        lung_area = np.count_nonzero(lung_mask) if np.count_nonzero(lung_mask) > 0 else image.size / 2
        features['lung_area_ratio'] = float(lung_area / image.size)
        
        # Edge features (Roberts operator)
        edges = cv2.Sobel(segmented, cv2.CV_64F, 1, 0, ksize=3)
        if np.count_nonzero(lung_mask) > 0:
            features['edge_intensity'] = float(np.mean(np.abs(edges[lung_mask > 0])))
        else:
            features['edge_intensity'] = float(np.mean(np.abs(edges)))
        
        logger.debug(f"Extracted features: {features}")
        return features


# ========================================
# PNEUMONIA DETECTION CLASSIFIER - PyTorch Neural Network
# ========================================

class PyTorchPneumoniaClassifier:
    """
    PyTorch-based pneumonia classifier using trained neural network model
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the classifier with a PyTorch model
        
        Args:
            model_path: Path to the trained model file (best_model.pth)
        """
        if torch is None:
            logger.warning("PyTorch is not installed; using feature-based classification")
            self.device = None
            self.model = None
            self.model_path = model_path
            return

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.model_path = model_path
        self.framework = "pytorch"
        self.variant = os.getenv("MODEL_VARIANT", "clahe")
        self.output_format = "single_logit"
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            logger.warning(f"Model path not found: {model_path}")

    def _select_state_dict(self, checkpoint):
        """Select a loadable state_dict from supported checkpoint layouts."""
        if isinstance(checkpoint, nn.Module):
            self.output_format = "module"
            return checkpoint

        if not isinstance(checkpoint, dict):
            raise TypeError(f"Unsupported PyTorch checkpoint type: {type(checkpoint).__name__}")

        if "state_dict" in checkpoint and isinstance(checkpoint["state_dict"], dict):
            return checkpoint["state_dict"]

        if self.variant in checkpoint and isinstance(checkpoint[self.variant], dict):
            logger.info(f"Using checkpoint variant: {self.variant}")
            return checkpoint[self.variant]

        variant_names = [key for key, value in checkpoint.items() if isinstance(value, dict)]
        if variant_names:
            selected = variant_names[0]
            logger.warning(
                f"MODEL_VARIANT={self.variant} was not found. Using checkpoint variant: {selected}"
            )
            self.variant = selected
            return checkpoint[selected]

        if any("." in str(key) for key in checkpoint.keys()):
            return checkpoint

        raise TypeError("Checkpoint does not contain a recognizable state_dict")

    def _build_model_from_state_dict(self, state_dict):
        """Create the neural network architecture expected by the provided checkpoint."""
        normalized_state = {
            key.replace("module.", "", 1): value
            for key, value in state_dict.items()
        }

        model = ResNetBinaryClassifier()
        missing, unexpected = model.load_state_dict(normalized_state, strict=False)
        if unexpected:
            logger.warning(f"Unexpected model checkpoint keys: {unexpected[:5]}")
        critical_missing = [key for key in missing if not key.startswith("fc.0")]
        if critical_missing:
            raise RuntimeError(f"Checkpoint is missing required model keys: {critical_missing[:5]}")

        return model
    
    def load_model(self, model_path):
        """Load the PyTorch model"""
        try:
            logger.info(f"Attempting to load model from: {model_path}")
            try:
                checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
            except TypeError:
                checkpoint = torch.load(model_path, map_location=self.device)

            selected_model = self._select_state_dict(checkpoint)
            if isinstance(selected_model, nn.Module):
                self.model = selected_model
            else:
                self.model = self._build_model_from_state_dict(selected_model)

            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            logger.info(f"✓ Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            logger.warning("Model loading failed - will use feature-based classification")
            self.model = None
    
    def preprocess_for_model(self, image):
        """
        Preprocess image for neural network input
        
        Args:
            image: Grayscale numpy array (0-255)
            
        Returns:
            Tensor ready for model input
        """
        # Convert to float and normalize to 0-1
        image_float = image.astype(np.float32) / 255.0
        
        # Convert grayscale to 3-channel (repeat across RGB)
        image_3channel = np.stack([image_float, image_float, image_float], axis=0)
        
        # Convert to tensor and add batch dimension
        tensor = torch.from_numpy(image_3channel).unsqueeze(0).to(self.device)
        
        return tensor
    
    def classify(self, image):
        """
        Classify X-ray image using the neural network
        
        Args:
            image: Preprocessed grayscale image (256x256)
            
        Returns:
            Dictionary with prediction, confidence, probabilities
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Cannot perform classification.")
        
        try:
            # Preprocess image for model
            tensor = self.preprocess_for_model(image)
            
            # Run inference
            with torch.no_grad():
                output = self.model(tensor)

            if isinstance(output, (tuple, list)):
                output = output[0]

            if output.ndim == 1:
                output = output.unsqueeze(0)
            
            if output.shape[1] >= 2:
                probabilities = torch.softmax(output, dim=1)[0].cpu().numpy()
                normal_prob = float(probabilities[0]) * 100
                pneumonia_prob = float(probabilities[1]) * 100
            else:
                pneumonia_prob = float(torch.sigmoid(output)[0][0].cpu().item()) * 100
                normal_prob = 100 - pneumonia_prob
            
            # Determine prediction
            prediction = 'Affected' if pneumonia_prob > 50 else 'Normal'
            confidence = max(normal_prob, pneumonia_prob)
            
            logger.info(f"Model Prediction: {prediction}")
            logger.info(f"  Normal: {normal_prob:.1f}%")
            logger.info(f"  Pneumonia: {pneumonia_prob:.1f}%")
            logger.info(f"  Confidence: {confidence:.1f}%")
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'probability_pneumonia': pneumonia_prob,
                'probability_normal': normal_prob,
                'score': pneumonia_prob / 100.0
            }
            
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            raise


class PneumoniaClassifier:
    """
    Pneumonia classifier - will use PyTorch model if available, 
    falls back to feature-based classification
    """
    
    def __init__(self, use_pytorch=True, model_path=None):
        self.use_pytorch = use_pytorch
        self.pytorch_classifier = None
        self.fallback_available = True
        
        if use_pytorch and model_path:
            try:
                classifier = PyTorchPneumoniaClassifier(model_path)
                if classifier.model is not None:
                    self.pytorch_classifier = classifier
                    logger.info("Using PyTorch neural network classifier")
                else:
                    logger.warning("PyTorch model unavailable. Falling back to feature-based classifier.")
            except Exception as e:
                logger.warning(f"PyTorch classifier initialization failed: {e}. Falling back to feature-based classifier.")
                self.pytorch_classifier = None
    
    def classify(self, image_or_features):
        """
        Classify using PyTorch model if available, otherwise use features
        
        Args:
            image_or_features: Either preprocessed image array or features dict
            
        Returns:
            Dictionary with prediction, confidence, probabilities
        """
        # Try PyTorch classifier first
        if self.pytorch_classifier is not None and isinstance(image_or_features, np.ndarray):
            try:
                return self.pytorch_classifier.classify(image_or_features)
            except Exception as e:
                logger.warning(f"PyTorch classification failed: {e}. Falling back to feature-based.")
        
        # Fallback to feature-based classification
        if isinstance(image_or_features, dict):
            features = image_or_features
        else:
            logger.warning("Cannot use feature-based classification without features dict")
            return {
                'prediction': 'Unknown',
                'confidence': 0,
                'probability_pneumonia': 50,
                'probability_normal': 50,
                'score': 0.5
            }
        
        # Feature-based classification (original implementation)
        return self._classify_from_features(features)
    
    def _classify_from_features(self, features):
        """Original feature-based classification"""
        # Get features with proper defaults
        mean_intensity = float(features.get('mean_intensity', 128))
        std_intensity = float(features.get('std_intensity', 30))
        edge_intensity = float(features.get('edge_intensity', 10))
        lung_area_ratio = float(features.get('lung_area_ratio', 0.3))
        hist_skew = float(features.get('hist_skew', 0))
        
        logger.info(f"Classification Features (Feature-based fallback):")
        logger.info(f"  Mean Intensity: {mean_intensity:.1f}")
        logger.info(f"  Std Intensity: {std_intensity:.1f}")
        logger.info(f"  Edge Intensity: {edge_intensity:.1f}")
        logger.info(f"  Lung Area Ratio: {lung_area_ratio:.3f}")
        
        # Weighted scoring system
        affected_indicators = 0
        affected_score = 0.0
        
        # INDICATOR 1: Mean Intensity
        if mean_intensity < 50:
            affected_score += 0.8
            affected_indicators += 1
        elif mean_intensity < 80:
            affected_score += 0.6
            affected_indicators += 1
        elif mean_intensity < 110:
            affected_score += 0.3
            affected_indicators += 1
        elif mean_intensity < 140:
            affected_score += 0.1
            affected_indicators += 1
        else:
            affected_indicators += 1
        
        # INDICATOR 2: Standard Deviation
        if std_intensity > 45:
            affected_score += 0.7
            affected_indicators += 1
        elif std_intensity > 35:
            affected_score += 0.5
            affected_indicators += 1
        elif std_intensity > 25:
            affected_score += 0.2
            affected_indicators += 1
        elif std_intensity > 15:
            affected_indicators += 1
        else:
            affected_indicators += 1
        
        # INDICATOR 3: Edge Intensity
        if edge_intensity > 25:
            affected_score += 0.75
            affected_indicators += 1
        elif edge_intensity > 15:
            affected_score += 0.5
            affected_indicators += 1
        elif edge_intensity > 10:
            affected_score += 0.25
            affected_indicators += 1
        else:
            affected_indicators += 1
        
        # Calculate final probability
        if affected_indicators > 0:
            affected_prob = affected_score / affected_indicators
        else:
            affected_prob = 0.5
        
        affected_prob = min(max(affected_prob, 0.0), 1.0)
        normal_prob = 1.0 - affected_prob
        
        prediction = 'Affected' if affected_prob >= 0.5 else 'Normal'
        confidence = max(affected_prob, normal_prob) * 100
        
        logger.info(f"Final Assessment (Feature-based): {prediction}")
        logger.info(f"  Affected Lung: {affected_prob*100:.1f}%")
        logger.info(f"  Normal Lung: {normal_prob*100:.1f}%")
        logger.info(f"  Confidence: {confidence:.1f}%")
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'probability_pneumonia': affected_prob * 100,
            'probability_normal': normal_prob * 100,
            'score': affected_prob
        }


# ========================================
# MAIN PIPELINE
# ========================================

class PneumoniaDetectionPipeline:
    """Complete pneumonia detection pipeline with PyTorch model integration"""
    
    def __init__(self, model_path=None):
        self.loader = ImageLoader()
        self.preprocessor = ImagePreprocessor()
        self.segmentor = LungSegmentor()
        self.feature_extractor = FeatureExtractor()
        self.classifier = PneumoniaClassifier(use_pytorch=True, model_path=model_path)
        self.model_path = model_path
    
    def detect(self, image_bytes):
        """
        Complete detection pipeline
        
        Args:
            image_bytes: RAW image bytes from file upload
            
        Returns:
            Detection result dictionary
        """
        try:
            # 1. Load image
            image = self.loader.load_image(image_bytes)
            
            # 2. Preprocess
            preprocessed = self.preprocessor.preprocess(image)
            
            # 3. Try PyTorch classification first (on preprocessed image directly)
            if self.classifier.pytorch_classifier is not None:
                logger.info("Using PyTorch neural network for classification")
                result = self.classifier.classify(preprocessed)
            else:
                # Fallback to feature-based classification
                logger.info("Using feature-based classification")
                
                # Segment lungs
                segmented, lung_mask = self.segmentor.segment_lungs(preprocessed)
                
                # Extract features
                features = self.feature_extractor.extract_features(preprocessed, lung_mask)
                
                # Classify using features
                result = self.classifier.classify(features)
            
            return result
        
        except Exception as e:
            logger.error(f"Detection pipeline failed: {str(e)}")
            raise Exception(f"Detection pipeline failed: {str(e)}")


# Global pipeline instance
pipeline = None

def init_pipeline(model_path=None):
    """
    Initialize the detection pipeline
    
    Args:
        model_path: Path to the PyTorch model file
    """
    global pipeline
    if model_path is None:
        # Try to find the model in default location
        default_model_path = Path(__file__).parent.parent / 'models' / 'model_clahe.pth'
        if default_model_path.exists():
            model_path = str(default_model_path)
            logger.info(f"Found model at default location: {model_path}")
        else:
            logger.warning(f"Model not found at default location: {default_model_path}")

    should_initialize = pipeline is None or str(getattr(pipeline, "model_path", "")) != str(model_path)
    if should_initialize:
        pipeline = PneumoniaDetectionPipeline(model_path=model_path)
    return pipeline

def detect_pneumonia(image_bytes, model_path=None):
    """
    Detect pneumonia from X-ray image bytes
    
    Args:
        image_bytes: Raw image bytes
        model_path: Path to the PyTorch model (optional)
        
    Returns:
        Detection result
    """
    init_pipeline(model_path=model_path)
    return pipeline.detect(image_bytes)
