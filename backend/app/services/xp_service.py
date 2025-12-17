from typing import Dict
from app.utils.storage import get_storage
from datetime import datetime


class XPService:
    """
    Service for managing user XP (Experience Points) and leveling.
    
    Level Progression:
    - Level 1: 0 XP
    - Level 2: 50 XP
    - Level 3: 150 XP
    - Level 4: 300 XP
    - Level 5: 500 XP
    - And so on...
    """
    
    # XP thresholds for each level
    LEVEL_THRESHOLDS = [
        0,      # Level 1
        50,     # Level 2
        150,    # Level 3
        300,    # Level 4
        500,    # Level 5
        750,    # Level 6
        1050,   # Level 7
        1400,   # Level 8
        1800,   # Level 9
        2250,   # Level 10
    ]
    
    # XP rewards
    XP_REWARDS = {
        "mcq_correct": 10,
        "mcq_perfect": 25,
        "streak_milestone": 20,
        "model_viewed": 5,
        "daily_complete": 30
    }
    
    def __init__(self):
        self.storage = get_storage()
        self.filename = "xp.json"
    
    def get_xp_data(self, user_id: str = "default") -> dict:
        """
        Get XP and level data for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with xp, level, and level progress
        """
        data = self.storage.read(self.filename, default={})
        
        if user_id not in data:
            return {
                "user_id": user_id,
                "xp": 0,
                "level": 1,
                "xp_to_next_level": self.LEVEL_THRESHOLDS[1],
                "updated_at": None
            }
        
        user_data = data[user_id]
        level = self._calculate_level(user_data["xp"])
        xp_to_next = self._xp_to_next_level(level, user_data["xp"])
        
        return {
            "user_id": user_id,
            "xp": user_data["xp"],
            "level": level,
            "xp_to_next_level": xp_to_next,
            "updated_at": user_data.get("updated_at")
        }
    
    def add_xp(self, user_id: str = "default", amount: int = 0, reason: str = "") -> dict:
        """
        Add XP to a user.
        
        Args:
            user_id: User identifier
            amount: Amount of XP to add
            reason: Reason for XP award
            
        Returns:
            Updated XP data with level_up flag
        """
        data = self.storage.read(self.filename, default={})
        
        # Get current XP
        if user_id not in data:
            current_xp = 0
            old_level = 1
        else:
            current_xp = data[user_id].get("xp", 0)
            old_level = self._calculate_level(current_xp)
        
        # Add XP
        new_xp = current_xp + amount
        new_level = self._calculate_level(new_xp)
        
        # Save updated data
        data[user_id] = {
            "user_id": user_id,
            "xp": new_xp,
            "level": new_level,
            "updated_at": datetime.utcnow().isoformat()
        }
        self.storage.write(self.filename, data)
        
        return {
            "user_id": user_id,
            "xp": new_xp,
            "level": new_level,
            "xp_added": amount,
            "reason": reason,
            "level_up": new_level > old_level,
            "xp_to_next_level": self._xp_to_next_level(new_level, new_xp)
        }
    
    def _calculate_level(self, xp: int) -> int:
        """Calculate level based on XP."""
        level = 1
        for threshold in self.LEVEL_THRESHOLDS:
            if xp >= threshold:
                level = self.LEVEL_THRESHOLDS.index(threshold) + 1
            else:
                break
        
        # Handle levels beyond predefined thresholds
        if xp >= self.LEVEL_THRESHOLDS[-1]:
            level = len(self.LEVEL_THRESHOLDS)
            # Simple formula for higher levels
            remaining_xp = xp - self.LEVEL_THRESHOLDS[-1]
            level += remaining_xp // 500
        
        return level
    
    def _xp_to_next_level(self, level: int, current_xp: int) -> int:
        """Calculate XP needed for next level."""
        if level < len(self.LEVEL_THRESHOLDS):
            return self.LEVEL_THRESHOLDS[level] - current_xp
        else:
            # For levels beyond predefined, use formula
            next_threshold = self.LEVEL_THRESHOLDS[-1] + ((level - len(self.LEVEL_THRESHOLDS) + 1) * 500)
            return next_threshold - current_xp
    
    def get_xp_reward(self, action: str) -> int:
        """
        Get XP reward amount for an action.
        
        Args:
            action: Action type (mcq_correct, streak_milestone, etc.)
            
        Returns:
            XP amount
        """
        return self.XP_REWARDS.get(action, 0)


# Global service instance
_xp_service: XPService = None


def get_xp_service() -> XPService:
    """Get the global XP service instance."""
    global _xp_service
    if _xp_service is None:
        _xp_service = XPService()
    return _xp_service
