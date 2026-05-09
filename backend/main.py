"""
SYNAPSE-X backend API.

The API loads the pneumonia model once on startup, exposes structured
inference endpoints, and centralizes request/error logging.
"""

import logging
import os
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.predict import router as predict_router
from services.model_loader import get_model, warmup_model

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SYNAPSE-X API",
    description="AI-powered chest X-ray screening for pneumonia detection",
    version="1.0.0",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins or ["*"],
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api", tags=["predictions"])


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    started_at = time.perf_counter()
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
    logger.info(
        f"Completed request: {request.method} {request.url.path} "
        f"status={response.status_code} duration_ms={duration_ms}"
    )
    response.headers["X-Processing-Time-ms"] = str(duration_ms)
    return response


@app.on_event("startup")
async def startup_event():
    logger.info("Starting SYNAPSE-X backend")
    try:
        get_model()
        if os.getenv("MODEL_WARMUP", "true").lower() == "true":
            warmup_model()
    except Exception:
        logger.exception("Model startup failed")


@app.get("/health")
async def health_check():
    model = get_model()
    return {
        "success": True,
        "status": "running",
        "service": "SYNAPSE-X API",
        "model": model.metadata(),
    }


@app.get("/")
async def root():
    return {
        "success": True,
        "name": "SYNAPSE-X",
        "tagline": "AI-powered chest X-ray screening for pneumonia detection",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "api_health": "/api/health",
            "analyze_json": "/api/analyze",
            "predict_multipart": "/api/predict",
            "docs": "/docs",
        },
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP error on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": str(exc.detail), "details": None},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Request validation failed",
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("DEBUG", "true").lower() == "true",
    )
