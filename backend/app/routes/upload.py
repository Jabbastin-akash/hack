from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io

from app.schemas.responses import PredictionResponse
from app.utils.file_validation import validate_file_type, validate_file_size
from app.utils.clip_inference import get_classifier
from app.utils.model_mapping import get_model_path

router = APIRouter()


@router.post("/upload-image", response_model=PredictionResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image and get a predicted 3D model based on CLIP classification.
    
    Args:
        file: Uploaded image file (PNG/JPG/JPEG)
        
    Returns:
        PredictionResponse with predicted subject, confidence, and model path
        
    Raises:
        HTTPException: If file validation fails or processing error occurs
    """
    # Validate file type
    validate_file_type(file.filename)
    
    # Read file contents
    try:
        contents = await file.read()
        validate_file_size(len(contents))
        
        # Load image with Pillow
        image = Image.open(io.BytesIO(contents))
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process image: {str(e)}"
        )
    
    # Get CLIP classifier and classify image
    try:
        classifier = get_classifier()
        predicted_label, confidence = classifier.classify_image(image)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )
    
    # Map label to 3D model path
    model_path = get_model_path(predicted_label)
    
    return {
        "predicted_subject": predicted_label,
        "confidence": round(confidence, 4),
        "model_path": model_path
    }
