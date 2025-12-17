from fastapi import APIRouter, HTTPException
from app.schemas.activity import (
    ActivityLogCreate,
    ActivityStatsResponse,
    RecentActivitiesResponse
)
from app.services.activity_service import get_activity_service

router = APIRouter()


@router.post("/user/activity/log")
async def log_activity(activity: ActivityLogCreate):
    """
    Log a user activity.
    
    Activity Types:
    - viewed_model: User viewed a 3D model
    - classified_image: User uploaded and classified an image
    - completed_mcq: User completed an MCQ
    - unlocked_badge: User unlocked an achievement
    - completed_streak: User maintained streak
    - level_up: User leveled up
    
    Args:
        activity: Activity log data
        
    Returns:
        Success message
    """
    try:
        activity_service = get_activity_service()
        success = activity_service.log_activity(
            activity_type=activity.type,
            details=activity.details,
            user_id=activity.user_id
        )
        
        if success:
            return {
                "success": True,
                "message": "Activity logged successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to log activity")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log activity: {str(e)}")


@router.get("/user/activity/recent", response_model=RecentActivitiesResponse)
async def get_recent_activities(user_id: str = "default", limit: int = 10):
    """
    Get recent activities for a user.
    
    Args:
        user_id: User identifier (default: "default")
        limit: Maximum number of activities (default: 10)
        
    Returns:
        List of recent activities
    """
    try:
        activity_service = get_activity_service()
        activities = activity_service.get_recent_activities(user_id=user_id, limit=limit)
        
        return {
            "activities": activities,
            "total": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get activities: {str(e)}")


@router.get("/user/activity/stats", response_model=ActivityStatsResponse)
async def get_activity_stats(user_id: str = "default"):
    """
    Get activity statistics for a user.
    
    Args:
        user_id: User identifier (default: "default")
        
    Returns:
        Activity statistics by type
    """
    try:
        activity_service = get_activity_service()
        stats = activity_service.get_activity_stats(user_id=user_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/user/activity/type/{activity_type}")
async def get_activities_by_type(
    activity_type: str,
    user_id: str = "default",
    limit: int = 10
):
    """
    Get activities of a specific type.
    
    Args:
        activity_type: Type of activity
        user_id: User identifier (default: "default")
        limit: Maximum number of activities (default: 10)
        
    Returns:
        List of filtered activities
    """
    try:
        activity_service = get_activity_service()
        activities = activity_service.get_activities_by_type(
            activity_type=activity_type,
            user_id=user_id,
            limit=limit
        )
        
        return {
            "activity_type": activity_type,
            "activities": activities,
            "total": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get activities: {str(e)}")
