import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import Tuple
import numpy as np
import warnings

# Suppress FutureWarning from huggingface_hub regarding resume_download
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub")


class CLIPClassifier:
    """
    CLIP-based image classifier for educational subjects.
    Preloads model at initialization and provides classification methods.
    """
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """
        Initialize CLIP model and processor.
        
        Args:
            model_name: HuggingFace model identifier
        """
        print(f"Loading CLIP model: {model_name}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Predefined text labels for classification
        self.labels = [
            "heart",
            "dna",
            "cell",
            "atom",
            "lever",
            "pendulum",
            "ac circuit"
        ]
        
        # Precompute text embeddings for efficiency
        self.text_embeddings = self._precompute_text_embeddings()
        print(f"CLIP model loaded successfully on {self.device}")
    
    def _precompute_text_embeddings(self) -> torch.Tensor:
        """
        Precompute text embeddings for all labels.
        
        Returns:
            Tensor of normalized text embeddings
        """
        with torch.no_grad():
            text_inputs = self.processor(
                text=self.labels,
                return_tensors="pt",
                padding=True
            ).to(self.device)
            
            text_features = self.model.get_text_features(**text_inputs)
            # Normalize embeddings
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
        return text_features
    
    def classify_image(self, image: Image.Image) -> Tuple[str, float]:
        """
        Classify an image and return the predicted label with confidence.
        
        Args:
            image: PIL Image object
            
        Returns:
            Tuple of (predicted_label, confidence_score)
        """
        # Ensure image is in RGB mode
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Preprocess image
        with torch.no_grad():
            image_inputs = self.processor(
                images=image,
                return_tensors="pt"
            ).to(self.device)
            
            # Get image embeddings
            image_features = self.model.get_image_features(**image_inputs)
            # Normalize embeddings
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Compute cosine similarity with text embeddings
            similarities = (image_features @ self.text_embeddings.T).squeeze(0)
            
            # Apply softmax to get probabilities
            probs = torch.nn.functional.softmax(similarities, dim=0)
            
            # Get the highest confidence prediction
            confidence, predicted_idx = torch.max(probs, dim=0)
            
        predicted_label = self.labels[predicted_idx.item()]
        confidence_score = confidence.item()
        
        return predicted_label, confidence_score


# Global classifier instance (initialized at startup)
_classifier: CLIPClassifier = None


def initialize_classifier():
    """Initialize the global CLIP classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = CLIPClassifier()


def get_classifier() -> CLIPClassifier:
    """
    Get the global CLIP classifier instance.
    Initializes it lazily if not already initialized.
    
    Returns:
        CLIPClassifier instance
    """
    global _classifier
    if _classifier is None:
        print("Lazy loading CLIP classifier...")
        initialize_classifier()
    return _classifier
