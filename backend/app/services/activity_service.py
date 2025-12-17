from typing import Dict, List
from datetime import datetime
from app.utils.storage import get_storage


class ActivityService:
    """
    Service for logging and retrieving user activities.
    
    Activity Types:
    - viewed_model: User viewed a 3D model
    - classified_image: User uploaded and classified an image
    - completed_mcq: User completed an MCQ
    - unlocked_badge: User unlocked an achievement
    - completed_streak: User maintained streak
    - level_up: User leveled up
    """
    
    def __init__(self):
        self.storage = get_storage()
        self.filename = "activity_logs.json"
    
    def log_activity(
        self,
        activity_type: str,
        details: Dict,
        user_id: str = "default"
    ) -> bool:
        """
        Log a user activity.
        
        Args:
            activity_type: Type of activity
            details: Activity details
            user_id: User identifier
            
        Returns:
            True if successful
        """
        entry = {
            "user_id": user_id,
            "type": activity_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return self.storage.append_log(self.filename, entry)
    
    def get_recent_activities(
        self,
        user_id: str = "default",
        limit: int = 10
    ) -> List[Dict]:
        """
        Get recent activities for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of activities
            
        Returns:
            List of recent activities
        """
        all_logs = self.storage.read(self.filename, default=[])
        
        # Filter by user
        user_logs = [log for log in all_logs if log.get("user_id") == user_id]
        
        # Sort by timestamp (most recent first)
        user_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return user_logs[:limit]
    
    def get_activities_by_type(
        self,
        activity_type: str,
        user_id: str = "default",
        limit: int = 10
    ) -> List[Dict]:
        """
        Get activities of a specific type.
        
        Args:
            activity_type: Type of activity
            user_id: User identifier
            limit: Maximum number of activities
            
        Returns:
            List of filtered activities
        """
        all_logs = self.storage.read(self.filename, default=[])
        
        # Filter by user and type
        filtered_logs = [
            log for log in all_logs
            if log.get("user_id") == user_id and log.get("type") == activity_type
        ]
        
        # Sort by timestamp (most recent first)
        filtered_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return filtered_logs[:limit]
    
    def get_activity_stats(self, user_id: str = "default") -> Dict:
        """
        Get activity statistics for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with activity counts by type
        """
        all_logs = self.storage.read(self.filename, default=[])
        user_logs = [log for log in all_logs if log.get("user_id") == user_id]
        
        stats = {}
        for log in user_logs:
            activity_type = log.get("type", "unknown")
            stats[activity_type] = stats.get(activity_type, 0) + 1
        
        return {
            "total_activities": len(user_logs),
            "by_type": stats
        }


# Global service instance
_activity_service: ActivityService = None


def get_activity_service() -> ActivityService:
    """Get the global activity service instance."""
    global _activity_service
    if _activity_service is None:
        _activity_service = ActivityService()
    return _activity_service
