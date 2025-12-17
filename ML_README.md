# ML Intelligence Layer - Edulens SNS

## 🎯 Overview

This is the **AI/ML intelligence layer** for Edulens SNS - a 2D to 3D educational content generator. The system uses computer vision and natural language processing to identify educational diagrams and recommend appropriate 3D models.

### Current Status: Phase 1 (MVP)
- ✅ CLIP-based image classifier
- ✅ 20+ educational subject categories
- ✅ 3D model metadata mapping
- ✅ Dataset building pipeline
- ✅ Future LLM roadmap documented

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- (Optional) CUDA-capable GPU for faster inference

### Installation

1. **Clone the repository** (if not already done)
```bash
cd /Users/vichu/Documents/GitHub/Edulens_SNS
```

2. **Create virtual environment**
```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Or using conda
conda create -n edulens python=3.9
conda activate edulens
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify installation**
```bash
python -c "import torch; import clip; print('✅ Installation successful!')"
```

---

## 📁 Project Structure

```
Edulens_SNS/
├── ml_models/              # ML models and algorithms
│   ├── classify.py         # CLIP-based classifier
│   ├── content_mapper.py   # 3D content mapping
│   └── dataset_builder.py  # Dataset management
│
├── config/                 # Configuration files
│   └── model_metadata.json # 3D model metadata
│
├── data/                   # Datasets
│   ├── raw/               # Original images
│   ├── processed/         # Preprocessed images
│   ├── annotations/       # Image annotations
│   └── embeddings/        # Pre-computed embeddings
│
├── docs/                   # Documentation
│   ├── FUTURE_LLM_ARCHITECTURE.md
│   └── DATASET_COLLECTION_GUIDE.md
│
└── requirements.txt        # Python dependencies
```

---

## 🔍 Usage Examples

### 1. Classify an Educational Diagram

```python
from ml_models.classify import EducationalSubjectClassifier

# Initialize classifier
classifier = EducationalSubjectClassifier()

# Classify an image
result = classifier.classify_image("path/to/heart_diagram.jpg")

print(f"Subject: {result['predicted_subject']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Top 3 predictions: {result['top_predictions']}")
```

**Command Line:**
```bash
python ml_models/classify.py data/sample_images/heart.jpg
```

**Output:**
```json
{
  "predicted_subject": "heart",
  "confidence": 0.9342,
  "top_predictions": [
    {"subject": "heart", "confidence": 0.9342},
    {"subject": "circulation", "confidence": 0.0421},
    {"subject": "cell", "confidence": 0.0187}
  ]
}
```

---

### 2. Get 3D Model Recommendation

```python
from ml_models.content_mapper import ContentMapper

# Initialize mapper
mapper = ContentMapper()

# Get model information
model_info = mapper.get_model_info("heart")

print(f"Model file: {model_info['file']}")
print(f"Animations: {model_info['animations']}")
print(f"Description: {model_info['description']}")
```

**Command Line:**
```bash
python ml_models/content_mapper.py heart
```

**Output:**
```
Model file: heart.glb
Animations: beat, explode, valve_open, valve_close
Description: Detailed 3D model of the human heart showing chambers, valves, and major vessels
```

---

### 3. Complete Classification + Recommendation Pipeline

```python
from ml_models.classify import EducationalSubjectClassifier
from ml_models.content_mapper import ContentMapper

# Initialize
classifier = EducationalSubjectClassifier()
mapper = ContentMapper()

# Process image
image_path = "diagrams/biology/heart_anatomy.jpg"
result = classifier.classify_image(image_path)

# Get recommendation
if result['confidence'] > 0.7:
    recommendation = mapper.get_recommendation(
        result['predicted_subject'],
        min_confidence=0.7
    )
    
    print(f"✅ Recommended: {recommendation['display_name']}")
    print(f"📦 Model: {recommendation['model_file']}")
    print(f"🎬 Animations: {', '.join(recommendation['animations'])}")
else:
    print("⚠️ Low confidence - manual review needed")
```

---

### 4. Build Dataset

```python
from ml_models.dataset_builder import DatasetBuilder

# Initialize builder
builder = DatasetBuilder()

# Add samples to dataset
builder.add_sample(
    image_path="downloads/heart_diagram.jpg",
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
print(f"Total images: {stats['total_images']}")
```

---

## 📊 Supported Subjects

### Biology (10 subjects)
- heart, cell, dna, mitochondria, plant_cell
- neuron, circulation, skeleton, digestion, photosynthesis

### Chemistry (6 subjects)
- water_molecule, atom, periodic_table, reaction

### Physics (4 subjects)
- lever, circuit, em_wave, pulley, motor

### Astronomy (1 subject)
- solar_system

**Total: 20+ educational subjects**

---

## 🧪 Running Tests

```bash
# Run basic functionality tests
python -m pytest tests/

# Test classifier
python ml_models/classify.py data/sample_images/test_heart.jpg

# Test content mapper
python ml_models/content_mapper.py

# Test dataset builder
python ml_models/dataset_builder.py
```

---

## 🎯 Model Performance

### Current CLIP Classifier (Phase 1)
- **Top-1 Accuracy:** ~75% (estimated)
- **Top-3 Accuracy:** ~90% (estimated)
- **Inference Time:** <500ms per image
- **Model Size:** ~600MB (ViT-B/32)

### Target (Future Custom LLM - Phase 3)
- **Top-1 Accuracy:** 85%+
- **Top-3 Accuracy:** 95%+
- **Inference Time:** <2s per image
- **Additional:** Explanations, reasoning, Q&A

---

## 🔬 Advanced Features

### Custom Subject Labels

Add your own subject categories:

```python
classifier = EducationalSubjectClassifier()

# Add custom labels
custom_labels = {
    "volcanic eruption diagram": "volcano",
    "earthquake seismograph": "seismograph",
    "tectonic plates map": "tectonics"
}

classifier.add_custom_labels(custom_labels)
```

### Batch Processing

Process multiple images efficiently:

```python
image_paths = [
    "biology/heart.jpg",
    "chemistry/h2o.jpg", 
    "physics/circuit.jpg"
]

results = classifier.classify_batch(image_paths, top_k=5)

for result in results:
    if result['status'] == 'success':
        print(f"{result['image_path']}: {result['predicted_subject']}")
```

### Search by Category

Find all models in a specific domain:

```python
mapper = ContentMapper()

# Get all biology models
biology_models = mapper.get_by_category("biology")

# Get beginner-level content
beginner_content = mapper.get_by_difficulty("beginner")

# Search by educational tag
neuroscience = mapper.search_by_tag("neuroscience")
```

---

## 🚀 Future Roadmap

### Phase 2: Enhanced Classification (Months 3-5)
- Fine-tune on custom educational dataset
- Improve accuracy to 80%+
- Add confidence calibration
- Support multi-label classification

### Phase 3: Custom Multimodal LLM (Months 6-12)
- Build LLaMA 3.1 8B-based system
- LoRA fine-tuning for efficiency
- RAG integration for grounding
- Generate explanations & descriptions
- Answer questions about diagrams

**See:** `docs/FUTURE_LLM_ARCHITECTURE.md` for complete roadmap

---

## 📚 Documentation

- **[Future LLM Architecture](docs/FUTURE_LLM_ARCHITECTURE.md)** - Complete roadmap for custom multimodal LLM
- **[Dataset Collection Guide](docs/DATASET_COLLECTION_GUIDE.md)** - How to build training datasets
- **API Documentation** - Coming soon
- **Model Cards** - Coming soon

---

## 🛠️ Development

### Code Style
```bash
# Format code
black ml_models/

# Lint code
flake8 ml_models/
```

### Adding New Subjects

1. **Update label taxonomy** in `classify.py`:
```python
SUBJECT_LABELS = [
    "anatomical heart",
    "human cell",
    "YOUR_NEW_SUBJECT",  # Add here
    # ...
]
```

2. **Add to label mapping**:
```python
LABEL_TO_SUBJECT = {
    "YOUR_NEW_SUBJECT": "your_subject_id",
    # ...
}
```

3. **Update metadata** in `config/model_metadata.json`:
```json
{
  "your_subject_id": {
    "file": "your_model.glb",
    "display_name": "Your Subject Name",
    "subject_category": "biology",
    // ...
  }
}
```

---

## 🐛 Troubleshooting

### Issue: "CLIP model download fails"
**Solution:** Check internet connection or manually download from OpenAI repo

### Issue: "CUDA out of memory"
**Solution:** Use CPU mode or reduce batch size
```python
classifier = EducationalSubjectClassifier(device="cpu")
```

### Issue: "Low classification confidence"
**Solution:** Image may be unclear, try:
- Higher resolution image
- Better lighting/contrast
- Remove watermarks/text overlays

### Issue: "Subject not found in metadata"
**Solution:** Add new subject to `config/model_metadata.json`

---

## 📞 Support & Contact

- **Issues:** GitHub Issues (coming soon)
- **Questions:** Create a discussion
- **Email:** support@edulens.com (placeholder)

---

## 🙏 Acknowledgments

- **OpenAI CLIP** - Vision-language pre-training
- **Hugging Face** - Transformers library
- **Meta LLaMA** - Foundation model (future)
- **Educational resources:** OpenStax, Khan Academy, Wikimedia

---

## 📄 License

[Add your license here]

---

## 🎯 Next Steps

1. ✅ Review this README
2. 🔧 Install dependencies
3. 🧪 Run test classification
4. 📊 Start collecting dataset
5. 📚 Read future architecture document
6. 🚀 Begin Phase 2 development

**Ready to build the future of educational AI!** 🎓✨
