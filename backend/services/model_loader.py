"""
Model service for SYNAPSE-X.

The backend keeps one model wrapper in memory and reuses it for every request.
The provided model file is a PyTorch checkpoint saved as ``best_model.pth``.
"""

import logging
import os
import time
from pathlib import Path
from typing import List, Optional

from .xray_model import init_pipeline

logger = logging.getLogger(__name__)


class ModelWrapper:
    """Owns the X-ray detection pipeline and exposes production-style metadata."""

    def __init__(self, model_path: Optional[str] = None):
        self.pipeline = None
        self.is_loaded = False
        self.model_path = self._resolve_model_path(model_path)
        self.framework = "pytorch"
        self.model_variant = os.getenv("MODEL_VARIANT", "clahe")
        self.input_format = {
            "type": "image",
            "formats": ["jpg", "jpeg", "png"],
            "preprocessing": [
                "grayscale conversion",
                "resize to 256x256",
                "CLAHE enhancement",
                "bilateral denoise",
                "3-channel tensor normalization to 0..1",
            ],
        }
        self.output_format = {
            "prediction": "Normal or Affected",
            "confidence": "percentage 0..100",
            "probabilities": "percentage 0..100 for normal and pneumonia",
        }
        self.load_time_ms = 0.0
        self._load_pipeline()

    @staticmethod
    def _resolve_model_path(model_path: Optional[str]) -> Optional[str]:
        configured_path = model_path or os.getenv("MODEL_PATH")
        if configured_path:
            candidate = Path(configured_path)
            if not candidate.is_absolute():
                candidate = Path(__file__).resolve().parent.parent / candidate
            return str(candidate)

        default_model_path = Path(__file__).resolve().parent.parent / "models" / "model_clahe.pth"
        return str(default_model_path)

    def _load_pipeline(self):
        started_at = time.perf_counter()
        try:
            if self.model_path and not Path(self.model_path).exists():
                logger.warning(f"Model file not found at {self.model_path}; fallback classifier will be used")

            logger.info(f"Loading SYNAPSE-X model from {self.model_path}")
            self.pipeline = init_pipeline(model_path=self.model_path)
            self.is_loaded = self.pipeline is not None
            self.load_time_ms = round((time.perf_counter() - started_at) * 1000, 2)

            classifier = getattr(self.pipeline, "classifier", None)
            pytorch_classifier = getattr(classifier, "pytorch_classifier", None)
            if pytorch_classifier is not None and pytorch_classifier.model is not None:
                self.model_variant = getattr(pytorch_classifier, "variant", self.model_variant)
                logger.info(
                    f"PyTorch model ready in {self.load_time_ms} ms "
                    f"(variant={self.model_variant})"
                )
            else:
                logger.info(
                    f"Feature-based fallback classifier ready in {self.load_time_ms} ms"
                )
        except Exception:
            logger.exception("Failed to initialize model pipeline")
            self.pipeline = None
            self.is_loaded = False
            raise

    def predict(self, image_bytes_list: List[bytes]) -> List[dict]:
        """Run inference for a batch of already validated image byte strings."""
        if not self.pipeline:
            raise RuntimeError("Pipeline not initialized")

        results = []
        for image_bytes in image_bytes_list:
            try:
                results.append(self.pipeline.detect(image_bytes))
            except Exception as exc:
                logger.exception("Failed to process uploaded image")
                results.append({
                    "prediction": "Error",
                    "confidence": 0,
                    "probability_normal": 0,
                    "probability_pneumonia": 0,
                    "error": str(exc),
                })
        return results

    def warmup(self):
        """Run a tiny synthetic image through the pipeline to allocate lazy resources."""
        if not self.pipeline:
            return

        try:
            from PIL import Image
            import io

            image = Image.new("L", (256, 256), color=128)
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            self.predict([buffer.getvalue()])
            logger.info("Model warmup completed")
        except Exception:
            logger.exception("Model warmup failed")

    def metadata(self) -> dict:
        return {
            "loaded": self.is_loaded,
            "framework": self.framework,
            "model_file": Path(self.model_path).name if self.model_path else None,
            "model_variant": self.model_variant,
            "load_time_ms": self.load_time_ms,
            "input_format": self.input_format,
            "output_format": self.output_format,
        }


_model_instance: Optional[ModelWrapper] = None


def load_model() -> ModelWrapper:
    logger.info("Loading model singleton")
    return ModelWrapper()


def get_model() -> ModelWrapper:
    global _model_instance
    if _model_instance is None:
        _model_instance = load_model()
    return _model_instance


def warmup_model() -> None:
    get_model().warmup()


def reload_model() -> ModelWrapper:
    global _model_instance
    _model_instance = load_model()
    return _model_instance


def predict(model: ModelWrapper, image_bytes_list: List[bytes]) -> List[dict]:
    if not image_bytes_list:
        return []
    logger.info(f"Running inference for {len(image_bytes_list)} image(s)")
    return model.predict(image_bytes_list)


def validate_model(model) -> bool:
    return bool(model and getattr(model, "is_loaded", False) and hasattr(model, "predict"))
