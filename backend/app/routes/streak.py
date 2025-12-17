from fastapi import APIRouter, HTTPException
from app.schemas.streak import StreakResponse, StreakUpdateResponse
from app.services.streak_service import get_streak_service

router = APIRouter()


@router.get("/user/streak", response_model=StreakResponse)
async def get_streak(user_id: str = "default"):
    """
    Get current streak for a user.
    
    Args:
        user_id: User identifier (default: "default")
        
    Returns:
        Current streak data
    """
    try:
        streak_service = get_streak_service()
        streak_data = streak_service.get_streak(user_id)
        return streak_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get streak: {str(e)}")


@router.post("/user/streak/update", response_model=StreakUpdateResponse)
async def update_streak(user_id: str = "default"):
    """
    Update streak based on current activity.
    
    Streak Rules:
    - If last_active == today → streak unchanged
    - If last_active == yesterday → streak++
    - Else → streak = 1
    
    Args:
        user_id: User identifier (default: "default")
        
    Returns:
        Updated streak data
    """
    try:
        streak_service = get_streak_service()
        streak_data = streak_service.update_streak(user_id)
        
        # Determine message based on streak
        if streak_data["streak"] == 1:
            message = "Streak started!"
        else:
            message = f"Streak maintained: {streak_data['streak']} days!"
        
        return {
            **streak_data,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update streak: {str(e)}")


@router.post("/user/streak/reset", response_model=StreakResponse)
async def reset_streak(user_id: str = "default"):
    """
    Reset streak to 0 (for testing or admin purposes).
    
    Args:
        user_id: User identifier (default: "default")
        
    Returns:
        Reset streak data
    """
    try:
        streak_service = get_streak_service()
        streak_data = streak_service.reset_streak(user_id)
        return streak_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset streak: {str(e)}")
