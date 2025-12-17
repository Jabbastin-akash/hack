from fastapi import APIRouter
from app.schemas.responses import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        JSON response with status and message
    """
    return {
        "status": "healthy",
        "message": "Image to 3D Model API is running"
    }
