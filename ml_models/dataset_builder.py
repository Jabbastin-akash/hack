"""
Dataset Building Pipeline for Educational Content AI
Utilities for collecting, organizing, and preparing training data
for future multimodal LLM fine-tuning.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class DatasetBuilder:
    """
    Organizes and manages educational diagram datasets for ML training.
    """
    
    def __init__(self, base_path: str = None):
        """
        Initialize dataset builder.
        
        Args:
            base_path: Root directory for dataset storage
        """
        if base_path is None:
            project_root = Path(__file__).parent.parent
            base_path = project_root / "data"
        
        self.base_path = Path(base_path)
        self._setup_directory_structure()
        
    def _setup_directory_structure(self):
        """Create organized directory structure for datasets."""
        directories = [
            "raw/biology",
            "raw/chemistry",
            "raw/physics",
            "raw/astronomy",
            "processed/biology",
            "processed/chemistry",
            "processed/physics",
            "processed/astronomy",
            "annotations",
            "metadata",
            "embeddings",
            "validation",
            "test"
        ]
        
        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)
    
    def add_sample(
        self,
        image_path: str,
        subject: str,
        category: str,
        annotations: Dict = None,
        copy_to_dataset: bool = True
    ) -> Dict:
        """
        Add a new sample to the dataset.
        
        Args:
            image_path: Path to the source image
            subject: Subject label (e.g., 'heart', 'dna')
            category: Category (biology, chemistry, physics, astronomy)
            annotations: Optional metadata/annotations
            copy_to_dataset: Whether to copy file to dataset structure
            
        Returns:
            Dictionary with sample information
        """
        source = Path(image_path)
        if not source.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{subject}_{timestamp}{source.suffix}"
        
        # Destination path
        dest_dir = self.base_path / "raw" / category
        dest_path = dest_dir / filename
        
        # Copy file if requested
        if copy_to_dataset:
            shutil.copy2(source, dest_path)
        
        # Create annotation entry
        sample_data = {
            "filename": filename,
            "subject": subject,
            "category": category,
            "original_path": str(source),
            "dataset_path": str(dest_path),
            "added_date": datetime.now().isoformat(),
            "annotations": annotations or {}
        }
        
        # Save annotation
        annotation_file = self.base_path / "annotations" / f"{filename.rsplit('.', 1)[0]}.json"
        with open(annotation_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        return sample_data
    
    def create_manifest(self, output_path: str = None) -> str:
        """
        Create a manifest file listing all dataset samples.
        
        Args:
            output_path: Path to save manifest. Auto-generated if None.
            
        Returns:
            Path to the created manifest file
        """
        if output_path is None:
            output_path = self.base_path / "metadata" / "dataset_manifest.json"
        
        manifest = {
            "created": datetime.now().isoformat(),
            "categories": {},
            "total_samples": 0
        }
        
        # Scan annotations
        annotation_dir = self.base_path / "annotations"
        for annotation_file in annotation_dir.glob("*.json"):
            with open(annotation_file, 'r') as f:
                sample = json.load(f)
            
            category = sample["category"]
            if category not in manifest["categories"]:
                manifest["categories"][category] = {
                    "count": 0,
                    "subjects": {}
                }
            
            subject = sample["subject"]
            if subject not in manifest["categories"][category]["subjects"]:
                manifest["categories"][category]["subjects"][subject] = []
            
            manifest["categories"][category]["subjects"][subject].append({
                "filename": sample["filename"],
                "path": sample["dataset_path"],
                "added": sample["added_date"]
            })
            
            manifest["categories"][category]["count"] += 1
            manifest["total_samples"] += 1
        
        # Save manifest
        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"Manifest created: {output_path}")
        print(f"Total samples: {manifest['total_samples']}")
        
        return str(output_path)
    
    def generate_dataset_report(self) -> Dict:
        """
        Generate statistics about the current dataset.
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            "total_images": 0,
            "by_category": {},
            "by_subject": {},
            "raw_count": 0,
            "processed_count": 0
        }
        
        # Count raw images
        for category_dir in (self.base_path / "raw").iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                images = list(category_dir.glob("*.[jp]*g")) + list(category_dir.glob("*.png"))
                count = len(images)
                
                stats["by_category"][category] = count
                stats["raw_count"] += count
        
        # Count processed images
        for category_dir in (self.base_path / "processed").iterdir():
            if category_dir.is_dir():
                images = list(category_dir.glob("*.[jp]*g")) + list(category_dir.glob("*.png"))
                stats["processed_count"] += len(images)
        
        stats["total_images"] = stats["raw_count"] + stats["processed_count"]
        
        # Subject distribution from annotations
        annotation_dir = self.base_path / "annotations"
        for annotation_file in annotation_dir.glob("*.json"):
            with open(annotation_file, 'r') as f:
                sample = json.load(f)
            
            subject = sample["subject"]
            stats["by_subject"][subject] = stats["by_subject"].get(subject, 0) + 1
        
        return stats


def create_collection_guide(output_path: str):
    """
    Generate a guide for dataset collection.
    
    Args:
        output_path: Where to save the guide
    """
    guide = """
# Educational Diagram Dataset Collection Guide

## 🎯 Objective
Build a comprehensive dataset of educational diagrams for training a multimodal LLM
that can understand 2D scientific diagrams and recommend appropriate 3D models.

## 📊 Target Distribution

### Biology (Target: 1000+ images)
- Anatomy: heart, brain, skeleton, organs (200+)
- Cell biology: cells, organelles, membranes (200+)
- Genetics: DNA, chromosomes, inheritance (150+)
- Systems: circulatory, nervous, digestive (200+)
- Botany: plant structures, photosynthesis (150+)
- Other: evolution, ecology diagrams (100+)

### Chemistry (Target: 800+ images)
- Molecular structures: H2O, CO2, organic molecules (200+)
- Atomic models: Bohr, electron shells (150+)
- Reactions: chemical equations, energy diagrams (150+)
- Periodic table variations (100+)
- Lab equipment and setups (100+)
- Bonding: ionic, covalent, metallic (100+)

### Physics (Target: 800+ images)
- Mechanics: forces, motion, simple machines (200+)
- Electricity: circuits, fields, magnetism (200+)
- Waves: sound, light, EM spectrum (150+)
- Energy: kinetic, potential, conservation (100+)
- Modern physics: relativity, quantum (100+)
- Optics: lenses, reflection, refraction (50+)

### Astronomy (Target: 400+ images)
- Solar system diagrams (100+)
- Star life cycles (50+)
- Galaxy structures (50+)
- Orbital mechanics (100+)
- Space phenomena (100+)

## 📁 Data Sources

### Free Educational Resources
1. **OpenStax** (https://openstax.org)
   - CC-BY licensed textbook images
   - High quality scientific diagrams
   
2. **Wikimedia Commons** (https://commons.wikimedia.org)
   - Search: "biology diagram", "chemistry structure", etc.
   - Filter by CC0/CC-BY licenses
   
3. **PhET Interactive Simulations** (https://phet.colorado.edu)
   - Screenshots of educational simulations
   
4. **Khan Academy** (https://www.khanacademy.org)
   - Educational diagrams (check usage rights)
   
5. **BioRender** (https://biorender.com)
   - Some free scientific illustrations
   
6. **PubChem** (https://pubchem.ncbi.nlm.nih.gov)
   - Chemical structure diagrams (public domain)

### Creation Tools
1. **Draw.io / diagrams.net**
   - Create custom diagrams
   
2. **ChemDraw / ChemSketch**
   - Chemical structures
   
3. **BioRender**
   - Biological illustrations

## 🏷️ Annotation Guidelines

### Required Metadata for Each Image
```json
{
  "subject": "heart",
  "category": "biology",
  "subcategory": "anatomy",
  "difficulty": "intermediate",
  "educational_tags": ["cardiovascular", "organ", "anatomy"],
  "diagram_type": "labeled_illustration",
  "quality": "high",
  "license": "CC-BY-4.0",
  "source": "OpenStax Anatomy Textbook",
  "resolution": "1920x1080",
  "has_labels": true,
  "has_colors": true,
  "style": "realistic"
}
```

### Diagram Types
- `labeled_illustration`: Has text labels
- `schematic`: Simplified representation
- `realistic`: Photo-realistic rendering
- `abstract`: Conceptual diagram
- `mixed`: Combination of types

### Quality Levels
- `high`: Clear, well-defined, >1000px
- `medium`: Acceptable quality, 500-1000px
- `low`: May need preprocessing, <500px

## 🔄 Data Collection Workflow

### Phase 1: Initial Collection (Week 1-2)
1. Gather 50-100 images per category
2. Focus on high-quality, clearly labeled diagrams
3. Prioritize subjects in model_metadata.json

### Phase 2: Expansion (Week 3-4)
1. Add variations of each subject
2. Include different diagram styles
3. Target 200-300 images per category

### Phase 3: Refinement (Week 5-6)
1. Balance subject distribution
2. Add edge cases and challenging examples
3. Reach 500+ images per major category

## 🧹 Data Preprocessing

### Image Standards
- Format: JPG or PNG
- Resolution: Minimum 512x512px, ideal 1024x1024px
- Color: RGB (convert grayscale to RGB if needed)
- Background: Clean, preferably white or neutral

### Preprocessing Steps
1. Resize to standard dimensions (e.g., 512x512, 1024x1024)
2. Remove watermarks (if legally permitted)
3. Crop to focus on main diagram
4. Normalize brightness/contrast
5. Remove excessive text/captions (keep labels)

## 📝 Annotation Process

### Use the DatasetBuilder Class
```python
from dataset_builder import DatasetBuilder

builder = DatasetBuilder()

# Add a sample
builder.add_sample(
    image_path="path/to/heart_diagram.jpg",
    subject="heart",
    category="biology",
    annotations={
        "difficulty": "intermediate",
        "has_labels": True,
        "style": "realistic"
    }
)

# Generate manifest
builder.create_manifest()

# Get statistics
stats = builder.generate_dataset_report()
print(stats)
```

## 🎯 Quality Checklist

For each image, verify:
- [ ] Clear subject identification
- [ ] Appropriate resolution
- [ ] Proper licensing/attribution
- [ ] Accurate annotations
- [ ] Belongs to correct category
- [ ] Unique (not a duplicate)
- [ ] Educational value
- [ ] Matches existing 3D model availability

## 📊 Validation Split Strategy

- Training: 70% (main learning dataset)
- Validation: 15% (hyperparameter tuning)
- Test: 15% (final evaluation, never seen during training)

Ensure balanced distribution across:
- Categories
- Subjects
- Difficulty levels
- Diagram styles

## 🚀 Next Steps After Collection

1. **Data Augmentation**
   - Rotation (±15°)
   - Scaling (0.8x - 1.2x)
   - Color jittering
   - Horizontal flips (where appropriate)

2. **Embedding Generation**
   - Use current CLIP model
   - Pre-compute embeddings for faster training

3. **Dataset Versioning**
   - Use Git LFS or DVC for large files
   - Tag versions: v1.0, v1.1, etc.
   - Document changes between versions

4. **Continuous Improvement**
   - Add difficult/misclassified examples
   - Expand to new subjects
   - Regular quality audits
"""
    
    with open(output_path, 'w') as f:
        f.write(guide)
    
    print(f"Collection guide created: {output_path}")


def main():
    """Example usage."""
    # Initialize builder
    builder = DatasetBuilder()
    
    print("Dataset directory structure created.")
    print(f"Base path: {builder.base_path}")
    
    # Generate report
    stats = builder.generate_dataset_report()
    print("\nCurrent Dataset Statistics:")
    print(f"Total images: {stats['total_images']}")
    print(f"Raw: {stats['raw_count']}, Processed: {stats['processed_count']}")
    
    if stats['by_category']:
        print("\nBy Category:")
        for category, count in stats['by_category'].items():
            print(f"  {category}: {count}")
    
    # Create collection guide
    guide_path = builder.base_path.parent / "docs" / "DATASET_COLLECTION_GUIDE.md"
    create_collection_guide(guide_path)


if __name__ == "__main__":
    main()
