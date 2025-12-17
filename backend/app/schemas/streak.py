from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StreakResponse(BaseModel):
    """Response schema for streak data"""
    user_id: str
    streak: int
    last_active: Optional[str]
    updated_at: Optional[str]


class StreakUpdateResponse(BaseModel):
    """Response schema for streak update"""
    user_id: str
    streak: int
    last_active: str
    updated_at: str
    message: str
