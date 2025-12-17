from typing import List, Dict
from app.utils.storage import get_storage


class RecommendationService:
    """
    Service for providing topic recommendations.
    
    This is a simple rule-based recommendation system.
    Future versions may integrate with AI models.
    """
    
    # Simple recommendation mapping
    RECOMMENDATIONS = {
        "heart": ["arteries", "veins", "circulatory system", "blood flow"],
        "dna": ["rna", "protein synthesis", "genetics", "chromosomes"],
        "cell": ["mitochondria", "nucleus", "cell membrane", "organelles"],
        "atom": ["electron", "proton", "neutron", "periodic table"],
        "lever": ["pulley", "inclined plane", "simple machines", "mechanical advantage"],
        "pendulum": ["oscillation", "simple harmonic motion", "energy conservation", "waves"],
        "ac circuit": ["dc circuit", "capacitor", "inductor", "ohm's law"]
    }
    
    def __init__(self):
        self.storage = get_storage()
    
    def get_recommendations(
        self,
        based_on: str = None,
        user_id: str = "default"
    ) -> List[str]:
        """
        Get topic recommendations.
        
        Args:
            based_on: Topic to base recommendations on
            user_id: User identifier
            
        Returns:
            List of recommended topics
        """
        if based_on and based_on.lower() in self.RECOMMENDATIONS:
            return self.RECOMMENDATIONS[based_on.lower()]
        
        # If no specific topic, get from recent activity
        recent_topics = self._get_recent_topics(user_id)
        
        if recent_topics:
            # Get recommendations based on most recent topic
            last_topic = recent_topics[0].lower()
            if last_topic in self.RECOMMENDATIONS:
                return self.RECOMMENDATIONS[last_topic]
        
        # Default recommendations
        return ["heart", "dna", "cell", "atom"]
    
    def _get_recent_topics(self, user_id: str) -> List[str]:
        """Get recently viewed topics from activity logs."""
        logs = self.storage.read("activity_logs.json", default=[])
        
        user_logs = [
            log for log in logs
            if log.get("user_id") == user_id and log.get("type") == "viewed_model"
        ]
        
        # Extract topics from recent activities
        topics = []
        for log in user_logs[-5:]:  # Last 5 activities
            details = log.get("details", {})
            model = details.get("model", "")
            if model:
                # Extract topic from model filename (e.g., "heart.glb" -> "heart")
                topic = model.replace(".glb", "").replace("_", " ")
                topics.append(topic)
        
        return topics
    
    def get_related_subjects(self, subject: str) -> List[str]:
        """
        Get related subjects for cross-topic learning.
        
        Args:
            subject: Current subject
            
        Returns:
            List of related subjects
        """
        # Subject groupings
        biology_topics = ["heart", "dna", "cell"]
        physics_topics = ["atom", "lever", "pendulum", "ac circuit"]
        
        if subject in biology_topics:
            return [t for t in biology_topics if t != subject]
        elif subject in physics_topics:
            return [t for t in physics_topics if t != subject]
        
        return []


# Global service instance
_recommendation_service: RecommendationService = None


def get_recommendation_service() -> RecommendationService:
    """Get the global recommendation service instance."""
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = RecommendationService()
    return _recommendation_service
