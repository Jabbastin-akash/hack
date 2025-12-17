"""
CLIP-based Educational Content Classifier
Uses OpenAI's CLIP model to identify educational subjects from 2D diagrams.
"""

import torch
import clip
from PIL import Image
import json
from typing import Dict, List, Tuple
import numpy as np


class EducationalSubjectClassifier:
    """
    Classifies educational diagrams into predefined subject categories
    using CLIP (ViT-B/32) for zero-shot image classification.
    """
    
    # Educational subject taxonomy
    SUBJECT_LABELS = [
        "anatomical heart",
        "human cell",
        "double helix DNA",
        "water molecule H2O",
        "atom model",
        "lever physics",
        "AC circuit",
        "mitochondria organelle",
        "plant cell structure",
        "neuron cell",
        "blood circulation system",
        "skeletal system bones",
        "digestive system",
        "solar system planets",
        "photosynthesis process",
        "periodic table elements",
        "chemical reaction diagram",
        "electromagnetic wave",
        "simple machine pulley",
        "electric motor diagram"
    ]
    
    # Mapping from verbose labels to simplified names
    LABEL_TO_SUBJECT = {
        "anatomical heart": "heart",
        "human cell": "cell",
        "double helix DNA": "dna",
        "water molecule H2O": "water_molecule",
        "atom model": "atom",
        "lever physics": "lever",
        "AC circuit": "circuit",
        "mitochondria organelle": "mitochondria",
        "plant cell structure": "plant_cell",
        "neuron cell": "neuron",
        "blood circulation system": "circulation",
        "skeletal system bones": "skeleton",
        "digestive system": "digestion",
        "solar system planets": "solar_system",
        "photosynthesis process": "photosynthesis",
        "periodic table elements": "periodic_table",
        "chemical reaction diagram": "reaction",
        "electromagnetic wave": "em_wave",
        "simple machine pulley": "pulley",
        "electric motor diagram": "motor"
    }
    
    def __init__(self, device: str = None):
        """
        Initialize the classifier with CLIP model.
        
        Args:
            device: Computing device ('cuda', 'mps', or 'cpu'). Auto-detected if None.
        """
        # Auto-detect best available device
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
            
        print(f"Initializing CLIP model on device: {self.device}")
        
        # Load CLIP model (ViT-B/32)
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.model.eval()
        
        # Pre-compute text embeddings for efficiency
        self._compute_text_embeddings()
        
    def _compute_text_embeddings(self):
        """Pre-compute and cache text embeddings for all subject labels."""
        print("Computing text embeddings for subject labels...")
        
        # Tokenize all labels
        text_tokens = clip.tokenize(self.SUBJECT_LABELS).to(self.device)
        
        # Compute embeddings
        with torch.no_grad():
            self.text_features = self.model.encode_text(text_tokens)
            # Normalize embeddings for cosine similarity
            self.text_features /= self.text_features.norm(dim=-1, keepdim=True)
            
        print(f"Cached embeddings for {len(self.SUBJECT_LABELS)} subject labels.")
    
    def classify_image(self, image_path: str, top_k: int = 3) -> Dict:
        """
        Classify an educational diagram image.
        
        Args:
            image_path: Path to the input image
            top_k: Number of top predictions to return
            
        Returns:
            Dictionary containing:
                - predicted_subject: Most likely subject (simplified name)
                - confidence: Confidence score (0-1)
                - top_predictions: List of top k predictions with scores
                - all_scores: Complete similarity scores for all labels
        """
        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Compute image embedding
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            # Normalize for cosine similarity
            image_features /= image_features.norm(dim=-1, keepdim=True)
        
        # Compute cosine similarity between image and all text labels
        similarity = (100.0 * image_features @ self.text_features.T).softmax(dim=-1)
        scores = similarity[0].cpu().numpy()
        
        # Get top k predictions
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        # Build results
        top_predictions = []
        for idx in top_indices:
            label = self.SUBJECT_LABELS[idx]
            subject = self.LABEL_TO_SUBJECT[label]
            score = float(scores[idx])
            
            top_predictions.append({
                "subject": subject,
                "label": label,
                "confidence": round(score, 4)
            })
        
        # Primary prediction
        best_label = self.SUBJECT_LABELS[top_indices[0]]
        predicted_subject = self.LABEL_TO_SUBJECT[best_label]
        confidence = float(scores[top_indices[0]])
        
        # Complete score dictionary
        all_scores = {
            self.LABEL_TO_SUBJECT[label]: round(float(scores[i]), 4)
            for i, label in enumerate(self.SUBJECT_LABELS)
        }
        
        return {
            "predicted_subject": predicted_subject,
            "confidence": round(confidence, 4),
            "top_predictions": top_predictions,
            "all_scores": all_scores
        }
    
    def classify_batch(self, image_paths: List[str], top_k: int = 3) -> List[Dict]:
        """
        Classify multiple images in batch.
        
        Args:
            image_paths: List of image file paths
            top_k: Number of top predictions per image
            
        Returns:
            List of classification results
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.classify_image(image_path, top_k=top_k)
                result["image_path"] = image_path
                result["status"] = "success"
                results.append(result)
            except Exception as e:
                results.append({
                    "image_path": image_path,
                    "status": "error",
                    "error": str(e)
                })
        return results
    
    def add_custom_labels(self, new_labels: Dict[str, str]):
        """
        Add custom subject labels to the classifier.
        
        Args:
            new_labels: Dictionary mapping verbose labels to simplified names
                       e.g., {"volcanic eruption diagram": "volcano"}
        """
        # Extend label lists
        self.SUBJECT_LABELS.extend(new_labels.keys())
        self.LABEL_TO_SUBJECT.update(new_labels)
        
        # Recompute text embeddings
        self._compute_text_embeddings()
        
        print(f"Added {len(new_labels)} new labels. Total labels: {len(self.SUBJECT_LABELS)}")


def main():
    """Example usage and testing."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python classify.py <image_path>")
        print("Example: python classify.py data/sample_images/heart.jpg")
        return
    
    image_path = sys.argv[1]
    
    # Initialize classifier
    classifier = EducationalSubjectClassifier()
    
    # Classify image
    print(f"\nClassifying image: {image_path}")
    result = classifier.classify_image(image_path, top_k=5)
    
    # Pretty print results
    print("\n" + "="*60)
    print("CLASSIFICATION RESULTS")
    print("="*60)
    print(f"\nPredicted Subject: {result['predicted_subject']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    print("\nTop 5 Predictions:")
    for i, pred in enumerate(result['top_predictions'], 1):
        print(f"  {i}. {pred['subject']:20s} ({pred['label']}) - {pred['confidence']:.2%}")
    
    # Export as JSON
    output_file = image_path.rsplit('.', 1)[0] + '_classification.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nFull results saved to: {output_file}")


if __name__ == "__main__":
    main()
