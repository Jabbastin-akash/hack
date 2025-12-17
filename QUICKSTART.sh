# Quick Start Guide
# Run these commands to get started with Edulens Intelligence Layer

# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Test installation
python -c "import torch; import clip; print('✅ Setup complete!')"

# 4. Try the classifier
# python ml_models/classify.py <your_image_path>

# 5. Try the complete pipeline
# python ml_models/pipeline.py <your_image_path>

# 6. View available 3D models
python ml_models/content_mapper.py

# 7. Initialize dataset builder
python ml_models/dataset_builder.py
