from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime


class ActivityLog(BaseModel):
    """Schema for activity log entry"""
    user_id: str
    type: str
    details: Dict
    timestamp: str


class ActivityLogCreate(BaseModel):
    """Schema for creating an activity log"""
    type: str
    details: Dict
    user_id: Optional[str] = "default"


class ActivityStatsResponse(BaseModel):
    """Response schema for activity statistics"""
    total_activities: int
    by_type: Dict[str, int]


class RecentActivitiesResponse(BaseModel):
    """Response schema for recent activities"""
    activities: List[ActivityLog]
    total: int
