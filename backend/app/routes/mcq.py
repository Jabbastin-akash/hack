from fastapi import APIRouter, HTTPException
from app.schemas.mcq import (
    MCQQuestion,
    MCQSubmission,
    MCQResult,
    DailyMCQsResponse
)
from app.services.mcq_service import get_mcq_service
from app.services.xp_service import get_xp_service
from app.services.activity_service import get_activity_service
from app.services.streak_service import get_streak_service

router = APIRouter()


@router.get("/mcq/daily", response_model=DailyMCQsResponse)
async def get_daily_mcqs(subject: str = None, limit: int = 5):
    """
    Get daily MCQ questions.
    
    Args:
        subject: Optional subject filter
        limit: Maximum number of questions (default: 5)
        
    Returns:
        List of daily MCQ questions
    """
    try:
        mcq_service = get_mcq_service()
        questions = mcq_service.get_daily_mcqs(subject=subject, limit=limit)
        
        # Remove correct answers from response
        cleaned_questions = []
        for q in questions:
            cleaned_q = {
                "id": q["id"],
                "subject": q["subject"],
                "question": q["question"],
                "options": q["options"],
                "difficulty": q.get("difficulty", "medium")
            }
            cleaned_questions.append(cleaned_q)
        
        return {
            "questions": cleaned_questions,
            "total": len(cleaned_questions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get MCQs: {str(e)}")


@router.post("/user/mcq/submit", response_model=MCQResult)
async def submit_mcq_answer(submission: MCQSubmission, user_id: str = "default"):
    """
    Submit an MCQ answer and get validation result.
    
    Process:
    1. Validate answer
    2. Award XP if correct
    3. Update streak if applicable
    4. Log activity
    
    Args:
        submission: MCQ submission with question_id and selected_option
        user_id: User identifier (default: "default")
        
    Returns:
        Validation result with XP awarded and explanation
    """
    try:
        mcq_service = get_mcq_service()
        xp_service = get_xp_service()
        activity_service = get_activity_service()
        streak_service = get_streak_service()
        
        # Validate answer
        validation = mcq_service.validate_answer(
            submission.question_id,
            submission.selected_option
        )
        
        if not validation.get("valid"):
            raise HTTPException(status_code=404, detail=validation.get("error", "Invalid question"))
        
        is_correct = validation["correct"]
        xp_awarded = 0
        level_up = False
        
        if is_correct:
            # Award XP for correct answer
            xp_reward = xp_service.get_xp_reward("mcq_correct")
            xp_result = xp_service.add_xp(
                user_id=user_id,
                amount=xp_reward,
                reason=f"Correct answer on {submission.question_id}"
            )
            xp_awarded = xp_result["xp_added"]
            level_up = xp_result["level_up"]
            
            # Update streak
            streak_service.update_streak(user_id)
        
        # Log activity
        activity_service.log_activity(
            activity_type="completed_mcq",
            details={
                "question_id": submission.question_id,
                "subject": validation.get("subject", ""),
                "correct": is_correct,
                "xp_awarded": xp_awarded
            },
            user_id=user_id
        )
        
        return {
            "correct": is_correct,
            "xp_awarded": xp_awarded,
            "correct_answer": validation["correct_answer"],
            "selected_option": validation["selected_option"],
            "explanation": validation.get("explanation", ""),
            "level_up": level_up
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit MCQ: {str(e)}")


@router.get("/mcq/subject/{subject}")
async def get_mcqs_by_subject(subject: str):
    """
    Get all MCQs for a specific subject.
    
    Args:
        subject: Subject name
        
    Returns:
        List of MCQs for the subject
    """
    try:
        mcq_service = get_mcq_service()
        questions = mcq_service.get_questions_by_subject(subject)
        
        # Remove correct answers
        cleaned_questions = []
        for q in questions:
            cleaned_q = {
                "id": q["id"],
                "subject": q["subject"],
                "question": q["question"],
                "options": q["options"],
                "difficulty": q.get("difficulty", "medium")
            }
            cleaned_questions.append(cleaned_q)
        
        return {
            "subject": subject,
            "questions": cleaned_questions,
            "total": len(cleaned_questions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subject MCQs: {str(e)}")
