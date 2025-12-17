# 🎯 Image to 3D Model Classification API

A lightweight FastAPI backend that uses OpenAI's CLIP model to classify 2D images of educational subjects and returns corresponding 3D model files.

## 🌟 Features

- **AI-Powered Classification**: Uses CLIP (Contrastive Language-Image Pre-training) for zero-shot image classification
- **7 Educational Subjects**: heart, dna, cell, atom, lever, pendulum, ac circuit
- **RESTful API**: Clean FastAPI implementation with automatic OpenAPI documentation
- **Static 3D Model Serving**: Serves GLB files for frontend consumption
- **CORS Enabled**: Ready for Vercel frontend integration
- **Production Ready**: Includes Dockerfile for easy deployment

## 🗂 Project Structure

```
app/
├── main.py                    # FastAPI app initialization, CORS, static files
├── routes/
│   ├── health.py             # Health check endpoint
│   └── upload.py             # Image upload and classification endpoint
├── utils/
│   ├── clip_inference.py     # CLIP model loading and inference logic
│   ├── model_mapping.py      # Label to GLB file mapping
│   └── file_validation.py    # File type and size validation
├── schemas/
│   └── responses.py          # Pydantic response models
└── static/
    └── models/               # GLB 3D model files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Local Development

1. **Clone and navigate to the project:**
   ```bash
   cd c:\Python310\edulens\Edulens_SNS
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your GLB models:**
   Place your 3D model files in `app/static/models/`:
   - heart.glb
   - dna.glb
   - cell.glb
   - atom.glb
   - lever.glb
   - pendulum.glb
   - ac_circuit.glb

5. **Run the server:**
   ```bash
   # From project root
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Or using Python directly
   python -m app.main
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## 📡 API Endpoints

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Image to 3D Model API is running"
}
```

### POST `/upload-image`
Upload an image for classification.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (PNG/JPG/JPEG image)

**Response:**
```json
{
  "predicted_subject": "heart",
  "confidence": 0.9234,
  "model_path": "/static/models/heart.glb"
}
```

**Error Response:**
```json
{
  "detail": "Invalid file type. Allowed types: png, jpg, jpeg"
}
```

### GET `/static/models/{filename}`
Serve 3D model files (automatically handled by FastAPI StaticFiles).

## 🧪 Testing the API

### Using cURL:
```bash
curl -X POST "http://localhost:8000/upload-image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

### Using Python requests:
```python
import requests

url = "http://localhost:8000/upload-image"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Using the Interactive Docs:
1. Navigate to http://localhost:8000/docs
2. Find the `/upload-image` endpoint
3. Click "Try it out"
4. Upload an image file
5. Click "Execute"

## 🐳 Docker Deployment

### Build the image:
```bash
docker build -t image-to-3d-api .
```

### Run the container:
```bash
docker run -d -p 8000:8000 --name image-api image-to-3d-api
```

## ☁️ Cloud Deployment

### Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and initialize:**
   ```bash
   railway login
   railway init
   ```

3. **Deploy:**
   ```bash
   railway up
   ```

4. **Add your GLB files:** Upload model files to Railway's persistent storage or use a CDN.

### Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `PORT=8000`
6. Deploy!

## 🔧 Configuration

### CORS Origins

Edit `app/main.py` to add your Vercel frontend URL:

```python
origins = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",  # Add your Vercel domain
]
```

### Environment Variables

Optional `.env` file configuration (copy from `.env.example`):
- `PORT`: Server port (default: 8000)
- `ALLOWED_ORIGINS`: Comma-separated CORS origins
- `CLIP_MODEL`: HuggingFace model identifier

## 📦 Updating the Model Library

To add new subjects:

1. **Add GLB file** to `app/static/models/` (e.g., `brain.glb`)

2. **Update label mapping** in `app/utils/model_mapping.py`:
   ```python
   LABEL_TO_MODEL = {
       "heart": "heart.glb",
       "brain": "brain.glb",  # New entry
       # ...
   }
   ```

3. **Update text labels** in `app/utils/clip_inference.py`:
   ```python
   self.labels = [
       "heart",
       "brain",  # New entry
       # ...
   ]
   ```

4. **Restart the server** to reload the model.

## 🧠 How It Works

1. **Image Upload**: Client sends image via multipart/form-data
2. **Validation**: File type and size are validated
3. **Preprocessing**: Image is loaded with Pillow and converted to RGB
4. **CLIP Encoding**: Image is encoded using CLIP's vision encoder
5. **Text Comparison**: Image embedding is compared to precomputed text embeddings
6. **Classification**: Highest similarity score determines the predicted label
7. **Model Mapping**: Label is mapped to corresponding GLB file path
8. **Response**: JSON response with prediction, confidence, and model path

## 📊 Model Performance

- **Model**: OpenAI CLIP (ViT-B/32)
- **Inference Time**: ~200-500ms on CPU
- **Accuracy**: Depends on image quality and subject clarity
- **Memory Usage**: ~1.5GB RAM for model

## 🛠 Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server
- **Transformers**: HuggingFace library for CLIP model
- **PyTorch**: Deep learning framework
- **Pillow**: Image processing
- **Pydantic**: Data validation

## 🐛 Troubleshooting

### Model download fails
- Ensure stable internet connection
- Models are cached in `~/.cache/huggingface/`
- First startup takes longer due to model download (~400MB)

### Out of memory errors
- CLIP model requires ~1.5GB RAM
- Consider using smaller CLIP variant: `openai/clip-vit-base-patch16`
- Or deploy on a platform with more RAM

### CORS errors
- Verify frontend URL is added to `origins` list in `main.py`
- Check browser console for specific CORS error
- Ensure credentials and headers are properly configured

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using FastAPI and OpenAI CLIP**
