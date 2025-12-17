from pydantic import BaseModel, Field
from typing import List, Optional


class MCQOption(BaseModel):
    """Schema for MCQ option"""
    label: str
    text: str


class MCQQuestion(BaseModel):
    """Schema for MCQ question"""
    id: str
    subject: str
    question: str
    options: List[MCQOption]
    difficulty: Optional[str] = "medium"


class MCQQuestionWithAnswer(MCQQuestion):
    """Schema for MCQ question with answer (admin only)"""
    correct_answer: str
    explanation: Optional[str] = ""


class MCQSubmission(BaseModel):
    """Schema for MCQ answer submission"""
    question_id: str
    selected_option: str = Field(..., pattern="^[A-D]$")


class MCQResult(BaseModel):
    """Schema for MCQ validation result"""
    correct: bool
    xp_awarded: int
    correct_answer: str
    selected_option: str
    explanation: Optional[str] = ""
    level_up: Optional[bool] = False


class DailyMCQsResponse(BaseModel):
    """Response schema for daily MCQs"""
    questions: List[MCQQuestion]
    total: int
