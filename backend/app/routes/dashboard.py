from fastapi import APIRouter, HTTPException
from app.schemas.dashboard import (
    DashboardResponse,
    XPData,
    RecommendationsResponse
)
from app.services.streak_service import get_streak_service
from app.services.xp_service import get_xp_service
from app.services.mcq_service import get_mcq_service
from app.services.activity_service import get_activity_service
from app.services.recommendation_service import get_recommendation_service

router = APIRouter()


@router.get("/user/dashboard", response_model=DashboardResponse)
async def get_dashboard(user_id: str = "default"):
    """
    Get aggregated dashboard data for a user.
    
    Returns:
    - Streak count
    - XP and level
    - Daily MCQs
    - Recent activity logs
    - Recommended topics
    - Last viewed 3D model
    - Activity statistics
    
    Args:
        user_id: User identifier (default: "default")
        
    Returns:
        Complete dashboard data
    """
    try:
        # Get services
        streak_service = get_streak_service()
        xp_service = get_xp_service()
        mcq_service = get_mcq_service()
        activity_service = get_activity_service()
        recommendation_service = get_recommendation_service()
        
        # Gather all data
        streak_data = streak_service.get_streak(user_id)
        xp_data = xp_service.get_xp_data(user_id)
        daily_mcqs = mcq_service.get_daily_mcqs(limit=5)
        recent_activities = activity_service.get_recent_activities(user_id, limit=10)
        activity_stats = activity_service.get_activity_stats(user_id)
        recommendations = recommendation_service.get_recommendations(user_id=user_id)
        
        # Get last viewed model
        last_viewed_model = None
        viewed_activities = [
            a for a in recent_activities
            if a.get("type") == "viewed_model"
        ]
        if viewed_activities:
            last_viewed_model = viewed_activities[0].get("details", {}).get("model")
        
        # Clean MCQ questions (remove answers)
        cleaned_mcqs = []
        for q in daily_mcqs:
            cleaned_q = {
                "id": q["id"],
                "subject": q["subject"],
                "question": q["question"],
                "options": q["options"],
                "difficulty": q.get("difficulty", "medium")
            }
            cleaned_mcqs.append(cleaned_q)
        
        return {
            "streak": streak_data.get("streak", 0),
            "xp": xp_data["xp"],
            "level": xp_data["level"],
            "xp_to_next_level": xp_data["xp_to_next_level"],
            "daily_mcqs": cleaned_mcqs,
            "recent_activity": recent_activities,
            "recommended_topics": recommendations,
            "last_viewed_model": last_viewed_model,
            "activity_stats": activity_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dashboard: {str(e)}")


@router.get("/user/xp", response_model=XPData)
async def get_xp(user_id: str = "default"):
    """
    Get XP and level data for a user.
    
    Args:
        user_id: User identifier (default: "default")
        
    Returns:
        XP and level information
    """
    try:
        xp_service = get_xp_service()
        xp_data = xp_service.get_xp_data(user_id)
        return xp_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get XP data: {str(e)}")


@router.get("/user/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(based_on: str = None, user_id: str = "default"):
    """
    Get topic recommendations for a user.
    
    Uses simple logic:
    - If user viewed "heart" → recommend "arteries", "veins"
    - If user studied "physics" → recommend related physics topics
    
    Args:
        based_on: Optional topic to base recommendations on
        user_id: User identifier (default: "default")
        
    Returns:
        List of recommended topics
    """
    try:
        recommendation_service = get_recommendation_service()
        recommendations = recommendation_service.get_recommendations(
            based_on=based_on,
            user_id=user_id
        )
        
        return {
            "recommended_topics": recommendations,
            "based_on": based_on
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")
