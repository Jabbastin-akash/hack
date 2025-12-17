from fastapi import HTTPException
from typing import BinaryIO


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file_type(filename: str) -> None:
    """
    Validate that the uploaded file has an allowed extension.
    
    Args:
        filename: Name of the uploaded file
        
    Raises:
        HTTPException: If file type is not allowed
    """
    if '.' not in filename:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )


def validate_file_size(file_size: int) -> None:
    """
    Validate that the uploaded file size is within limits.
    
    Args:
        file_size: Size of the uploaded file in bytes
        
    Raises:
        HTTPException: If file size exceeds maximum
    """
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB"
        )
