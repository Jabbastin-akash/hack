"""
3D Content Mapping System
Links predicted subjects to 3D GLB models with metadata.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class ContentMapper:
    """
    Maps educational subjects to 3D content and metadata.
    Provides utilities for content retrieval and management.
    """
    
    def __init__(self, metadata_path: str = None):
        """
        Initialize the content mapper.
        
        Args:
            metadata_path: Path to model_metadata.json. Auto-detected if None.
        """
        if metadata_path is None:
            # Default path relative to project root
            project_root = Path(__file__).parent.parent
            metadata_path = project_root / "config" / "model_metadata.json"
        
        self.metadata_path = Path(metadata_path)
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict:
        """Load metadata from JSON file."""
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")
        
        with open(self.metadata_path, 'r') as f:
            return json.load(f)
    
    def get_model_info(self, subject: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve 3D model metadata for a given subject.
        
        Args:
            subject: Subject identifier (e.g., 'heart', 'dna')
            
        Returns:
            Dictionary with model metadata or None if not found
        """
        return self.metadata.get("subjects", {}).get(subject)
    
    def get_model_file(self, subject: str) -> Optional[str]:
        """
        Get the GLB filename for a subject.
        
        Args:
            subject: Subject identifier
            
        Returns:
            GLB filename or None if not found
        """
        info = self.get_model_info(subject)
        return info.get("file") if info else None
    
    def get_animations(self, subject: str) -> List[str]:
        """
        Get available animations for a subject.
        
        Args:
            subject: Subject identifier
            
        Returns:
            List of animation names
        """
        info = self.get_model_info(subject)
        return info.get("animations", []) if info else []
    
    def get_by_category(self, category: str) -> Dict[str, Dict]:
        """
        Get all subjects in a specific category.
        
        Args:
            category: Category name (e.g., 'biology', 'chemistry', 'physics')
            
        Returns:
            Dictionary of subjects in that category
        """
        subjects = self.metadata.get("subjects", {})
        return {
            subject: data
            for subject, data in subjects.items()
            if data.get("subject_category") == category
        }
    
    def get_by_difficulty(self, level: str) -> Dict[str, Dict]:
        """
        Get subjects by difficulty level.
        
        Args:
            level: Difficulty level ('beginner', 'intermediate', 'advanced')
            
        Returns:
            Dictionary of subjects at that difficulty
        """
        subjects = self.metadata.get("subjects", {})
        return {
            subject: data
            for subject, data in subjects.items()
            if data.get("difficulty_level") == level
        }
    
    def search_by_tag(self, tag: str) -> Dict[str, Dict]:
        """
        Search subjects by educational tag.
        
        Args:
            tag: Educational tag to search for
            
        Returns:
            Dictionary of matching subjects
        """
        subjects = self.metadata.get("subjects", {})
        return {
            subject: data
            for subject, data in subjects.items()
            if tag.lower() in [t.lower() for t in data.get("educational_tags", [])]
        }
    
    def get_recommendation(
        self,
        subject: str,
        min_confidence: float = 0.5,
        prefer_difficulty: str = None
    ) -> Dict[str, Any]:
        """
        Get content recommendation based on classification result.
        
        Args:
            subject: Predicted subject
            min_confidence: Minimum confidence threshold
            prefer_difficulty: Preferred difficulty level filter
            
        Returns:
            Recommendation dictionary with model info and metadata
        """
        info = self.get_model_info(subject)
        
        if not info:
            return {
                "status": "not_found",
                "subject": subject,
                "message": f"No 3D model available for subject: {subject}"
            }
        
        # Check if difficulty matches preference
        difficulty_match = True
        if prefer_difficulty:
            difficulty_match = info.get("difficulty_level") == prefer_difficulty
        
        return {
            "status": "success",
            "subject": subject,
            "model_file": info["file"],
            "display_name": info["display_name"],
            "category": info["subject_category"],
            "difficulty": info["difficulty_level"],
            "difficulty_matches_preference": difficulty_match,
            "animations": info.get("animations", []),
            "interactive_features": info.get("interactive_features", []),
            "description": info.get("description", ""),
            "educational_tags": info.get("educational_tags", []),
            "recommended_age": info.get("recommended_age", "N/A")
        }
    
    def get_all_subjects(self) -> List[str]:
        """Get list of all available subjects."""
        return list(self.metadata.get("subjects", {}).keys())
    
    def get_categories(self) -> Dict[str, Dict]:
        """Get information about all subject categories."""
        return self.metadata.get("category_info", {})
    
    def export_subject_list(self, output_path: str):
        """
        Export a simplified subject list for reference.
        
        Args:
            output_path: Path to save the subject list
        """
        subjects = self.metadata.get("subjects", {})
        
        subject_list = []
        for subject, data in subjects.items():
            subject_list.append({
                "id": subject,
                "name": data["display_name"],
                "category": data["subject_category"],
                "model": data["file"],
                "difficulty": data["difficulty_level"]
            })
        
        with open(output_path, 'w') as f:
            json.dump(subject_list, f, indent=2)
        
        print(f"Exported {len(subject_list)} subjects to {output_path}")


def main():
    """Example usage and testing."""
    import sys
    
    # Initialize mapper
    mapper = ContentMapper()
    
    if len(sys.argv) > 1:
        subject = sys.argv[1]
        
        # Get model info
        info = mapper.get_model_info(subject)
        
        if info:
            print(f"\n{'='*60}")
            print(f"3D MODEL INFO: {subject}")
            print('='*60)
            print(f"Display Name: {info['display_name']}")
            print(f"File: {info['file']}")
            print(f"Category: {info['subject_category']}")
            print(f"Difficulty: {info['difficulty_level']}")
            print(f"\nAnimations: {', '.join(info['animations'])}")
            print(f"\nInteractive Features: {', '.join(info['interactive_features'])}")
            print(f"\nDescription: {info['description']}")
            print(f"\nTags: {', '.join(info['educational_tags'])}")
        else:
            print(f"Subject '{subject}' not found in metadata.")
    else:
        # List all subjects
        print("\nAvailable Subjects:")
        print("="*60)
        
        categories = {}
        for subject in mapper.get_all_subjects():
            info = mapper.get_model_info(subject)
            category = info['subject_category']
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'id': subject,
                'name': info['display_name']
            })
        
        for category, items in sorted(categories.items()):
            print(f"\n{category.upper()}:")
            for item in items:
                print(f"  - {item['id']:20s} → {item['name']}")


if __name__ == "__main__":
    main()
