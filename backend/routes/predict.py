"""
Prediction API routes.

Primary production endpoint:
    POST /api/analyze

Compatibility endpoint:
    POST /api/predict
"""

import base64
import binascii
import logging
import time
from typing import List, Optional, Tuple

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from schemas import AnalyzeRequest, ImagePayload
from services.model_loader import get_model, predict

logger = logging.getLogger(__name__)

router = APIRouter()

MAX_FILES = 10
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}
MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_file_type(filename: Optional[str]) -> bool:
    return bool(filename) and "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    return 0 < file_size <= MAX_FILE_SIZE


def _strip_data_url(value: str) -> str:
    if "," in value and value.strip().lower().startswith("data:"):
        return value.split(",", 1)[1]
    return value


def decode_image_payload(image: ImagePayload) -> bytes:
    try:
        decoded = base64.b64decode(_strip_data_url(image.data), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image data for {image.filename}") from exc

    if not validate_file_size(len(decoded)):
        raise HTTPException(
            status_code=400,
            detail=f"File size for {image.filename} must be between 1 byte and 10 MB",
        )

    if not validate_file_type(image.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {image.filename}. Allowed: JPG, JPEG, PNG",
        )

    return decoded


def extract_json_images(payload: AnalyzeRequest) -> Tuple[List[bytes], List[str]]:
    images = list(payload.images)

    if payload.input is not None and not images:
        if isinstance(payload.input, str):
            images = [ImagePayload(filename="input.png", data=payload.input)]
        elif isinstance(payload.input, list):
            images = [
                ImagePayload(filename=f"input-{index + 1}.png", data=value)
                for index, value in enumerate(payload.input)
            ]
        elif isinstance(payload.input, dict):
            raw_images = payload.input.get("images") or payload.input.get("files") or []
            if isinstance(raw_images, str):
                raw_images = [raw_images]
            images = [
                item if isinstance(item, ImagePayload) else ImagePayload(**item) if isinstance(item, dict)
                else ImagePayload(filename=f"input-{index + 1}.png", data=item)
                for index, item in enumerate(raw_images)
            ]

    if not images:
        raise HTTPException(status_code=400, detail="No images provided")
    if len(images) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Too many files. Maximum {MAX_FILES} files allowed.")

    image_bytes = [decode_image_payload(image) for image in images]
    filenames = [image.filename for image in images]
    return image_bytes, filenames


async def extract_upload_images(files: Optional[List[UploadFile]]) -> Tuple[List[bytes], List[str]]:
    if files is None or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files provided")
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Too many files. Maximum {MAX_FILES} files allowed.")

    image_bytes = []
    filenames = []
    for file in files:
        if file is None or not file.filename:
            raise HTTPException(status_code=400, detail="One of the uploaded files is missing a filename")
        if not validate_file_type(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Allowed: JPG, JPEG, PNG",
            )
        if file.content_type and file.content_type.lower() not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")

        content = await file.read()
        if not validate_file_size(len(content)):
            raise HTTPException(
                status_code=400,
                detail=f"File size for {file.filename} must be between 1 byte and 10 MB",
            )
        image_bytes.append(content)
        filenames.append(file.filename)

    return image_bytes, filenames


async def run_prediction(image_bytes: List[bytes], filenames: List[str]) -> dict:
    started_at = time.perf_counter()
    model = get_model()
    prediction_results = await run_in_threadpool(predict, model, image_bytes)
    processing_time_ms = round((time.perf_counter() - started_at) * 1000, 2)

    predictions = []
    for filename, pred in zip(filenames, prediction_results):
        status = "error" if pred.get("prediction") == "Error" or pred.get("error") else "success"
        predictions.append({
            "filename": filename,
            "prediction": pred.get("prediction", "Unknown"),
            "confidence": round(float(pred.get("confidence", 0)), 2),
            "probability_normal": round(float(pred.get("probability_normal", 0)), 2),
            "probability_pneumonia": round(float(pred.get("probability_pneumonia", 0)), 2),
            "status": status,
            "error": pred.get("error"),
        })

    first_success = next((item for item in predictions if item["status"] == "success"), None)
    logger.info(
        f"Inference completed for {len(predictions)} image(s) in {processing_time_ms} ms"
    )
    return {
        "success": all(item["status"] == "success" for item in predictions),
        "prediction": first_success["prediction"] if first_success else None,
        "confidence": first_success["confidence"] if first_success else None,
        "processing_time_ms": processing_time_ms,
        "predictions": predictions,
        "model": model.metadata(),
    }


@router.post("/analyze")
async def analyze_pneumonia(payload: AnalyzeRequest):
    """Analyze one or more base64-encoded X-ray images from a structured JSON body."""
    image_bytes, filenames = extract_json_images(payload)
    logger.info(f"Received JSON analyze request with {len(filenames)} image(s)")
    return await run_prediction(image_bytes, filenames)


@router.post("/predict")
async def predict_pneumonia(files: Optional[List[UploadFile]] = File(default=None)):
    """Compatibility endpoint for multipart image uploads."""
    image_bytes, filenames = await extract_upload_images(files)
    logger.info(f"Received multipart predict request with {len(filenames)} image(s)")
    return await run_prediction(image_bytes, filenames)


@router.get("/predict/config")
async def get_prediction_config():
    model = get_model()
    return {
        "success": True,
        "max_files": MAX_FILES,
        "allowed_formats": sorted(ALLOWED_EXTENSIONS),
        "allowed_content_types": sorted(ALLOWED_CONTENT_TYPES),
        "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
        "api": {
            "json_endpoint": "/api/analyze",
            "multipart_endpoint": "/api/predict",
            "health_endpoint": "/api/health",
        },
        "model": model.metadata(),
    }


@router.get("/health")
async def api_health_check():
    model = get_model()
    return {
        "success": True,
        "status": "running",
        "service": "SYNAPSE-X API",
        "model": model.metadata(),
    }
