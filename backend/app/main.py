from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.routes import health, upload, dashboard, streak, mcq, activity
from app.utils.clip_inference import initialize_classifier


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("Starting up...")
    # Note: CLIP classifier is now lazy-loaded on first request to prevent startup timeouts
    print("Startup complete!")
    
    yield
    
    # Shutdown (cleanup if needed)
    print("Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Image to 3D Model API with Student Dashboard",
    description="AI-powered image classification API that maps 2D images to 3D models using CLIP, with gamification features including streaks, XP, MCQs, and recommendations",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://*.vercel.app",  # Wildcard for Vercel deployments
    # Add your specific Vercel domain here:
    # "https://your-app.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving GLB models
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(upload.router, tags=["Upload"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(streak.router, tags=["Streak"])
app.include_router(mcq.router, tags=["MCQ"])
app.include_router(activity.router, tags=["Activity"])


@app.get("/api")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Image to 3D Model API with Student Dashboard",
        "version": "2.0.0",
        "features": [
            "CLIP-based image classification",
            "3D model serving",
            "Daily streak tracking",
            "XP and leveling system",
            "MCQ questions",
            "Activity logging",
            "Topic recommendations"
        ],
        "docs": "/docs",
        "health": "/health",
        "dashboard": "/user/dashboard"
    }


# Serve frontend
# Check if running in Docker (or if /app/frontend exists)
frontend_path = "/app/frontend"
if not os.path.exists(frontend_path):
    # Fallback for local development: Go up two levels from app/ (backend/app -> backend -> root)
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
