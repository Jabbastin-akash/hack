/**
 * EduLens Frontend Configuration
 * 
 * Configure your backend API endpoints and app settings here.
 * Copy this file to js/config.js and update with your backend URL.
 */

// ============================================
// API Configuration
// ============================================

const API_CONFIG = {
    // Your backend base URL
    // Examples:
    // - Development: 'http://localhost:5000'
    // - Production: 'https://api.edulens.com'
    BASE_URL: 'http://localhost:5000',
    
    // API Endpoints
    ENDPOINTS: {
        // Image upload and classification
        UPLOAD_IMAGE: '/upload-image',
        
        // Dashboard data
        DASHBOARD: '/user/dashboard',
        
        // Quiz endpoints
        MCQ_DAILY: '/user/mcq/daily',
        MCQ_SUBMIT: '/user/mcq/submit',
        
        // Activity tracking
        ACTIVITY_LOG: '/user/activity/log',
        
        // Streak management
        STREAK_COMPLETE: '/user/streak/complete',
        STREAK_STATUS: '/user/streak/status',
        
        // Badge management
        BADGES_UNLOCK: '/user/badges/unlock',
        BADGES_LIST: '/user/badges',
        
        // 3D Models
        MODELS_PATH: '/static/models',
    },
    
    // Request timeout in milliseconds
    TIMEOUT: 30000,
    
    // Enable demo mode (uses fallback data if backend fails)
    DEMO_MODE: true,
};

// ============================================
// App Configuration
// ============================================

const APP_CONFIG = {
    // App name
    NAME: 'EduLens',
    
    // Version
    VERSION: '1.0.0',
    
    // XP Rewards
    XP_REWARDS: {
        QUIZ_CORRECT: 10,          // XP per correct answer
        QUIZ_PERFECT_BONUS: 20,    // Bonus for 100% score
        MODEL_VIEW: 5,             // XP for viewing a model
        IMAGE_UPLOAD: 15,          // XP for uploading an image
        DAILY_STREAK: 25,          // XP for maintaining streak
    },
    
    // Level System
    LEVELS: {
        XP_PER_LEVEL: 100,         // XP needed per level
        MAX_LEVEL: 50,             // Maximum level
    },
    
    // Quiz Settings
    QUIZ: {
        QUESTIONS_PER_DAY: 5,      // Number of questions in daily quiz
        TIME_LIMIT: 300,           // Time limit in seconds (5 min)
        PASSING_SCORE: 60,         // Minimum percentage to pass
    },
    
    // Streak Settings
    STREAK: {
        GRACE_PERIOD_HOURS: 24,    // Hours before streak breaks
        MAX_STREAK_DISPLAY: 999,   // Maximum streak to display
    },
    
    // Upload Settings
    UPLOAD: {
        MAX_FILE_SIZE: 10 * 1024 * 1024,  // 10MB
        ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg', 'image/webp'],
        COMPRESS_QUALITY: 0.8,     // Image compression quality
    },
    
    // 3D Viewer Settings
    VIEWER: {
        CAMERA_FOV: 45,            // Camera field of view
        CAMERA_NEAR: 0.1,          // Near clipping plane
        CAMERA_FAR: 1000,          // Far clipping plane
        ENABLE_SHADOWS: true,      // Enable shadow rendering
        ENABLE_ANTIALIASING: true, // Enable antialiasing
        MAX_PIXEL_RATIO: 2,        // Maximum pixel ratio for performance
    },
    
    // UI Settings
    UI: {
        ANIMATION_DURATION: 300,   // Default animation duration in ms
        TOAST_DURATION: 5000,      // Toast notification duration
        AUTO_SAVE_INTERVAL: 60000, // Auto-save interval (1 min)
    },
};

// ============================================
// Subject Configuration
// ============================================

const SUBJECT_CONFIG = {
    biology: {
        name: 'Biology',
        icon: '🧬',
        color: '#059669',
        topics: ['anatomy', 'cells', 'genetics', 'ecology'],
    },
    chemistry: {
        name: 'Chemistry',
        icon: '⚗️',
        color: '#7c3aed',
        topics: ['molecules', 'reactions', 'elements', 'compounds'],
    },
    physics: {
        name: 'Physics',
        icon: '⚛️',
        color: '#dc2626',
        topics: ['mechanics', 'electricity', 'optics', 'quantum'],
    },
};

// ============================================
// Helper Functions
// ============================================

const ConfigHelper = {
    /**
     * Get full API URL for an endpoint
     */
    getApiUrl(endpoint) {
        return `${API_CONFIG.BASE_URL}${endpoint}`;
    },
    
    /**
     * Make API request with error handling
     */
    async apiRequest(endpoint, options = {}) {
        const url = this.getApiUrl(endpoint);
        const timeout = options.timeout || API_CONFIG.TIMEOUT;
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            
            if (API_CONFIG.DEMO_MODE) {
                console.log('Demo mode enabled, returning fallback data');
                return null; // Component will use demo data
            }
            
            throw error;
        }
    },
    
    /**
     * Get subject configuration
     */
    getSubject(subjectKey) {
        return SUBJECT_CONFIG[subjectKey] || null;
    },
    
    /**
     * Calculate XP for level
     */
    calculateXPForLevel(level) {
        return level * APP_CONFIG.LEVELS.XP_PER_LEVEL;
    },
    
    /**
     * Calculate level from XP
     */
    calculateLevelFromXP(xp) {
        return Math.floor(xp / APP_CONFIG.LEVELS.XP_PER_LEVEL) + 1;
    },
    
    /**
     * Validate file upload
     */
    validateUpload(file) {
        if (file.size > APP_CONFIG.UPLOAD.MAX_FILE_SIZE) {
            return {
                valid: false,
                error: 'File size exceeds 10MB limit'
            };
        }
        
        if (!APP_CONFIG.UPLOAD.ALLOWED_TYPES.includes(file.type)) {
            return {
                valid: false,
                error: 'Invalid file type. Please upload an image.'
            };
        }
        
        return { valid: true };
    },
};

// ============================================
// Export Configuration (if using modules)
// ============================================

// For ES6 modules
// export { API_CONFIG, APP_CONFIG, SUBJECT_CONFIG, ConfigHelper };

// For global scope (current setup)
window.API_CONFIG = API_CONFIG;
window.APP_CONFIG = APP_CONFIG;
window.SUBJECT_CONFIG = SUBJECT_CONFIG;
window.ConfigHelper = ConfigHelper;

console.log('✅ EduLens configuration loaded');
console.log('📍 API Base URL:', API_CONFIG.BASE_URL);
console.log('🎮 Demo Mode:', API_CONFIG.DEMO_MODE ? 'Enabled' : 'Disabled');
