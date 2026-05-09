"""Pydantic schemas shared by the API routes."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class ImagePayload(BaseModel):
    filename: str = Field(default="image.png", min_length=1, max_length=255)
    content_type: str = Field(default="image/png")
    data: str = Field(..., min_length=1, description="Base64 image bytes, optionally as a data URL")

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, value: str) -> str:
        allowed = {"image/jpeg", "image/jpg", "image/png"}
        normalized = value.lower()
        if normalized not in allowed:
            raise ValueError("content_type must be image/jpeg, image/jpg, or image/png")
        return normalized


class AnalyzeRequest(BaseModel):
    input: Optional[Union[str, List[str], Dict[str, Any]]] = None
    images: List[ImagePayload] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_input_or_images(self):
        if self.images or self.input is not None:
            return self
        raise ValueError("Request must include images or input")


class PredictionItem(BaseModel):
    filename: str
    prediction: str
    confidence: float
    probability_normal: float
    probability_pneumonia: float
    status: str = "success"
    error: Optional[str] = None


class PredictionResponse(BaseModel):
    success: bool
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    processing_time_ms: float
    predictions: List[PredictionItem]
    model: Dict[str, Any]


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Any] = None
