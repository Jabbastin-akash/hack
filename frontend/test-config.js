/**
 * Node.js Test Runner for EduLens Configuration
 * This script tests the configuration without browser dependencies
 */

// Mock browser globals for Node.js environment
global.window = {};
global.fetch = async () => ({ ok: true, json: () => ({}) });
global.AbortController = class { abort() {} };
global.setTimeout = setTimeout;
global.clearTimeout = clearTimeout;
global.console = console;

console.log('🚀 Starting EduLens Configuration Test\n');

// Load the configuration by requiring it as a string and evaluating
const fs = require('fs');
const path = require('path');

try {
    // Read the config file from the js directory
    const configPath = path.join(__dirname, 'js', 'config.example.js');
    let configCode = fs.readFileSync(configPath, 'utf8');
    
    // Replace window assignments with global assignments for Node.js
    configCode = configCode.replace(/window\./g, 'global.');
    
    // Execute the configuration code
    eval(configCode);
    
    console.log('✅ Configuration loaded successfully!\n');
    
    // Test API Configuration
    console.log('🔗 API Configuration:');
    console.log(`   Base URL: ${global.API_CONFIG.BASE_URL}`);
    console.log(`   Demo Mode: ${global.API_CONFIG.DEMO_MODE}`);
    console.log(`   Timeout: ${global.API_CONFIG.TIMEOUT}ms`);
    console.log(`   Endpoints: ${Object.keys(global.API_CONFIG.ENDPOINTS).length} configured\n`);
    
    // Test App Configuration
    console.log('⚙️ App Configuration:');
    console.log(`   Name: ${global.APP_CONFIG.NAME}`);
    console.log(`   Version: ${global.APP_CONFIG.VERSION}`);
    console.log(`   XP per correct answer: ${global.APP_CONFIG.XP_REWARDS.QUIZ_CORRECT}`);
    console.log(`   XP per level: ${global.APP_CONFIG.LEVELS.XP_PER_LEVEL}\n`);
    
    // Test Subject Configuration
    console.log('📚 Subject Configuration:');
    Object.entries(global.SUBJECT_CONFIG).forEach(([key, subject]) => {
        console.log(`   ${subject.icon} ${subject.name}: ${subject.topics.join(', ')}`);
    });
    console.log('');
    
    // Test Helper Functions
    console.log('🛠️ Testing Helper Functions:');
    const testEndpoint = global.API_CONFIG.ENDPOINTS.UPLOAD_IMAGE;
    const fullUrl = global.ConfigHelper.getApiUrl(testEndpoint);
    console.log(`   API URL: ${fullUrl}`);
    console.log(`   Level 10 requires: ${global.ConfigHelper.calculateXPForLevel(10)} XP`);
    console.log(`   500 XP = Level: ${global.ConfigHelper.calculateLevelFromXP(500)}`);
    
    // Test file validation
    const mockFile = {
        size: 1024 * 1024, // 1MB
        type: 'image/jpeg'
    };
    const validation = global.ConfigHelper.validateUpload(mockFile);
    console.log(`   File validation (1MB JPEG): ${validation.valid ? 'Valid' : validation.error}`);
    
    // Test subject lookup
    const biologySubject = global.ConfigHelper.getSubject('biology');
    console.log(`   Biology subject lookup: ${biologySubject.icon} ${biologySubject.name}\n`);
    
    console.log('🎯 All tests completed successfully!');
    console.log('💡 The configuration is ready to use in your frontend application.');
    console.log('📝 Remember to copy config.example.js to config.js and update your settings.');

} catch (error) {
    console.error('❌ Error running configuration test:', error.message);
    process.exit(1);
}