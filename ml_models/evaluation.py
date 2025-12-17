"""
Evaluation metrics and testing utilities for the ML intelligence layer.
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


class ModelEvaluator:
    """
    Comprehensive evaluation metrics for the classification system.
    """
    
    def __init__(self):
        self.predictions = []
        self.ground_truths = []
        self.confidences = []
    
    def add_prediction(self, predicted: str, ground_truth: str, confidence: float):
        """Add a single prediction for evaluation."""
        self.predictions.append(predicted)
        self.ground_truths.append(ground_truth)
        self.confidences.append(confidence)
    
    def compute_metrics(self) -> Dict:
        """
        Compute comprehensive evaluation metrics.
        
        Returns:
            Dictionary with all metrics
        """
        if len(self.predictions) == 0:
            return {"error": "No predictions to evaluate"}
        
        # Basic metrics
        accuracy = accuracy_score(self.ground_truths, self.predictions)
        
        # Per-class metrics
        labels = sorted(set(self.ground_truths + self.predictions))
        precision = precision_score(
            self.ground_truths, 
            self.predictions, 
            labels=labels,
            average='weighted',
            zero_division=0
        )
        recall = recall_score(
            self.ground_truths,
            self.predictions,
            labels=labels, 
            average='weighted',
            zero_division=0
        )
        f1 = f1_score(
            self.ground_truths,
            self.predictions,
            labels=labels,
            average='weighted',
            zero_division=0
        )
        
        # Confidence analysis
        avg_confidence = np.mean(self.confidences)
        correct_mask = np.array(self.predictions) == np.array(self.ground_truths)
        avg_confidence_correct = np.mean([
            c for c, m in zip(self.confidences, correct_mask) if m
        ]) if any(correct_mask) else 0
        avg_confidence_incorrect = np.mean([
            c for c, m in zip(self.confidences, correct_mask) if not m
        ]) if not all(correct_mask) else 0
        
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "num_samples": len(self.predictions),
            "num_correct": int(sum(correct_mask)),
            "num_incorrect": int(len(correct_mask) - sum(correct_mask)),
            "avg_confidence": round(avg_confidence, 4),
            "avg_confidence_correct": round(avg_confidence_correct, 4),
            "avg_confidence_incorrect": round(avg_confidence_incorrect, 4)
        }
    
    def get_confusion_matrix(self) -> np.ndarray:
        """Get confusion matrix."""
        labels = sorted(set(self.ground_truths + self.predictions))
        return confusion_matrix(self.ground_truths, self.predictions, labels=labels)
    
    def get_classification_report(self) -> str:
        """Get detailed classification report."""
        return classification_report(self.ground_truths, self.predictions)
    
    def top_k_accuracy(self, k: int, top_k_predictions: List[List[str]]) -> float:
        """
        Compute top-k accuracy.
        
        Args:
            k: Number of top predictions to consider
            top_k_predictions: List of lists of top-k predictions for each sample
            
        Returns:
            Top-k accuracy
        """
        correct = sum(
            gt in preds[:k]
            for gt, preds in zip(self.ground_truths, top_k_predictions)
        )
        return correct / len(self.ground_truths)


def calibration_curve(confidences: List[float], correct: List[bool], n_bins: int = 10) -> Tuple:
    """
    Compute calibration curve for confidence scores.
    
    Args:
        confidences: List of model confidence scores
        correct: List of boolean indicators (True if prediction was correct)
        n_bins: Number of bins for calibration
        
    Returns:
        Tuple of (bin_centers, bin_accuracies, bin_counts)
    """
    confidences = np.array(confidences)
    correct = np.array(correct)
    
    bins = np.linspace(0, 1, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_accuracies = []
    bin_counts = []
    
    for i in range(n_bins):
        mask = (confidences >= bins[i]) & (confidences < bins[i + 1])
        if mask.sum() > 0:
            bin_accuracies.append(correct[mask].mean())
            bin_counts.append(mask.sum())
        else:
            bin_accuracies.append(0)
            bin_counts.append(0)
    
    return bin_centers, np.array(bin_accuracies), np.array(bin_counts)


if __name__ == "__main__":
    # Example usage
    evaluator = ModelEvaluator()
    
    # Simulate some predictions
    evaluator.add_prediction("heart", "heart", 0.95)
    evaluator.add_prediction("cell", "cell", 0.88)
    evaluator.add_prediction("dna", "atom", 0.72)  # Wrong prediction
    evaluator.add_prediction("circuit", "circuit", 0.91)
    
    # Compute metrics
    metrics = evaluator.compute_metrics()
    print("Evaluation Metrics:")
    print(f"  Accuracy: {metrics['accuracy']:.1%}")
    print(f"  Precision: {metrics['precision']:.1%}")
    print(f"  Recall: {metrics['recall']:.1%}")
    print(f"  F1 Score: {metrics['f1_score']:.1%}")
    print(f"  Average Confidence: {metrics['avg_confidence']:.1%}")
