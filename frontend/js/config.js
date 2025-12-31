/**
 * EduLens Frontend Configuration
 * 
 * Configure your backend API endpoints and app settings here.
 */

// ============================================
// API Configuration
// ============================================

const API_CONFIG = {
    // Your backend base URL
    // Empty string means use the same origin as the frontend
    BASE_URL: '',

    // API Endpoints
    ENDPOINTS: {
        HEALTH: '/health',
        UPLOAD: '/upload',
        DASHBOARD: '/user/dashboard',
        STREAK: '/streak',
        MCQ: '/mcq',
        ACTIVITY: '/activity'
    }
};
