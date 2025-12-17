from datetime import datetime, timedelta
from app.utils.storage import get_storage


class StreakService:
    """
    Service for managing user streak tracking.
    
    Streak Rules:
    - If last_active == today → streak unchanged
    - If last_active == yesterday → streak++
    - Else → streak = 1
    """
    
    def __init__(self):
        self.storage = get_storage()
        self.filename = "streak.json"
    
    def get_streak(self, user_id: str = "default") -> dict:
        """
        Get current streak for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with streak, last_active, and updated_at
        """
        data = self.storage.read(self.filename, default={})
        
        if user_id not in data:
            return {
                "user_id": user_id,
                "streak": 0,
                "last_active": None,
                "updated_at": None
            }
        
        return data[user_id]
    
    def update_streak(self, user_id: str = "default") -> dict:
        """
        Update streak based on last activity.
        
        Args:
            user_id: User identifier
            
        Returns:
            Updated streak data
        """
        data = self.storage.read(self.filename, default={})
        today = datetime.utcnow().date()
        
        # Get existing streak data
        if user_id not in data:
            user_data = {
                "user_id": user_id,
                "streak": 1,
                "last_active": today.isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        else:
            user_data = data[user_id]
            last_active = datetime.fromisoformat(user_data["last_active"]).date() if user_data.get("last_active") else None
            
            if last_active is None:
                # First time
                user_data["streak"] = 1
            elif last_active == today:
                # Already active today, no change
                pass
            elif last_active == today - timedelta(days=1):
                # Active yesterday, increment streak
                user_data["streak"] += 1
            else:
                # Streak broken, reset to 1
                user_data["streak"] = 1
            
            user_data["last_active"] = today.isoformat()
            user_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Save updated data
        data[user_id] = user_data
        self.storage.write(self.filename, data)
        
        return user_data
    
    def reset_streak(self, user_id: str = "default") -> dict:
        """
        Reset streak to 0 (for testing or admin purposes).
        
        Args:
            user_id: User identifier
            
        Returns:
            Reset streak data
        """
        data = self.storage.read(self.filename, default={})
        
        user_data = {
            "user_id": user_id,
            "streak": 0,
            "last_active": None,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        data[user_id] = user_data
        self.storage.write(self.filename, data)
        
        return user_data


# Global service instance
_streak_service: StreakService = None


def get_streak_service() -> StreakService:
    """Get the global streak service instance."""
    global _streak_service
    if _streak_service is None:
        _streak_service = StreakService()
    return _streak_service
