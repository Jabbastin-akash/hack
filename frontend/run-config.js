/**
 * Direct Configuration Test Runner
 * Runs the EduLens configuration from the current file location
 */

const fs = require('fs');

// Mock browser globals for Node.js environment
global.window = {};
global.fetch = async () => ({ ok: true, json: () => ({}) });
global.AbortController = class { abort() {} };

console.log('🚀 Running EduLens Configuration\n');

try {
    // Read the config file directly from the path
    const configPath = 'c:\\Users\\Lokesh Kumar\\OneDrive\\Desktop\\Github\\Cohort_Web_App\\Edulens_SNS\\frontend\\js\\config.example.js';
    let configCode = fs.readFileSync(configPath, 'utf8');
    
    // Replace window assignments with global assignments for Node.js
    configCode = configCode.replace(/window\./g, 'global.');
    
    // Execute the configuration code
    eval(configCode);
    
    console.log('✅ Configuration executed successfully!\n');
    
    // Display key configuration values
    console.log('🔗 API Configuration:');
    console.log(`   📍 Base URL: ${global.API_CONFIG.BASE_URL}`);
    console.log(`   🎮 Demo Mode: ${global.API_CONFIG.DEMO_MODE ? 'Enabled' : 'Disabled'}`);
    console.log(`   ⏱️  Timeout: ${global.API_CONFIG.TIMEOUT}ms`);
    console.log(`   🔗 Endpoints Available: ${Object.keys(global.API_CONFIG.ENDPOINTS).length}`);
    
    console.log('\n⚙️  App Configuration:');
    console.log(`   📱 App Name: ${global.APP_CONFIG.NAME}`);
    console.log(`   📊 Version: ${global.APP_CONFIG.VERSION}`);
    console.log(`   🏆 XP Rewards: Quiz(${global.APP_CONFIG.XP_REWARDS.QUIZ_CORRECT}), Upload(${global.APP_CONFIG.XP_REWARDS.IMAGE_UPLOAD}), Streak(${global.APP_CONFIG.XP_REWARDS.DAILY_STREAK})`);
    
    console.log('\n📚 Subjects Available:');
    Object.entries(global.SUBJECT_CONFIG).forEach(([key, subject]) => {
        console.log(`   ${subject.icon} ${subject.name} (${subject.topics.length} topics)`);
    });
    
    console.log('\n🛠️  Helper Functions Test:');
    
    // Test API URL generation
    const uploadEndpoint = global.ConfigHelper.getApiUrl(global.API_CONFIG.ENDPOINTS.UPLOAD_IMAGE);
    console.log(`   🔗 Upload URL: ${uploadEndpoint}`);
    
    // Test XP calculations
    const xpFor20 = global.ConfigHelper.calculateXPForLevel(20);
    const levelFrom1000 = global.ConfigHelper.calculateLevelFromXP(1000);
    console.log(`   📈 Level 20 requires: ${xpFor20} XP`);
    console.log(`   📊 1000 XP equals: Level ${levelFrom1000}`);
    
    // Test file validation
    const testFiles = [
        { name: 'good.jpg', size: 2 * 1024 * 1024, type: 'image/jpeg' },
        { name: 'too-big.jpg', size: 15 * 1024 * 1024, type: 'image/jpeg' },
        { name: 'wrong.txt', size: 1024, type: 'text/plain' }
    ];
    
    console.log('\n📁 File Validation Tests:');
    testFiles.forEach(file => {
        const result = global.ConfigHelper.validateUpload(file);
        const status = result.valid ? '✅' : '❌';
        console.log(`   ${status} ${file.name}: ${result.valid ? 'Valid' : result.error}`);
    });
    
    console.log('\n🎯 Configuration is ready to use!');
    console.log('💡 To use in your frontend:');
    console.log('   1. Copy config.example.js to config.js');
    console.log('   2. Update API_CONFIG.BASE_URL with your backend URL');
    console.log('   3. Include config.js in your HTML pages');

} catch (error) {
    console.error('❌ Error:', error.message);
    
    if (error.code === 'ENOENT') {
        console.log('\n💡 The file might not exist at the expected location.');
        console.log('   Current file should be at:');
        console.log('   c:\\Users\\Lokesh Kumar\\OneDrive\\Desktop\\Github\\Cohort_Web_App\\Edulens_SNS\\frontend\\js\\config.example.js');
    }
}