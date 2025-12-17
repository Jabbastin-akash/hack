from typing import List, Dict, Optional
from datetime import datetime
from app.utils.storage import get_storage


class MCQService:
    """
    Service for managing Multiple Choice Questions (MCQs).
    Handles question retrieval, validation, and scoring.
    """
    
    def __init__(self):
        self.storage = get_storage()
        self.filename = "mcqs.json"
    
    def get_daily_mcqs(self, subject: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """
        Get daily MCQ questions.
        
        Args:
            subject: Optional subject filter
            limit: Maximum number of questions
            
        Returns:
            List of MCQ questions
        """
        all_mcqs = self.storage.read(self.filename, default={"questions": []})
        questions = all_mcqs.get("questions", [])
        
        # Filter by subject if provided
        if subject:
            questions = [q for q in questions if q.get("subject") == subject]
        
        # Return limited set
        return questions[:limit]
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """
        Get a specific question by ID.
        
        Args:
            question_id: Question identifier
            
        Returns:
            Question dict or None
        """
        all_mcqs = self.storage.read(self.filename, default={"questions": []})
        questions = all_mcqs.get("questions", [])
        
        for question in questions:
            if question.get("id") == question_id:
                return question
        
        return None
    
    def validate_answer(self, question_id: str, selected_option: str) -> Dict:
        """
        Validate an answer to a question.
        
        Args:
            question_id: Question identifier
            selected_option: Selected option (A, B, C, D)
            
        Returns:
            Validation result with correct answer and explanation
        """
        question = self.get_question_by_id(question_id)
        
        if not question:
            return {
                "valid": False,
                "error": "Question not found"
            }
        
        correct_answer = question.get("correct_answer")
        is_correct = selected_option == correct_answer
        
        return {
            "valid": True,
            "correct": is_correct,
            "correct_answer": correct_answer,
            "selected_option": selected_option,
            "explanation": question.get("explanation", ""),
            "subject": question.get("subject", "")
        }
    
    def get_questions_by_subject(self, subject: str) -> List[Dict]:
        """
        Get all questions for a specific subject.
        
        Args:
            subject: Subject name
            
        Returns:
            List of questions
        """
        all_mcqs = self.storage.read(self.filename, default={"questions": []})
        questions = all_mcqs.get("questions", [])
        
        return [q for q in questions if q.get("subject") == subject]
    
    def add_question(self, question: Dict) -> bool:
        """
        Add a new question to the MCQ database.
        
        Args:
            question: Question dictionary
            
        Returns:
            True if successful
        """
        all_mcqs = self.storage.read(self.filename, default={"questions": []})
        
        if "questions" not in all_mcqs:
            all_mcqs["questions"] = []
        
        # Add timestamp
        question["created_at"] = datetime.utcnow().isoformat()
        
        all_mcqs["questions"].append(question)
        return self.storage.write(self.filename, all_mcqs)


# Global service instance
_mcq_service: MCQService = None


def get_mcq_service() -> MCQService:
    """Get the global MCQ service instance."""
    global _mcq_service
    if _mcq_service is None:
        _mcq_service = MCQService()
    return _mcq_service
