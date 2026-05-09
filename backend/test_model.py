#!/usr/bin/env python3
"""
Test script to verify PyTorch model integration and run inference tests
"""

import cv2
import numpy as np
from pathlib import Path
from services.xray_model import init_pipeline
from services.model_loader import get_model, predict

def test_model_loading():
    """Test that the model loads successfully"""
    print("\n" + "="*60)
    print("TEST: Model Loading")
    print("="*60)
    
    try:
        model = get_model()
        if model.is_loaded:
            print("✓ Model loaded successfully")
            print(f"  PyTorch model available: {model.pipeline.classifier.pytorch_classifier is not None}")
            return True
        else:
            print("✗ Model failed to load")
            return False
    except Exception as e:
        print(f"✗ Model loading failed: {str(e)}")
        return False

def test_model_with_synthetic_images():
    """Test model with synthetic test images"""
    
    print("\n" + "="*60)
    print("TEST: Inference with Synthetic Images")
    print("="*60)
    
    # Initialize pipeline
    pipeline = init_pipeline()
    print("✓ Pipeline initialized")
    
    # Create synthetic test images
    # Test image 1: Normal lungs (higher intensity)
    normal_img = np.ones((256, 256), dtype=np.uint8) * 200
    normal_img[50:206, 80:176] = 180
    cv2.circle(normal_img, (110, 100), 40, 150, -1)
    cv2.circle(normal_img, (146, 100), 40, 150, -1)
    normal_bytes = normal_img.tobytes()
    
    # Test image 2: Affected lungs (lower intensity with consolidation)
    affected_img = np.ones((256, 256), dtype=np.uint8) * 180
    affected_img[50:206, 80:176] = 100
    cv2.circle(affected_img, (110, 100), 40, 60, -1)
    cv2.circle(affected_img, (146, 100), 40, 70, -1)
    cv2.ellipse(affected_img, (110, 90), (20, 25), 0, 0, 360, 30, -1)
    cv2.ellipse(affected_img, (146, 100), (15, 20), 0, 0, 360, 40, -1)
    affected_bytes = affected_img.tobytes()
    
    # Test with model
    print("\nTesting with PyTorch model...")
    print("-" * 60)
    
    try:
        # Test normal image
        print("\n1. Normal Lungs (High Intensity)")
        result1 = pipeline.detect(normal_bytes)
        print(f"   Prediction: {result1['prediction']}")
        print(f"   Confidence: {result1['confidence']:.1f}%")
        print(f"   Pneumonia Probability: {result1['probability_pneumonia']:.1f}%")
        print(f"   Normal Probability: {result1['probability_normal']:.1f}%")
        
        # Test affected image
        print("\n2. Affected Lungs (Low Intensity + Infiltrates)")
        result2 = pipeline.detect(affected_bytes)
        print(f"   Prediction: {result2['prediction']}")
        print(f"   Confidence: {result2['confidence']:.1f}%")
        print(f"   Pneumonia Probability: {result2['probability_pneumonia']:.1f}%")
        print(f"   Normal Probability: {result2['probability_normal']:.1f}%")
        
        return True
    except Exception as e:
        print(f"✗ Inference failed: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction with model wrapper"""
    
    print("\n" + "="*60)
    print("TEST: Batch Prediction")
    print("="*60)
    
    try:
        # Get model
        model = get_model()
        
        # Create test images
        normal_img = np.ones((256, 256), dtype=np.uint8) * 200
        affected_img = np.ones((256, 256), dtype=np.uint8) * 100
        
        image_bytes_list = [normal_img.tobytes(), affected_img.tobytes()]
        
        # Run batch prediction
        results = predict(model, image_bytes_list)
        
        print(f"✓ Batch prediction completed for {len(results)} images")
        for i, result in enumerate(results, 1):
            print(f"\n  Image {i}:")
            print(f"    Prediction: {result['prediction']}")
            print(f"    Confidence: {result['confidence']:.1f}%")
            print(f"    Pneumonia: {result['probability_pneumonia']:.1f}%")
        
        return True
    except Exception as e:
        print(f"✗ Batch prediction failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SYNAPSE-X PyTorch Model Integration Tests")
    print("="*60)
    
    results = []
    
    # Test 1: Model loading
    results.append(("Model Loading", test_model_loading()))
    
    # Test 2: Inference with synthetic images
    results.append(("Synthetic Image Inference", test_model_with_synthetic_images()))
    
    # Test 3: Batch prediction
    results.append(("Batch Prediction", test_batch_prediction()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")

if __name__ == "__main__":
    main()
    
    # Check if model is differentiating
    print("\n" + "="*60)
    print("ANALYSIS")
    print("="*60)
    diff = abs(result1['probability_pneumonia'] - result2['probability_pneumonia'])
    if diff > 10:
        print(f"✓ Model IS differentiating (difference: {diff:.1f}%)")
    else:
        print(f"✗ Model is NOT differentiating well (difference: {diff:.1f}%)")

if __name__ == "__main__":
    test_model_with_test_image()
