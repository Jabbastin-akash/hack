# Deploying EduLens to Railway

This guide explains how to deploy the EduLens application (Backend + Frontend) to Railway.

## Prerequisites

1.  A GitHub account.
2.  A Railway account (login with GitHub).
3.  This project pushed to a GitHub repository.

## Deployment Steps

1.  **Push to GitHub**: Ensure your latest code, including the new `Dockerfile` and `frontend/js/config.js`, is pushed to your GitHub repository.

2.  **Create Project on Railway**:
    *   Go to [Railway Dashboard](https://railway.app/dashboard).
    *   Click "New Project".
    *   Select "Deploy from GitHub repo".
    *   Select your repository.

3.  **Configuration**:
    *   Railway will automatically detect the `Dockerfile` in the root directory.
    *   It will start building the application.

4.  **Environment Variables** (Optional):
    *   If your app needs any environment variables (like API keys), go to the "Variables" tab in your Railway project and add them.

5.  **Access the App**:
    *   Once the deployment is successful, Railway will provide a public URL (e.g., `https://edulens-production.up.railway.app`).
    *   Click the URL to see your application. The frontend should load automatically.

## How it Works

*   **Single Service**: We have configured the application to run as a single service.
*   **Backend**: The Python FastAPI backend runs on port 8000.
*   **Frontend**: The backend serves the frontend static files at the root URL (`/`).
*   **API**: The API endpoints are available at their respective paths (e.g., `/health`, `/upload`). The original root API message is moved to `/api`.

## Troubleshooting

*   **Build Fails**: Check the "Build Logs" in Railway. If it fails installing dependencies, ensure `backend/requirements.txt` is correct.
*   **Frontend Connection Error**: Ensure `frontend/js/config.js` has `BASE_URL: ''` (empty string) so it uses the same domain as the backend.
