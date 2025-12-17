from typing import Dict


# Mapping of classification labels to GLB model filenames
LABEL_TO_MODEL: Dict[str, str] = {
    "heart": "heart.glb",
    "dna": "dna.glb",
    "cell": "cell.glb",
    "atom": "atom.glb",
    "lever": "lever.glb",
    "pendulum": "pendulum.glb",
    "ac circuit": "ac_circuit.glb"
}


def get_model_path(label: str) -> str:
    """
    Map a classification label to its corresponding GLB model file path.
    
    Args:
        label: Predicted subject label
        
    Returns:
        URL path to the GLB model file
    """
    filename = LABEL_TO_MODEL.get(label.lower(), "heart.glb")  # Default to heart if not found
    return f"/static/models/{filename}"


def get_available_labels() -> list:
    """
    Get list of all available classification labels.
    
    Returns:
        List of label strings
    """
    return list(LABEL_TO_MODEL.keys())
