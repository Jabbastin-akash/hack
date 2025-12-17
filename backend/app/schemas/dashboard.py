from pydantic import BaseModel
from typing import List, Optional
from app.schemas.mcq import MCQQuestion
from app.schemas.activity import ActivityLog


class XPData(BaseModel):
    """Schema for XP data"""
    user_id: str
    xp: int
    level: int
    xp_to_next_level: int
    updated_at: Optional[str]


class XPAddResponse(BaseModel):
    """Response schema for adding XP"""
    user_id: str
    xp: int
    level: int
    xp_added: int
    reason: str
    level_up: bool
    xp_to_next_level: int


class RecommendationsResponse(BaseModel):
    """Response schema for topic recommendations"""
    recommended_topics: List[str]
    based_on: Optional[str] = None


class DashboardResponse(BaseModel):
    """Response schema for user dashboard"""
    streak: int
    xp: int
    level: int
    xp_to_next_level: int
    daily_mcqs: List[MCQQuestion]
    recent_activity: List[ActivityLog]
    recommended_topics: List[str]
    last_viewed_model: Optional[str] = None
    activity_stats: dict
