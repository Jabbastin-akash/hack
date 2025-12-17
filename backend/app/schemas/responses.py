from pydantic import BaseModel


class PredictionResponse(BaseModel):
    """Response schema for image classification predictions"""
    predicted_subject: str
    confidence: float
    model_path: str


class HealthResponse(BaseModel):
    """Response schema for health check"""
    status: str
    message: str


class ErrorResponse(BaseModel):
    """Response schema for errors"""
    detail: str
