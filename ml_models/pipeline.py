"""
Integration example: Combining classifier and content mapper
for end-to-end educational diagram processing.
"""

import sys
import json
from pathlib import Path
from ml_models.classify import EducationalSubjectClassifier
from ml_models.content_mapper import ContentMapper


class EduLensIntelligence:
    """
    Main intelligence system combining classification and content mapping.
    """
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialize the intelligence system.
        
        Args:
            confidence_threshold: Minimum confidence for automatic recommendations
        """
        print("🚀 Initializing Edulens Intelligence System...")
        self.classifier = EducationalSubjectClassifier()
        self.mapper = ContentMapper()
        self.confidence_threshold = confidence_threshold
        print("✅ System ready!\n")
    
    def process_image(self, image_path: str, user_query: str = None) -> dict:
        """
        Complete processing pipeline: classify image and recommend 3D content.
        
        Args:
            image_path: Path to educational diagram
            user_query: Optional user query for context
            
        Returns:
            Complete recommendation with classification and 3D model info
        """
        # Step 1: Classify the image
        print(f"📸 Classifying: {image_path}")
        classification = self.classifier.classify_image(image_path, top_k=3)
        
        subject = classification['predicted_subject']
        confidence = classification['confidence']
        
        print(f"🎯 Detected: {subject} (confidence: {confidence:.2%})")
        
        # Step 2: Get 3D model recommendation
        if confidence >= self.confidence_threshold:
            recommendation = self.mapper.get_recommendation(subject)
            status = "high_confidence"
            message = "Automatic recommendation"
        else:
            recommendation = self.mapper.get_recommendation(subject)
            status = "low_confidence"
            message = "Manual review recommended"
        
        # Step 3: Build complete response
        response = {
            "status": status,
            "message": message,
            "classification": {
                "subject": subject,
                "confidence": confidence,
                "top_predictions": classification['top_predictions']
            },
            "recommendation": recommendation,
            "user_query": user_query
        }
        
        return response
    
    def explain_recommendation(self, response: dict) -> str:
        """
        Generate human-readable explanation of the recommendation.
        
        Args:
            response: Response from process_image()
            
        Returns:
            Formatted explanation string
        """
        classification = response['classification']
        recommendation = response['recommendation']
        
        explanation = f"""
╔══════════════════════════════════════════════════════════════╗
║           EDULENS INTELLIGENCE RECOMMENDATION                ║
╚══════════════════════════════════════════════════════════════╝

📊 CLASSIFICATION RESULTS
  Subject: {classification['subject']}
  Confidence: {classification['confidence']:.1%}
  
  Top 3 Predictions:
"""
        
        for i, pred in enumerate(classification['top_predictions'], 1):
            explanation += f"    {i}. {pred['subject']:20s} - {pred['confidence']:.1%}\n"
        
        if recommendation['status'] == 'success':
            explanation += f"""
🎬 3D MODEL RECOMMENDATION
  Display Name: {recommendation['display_name']}
  Model File: {recommendation['model_file']}
  Category: {recommendation['category']}
  Difficulty: {recommendation['difficulty']}
  
  Available Animations:
"""
            for anim in recommendation['animations']:
                explanation += f"    • {anim}\n"
            
            explanation += f"""
  Interactive Features:
"""
            for feature in recommendation['interactive_features']:
                explanation += f"    • {feature}\n"
            
            explanation += f"""
📚 DESCRIPTION
  {recommendation['description']}
  
🏷️  TAGS
  {', '.join(recommendation['educational_tags'])}
  
👥 RECOMMENDED FOR
  {recommendation['recommended_age']}
"""
        else:
            explanation += f"""
⚠️  NO MODEL FOUND
  The subject "{classification['subject']}" was detected, but no 3D model
  is currently available in the database.
"""
        
        explanation += "\n" + "═" * 64 + "\n"
        
        return explanation
    
    def batch_process(self, image_paths: list) -> list:
        """
        Process multiple images in batch.
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of responses for each image
        """
        results = []
        
        print(f"\n🔄 Processing {len(image_paths)} images...\n")
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"[{i}/{len(image_paths)}] Processing: {Path(image_path).name}")
            
            try:
                response = self.process_image(image_path)
                results.append(response)
                print(f"  ✅ Success - {response['classification']['subject']}\n")
            except Exception as e:
                print(f"  ❌ Error: {str(e)}\n")
                results.append({
                    "status": "error",
                    "image_path": image_path,
                    "error": str(e)
                })
        
        return results


def main():
    """Demo and command-line interface."""
    
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════╗
║              EDULENS INTELLIGENCE SYSTEM v1.0                ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  python pipeline.py <image_path> [--query "optional question"]
  
Examples:
  python pipeline.py data/biology/heart.jpg
  python pipeline.py data/chemistry/h2o.png --query "Show me molecular structure"
  
Features:
  • CLIP-based subject classification
  • 20+ educational subjects
  • Automatic 3D model recommendations
  • Confidence scoring
  • Animation suggestions
        """)
        return
    
    # Parse arguments
    image_path = sys.argv[1]
    user_query = None
    
    if "--query" in sys.argv:
        query_idx = sys.argv.index("--query")
        if query_idx + 1 < len(sys.argv):
            user_query = sys.argv[query_idx + 1]
    
    # Initialize system
    system = EduLensIntelligence(confidence_threshold=0.6)
    
    # Process image
    try:
        response = system.process_image(image_path, user_query)
        
        # Display results
        explanation = system.explain_recommendation(response)
        print(explanation)
        
        # Save JSON output
        output_path = Path(image_path).stem + "_recommendation.json"
        with open(output_path, 'w') as f:
            json.dump(response, f, indent=2)
        
        print(f"💾 Full response saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
