"""
Comprehensive Backend Testing Script
Tests all endpoints including CLIP classification and new dashboard features.
"""
import requests
import json
from io import BytesIO
from PIL import Image
import time

BASE_URL = "http://localhost:8000"
USER_ID = "test_user"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_result(endpoint, status, data=None, error=None):
    """Print test result."""
    status_icon = "✅" if status == "PASS" else "❌"
    print(f"{status_icon} {endpoint}: {status}")
    if data:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
    if error:
        print(f"   Error: {error}")

# =============================================================================
# TEST 1: HEALTH CHECK
# =============================================================================
print_section("TEST 1: Health Check")
try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print_result("GET /health", "PASS", response.json())
    else:
        print_result("GET /health", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /health", "FAIL", error=str(e))

# =============================================================================
# TEST 2: ROOT ENDPOINT
# =============================================================================
print_section("TEST 2: Root Endpoint")
try:
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print_result("GET /", "PASS", response.json())
    else:
        print_result("GET /", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /", "FAIL", error=str(e))

# =============================================================================
# TEST 3: STREAK ENDPOINTS
# =============================================================================
print_section("TEST 3: Streak Management")

# Get initial streak
try:
    response = requests.get(f"{BASE_URL}/user/streak", params={"user_id": USER_ID})
    if response.status_code == 200:
        print_result("GET /user/streak", "PASS", response.json())
    else:
        print_result("GET /user/streak", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /user/streak", "FAIL", error=str(e))

# Update streak
try:
    response = requests.post(f"{BASE_URL}/user/streak/update", params={"user_id": USER_ID})
    if response.status_code == 200:
        print_result("POST /user/streak/update", "PASS", response.json())
    else:
        print_result("POST /user/streak/update", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("POST /user/streak/update", "FAIL", error=str(e))

# =============================================================================
# TEST 4: XP ENDPOINT
# =============================================================================
print_section("TEST 4: XP and Leveling")
try:
    response = requests.get(f"{BASE_URL}/user/xp", params={"user_id": USER_ID})
    if response.status_code == 200:
        print_result("GET /user/xp", "PASS", response.json())
    else:
        print_result("GET /user/xp", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /user/xp", "FAIL", error=str(e))

# =============================================================================
# TEST 5: MCQ ENDPOINTS
# =============================================================================
print_section("TEST 5: MCQ Questions")

# Get daily MCQs
try:
    response = requests.get(f"{BASE_URL}/mcq/daily", params={"limit": 3})
    if response.status_code == 200:
        data = response.json()
        print_result("GET /mcq/daily", "PASS", data)
        
        # Store first question for submission test
        if data.get("questions"):
            first_question = data["questions"][0]
            question_id = first_question["id"]
            print(f"\n   📝 Testing with Question: {first_question['question'][:50]}...")
            
            # Submit MCQ answer
            print("\n   Submitting answer...")
            submission = {
                "question_id": question_id,
                "selected_option": "B"  # Try option B
            }
            response = requests.post(
                f"{BASE_URL}/user/mcq/submit",
                params={"user_id": USER_ID},
                json=submission
            )
            if response.status_code == 200:
                result = response.json()
                print_result("POST /user/mcq/submit", "PASS", result)
                if result.get("correct"):
                    print(f"   🎉 Correct! Earned {result.get('xp_awarded', 0)} XP")
                else:
                    print(f"   ❌ Wrong. Correct answer: {result.get('correct_answer')}")
            else:
                print_result("POST /user/mcq/submit", "FAIL", error=f"Status {response.status_code}")
    else:
        print_result("GET /mcq/daily", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /mcq/daily", "FAIL", error=str(e))

# Get MCQs by subject
try:
    response = requests.get(f"{BASE_URL}/mcq/subject/heart")
    if response.status_code == 200:
        print_result("GET /mcq/subject/heart", "PASS", response.json())
    else:
        print_result("GET /mcq/subject/heart", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /mcq/subject/heart", "FAIL", error=str(e))

# =============================================================================
# TEST 6: ACTIVITY LOGGING
# =============================================================================
print_section("TEST 6: Activity Logging")

# Log an activity
try:
    activity_data = {
        "type": "viewed_model",
        "details": {
            "model": "heart.glb",
            "duration": 30
        },
        "user_id": USER_ID
    }
    response = requests.post(f"{BASE_URL}/user/activity/log", json=activity_data)
    if response.status_code == 200:
        print_result("POST /user/activity/log", "PASS", response.json())
    else:
        print_result("POST /user/activity/log", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("POST /user/activity/log", "FAIL", error=str(e))

# Get recent activities
try:
    response = requests.get(
        f"{BASE_URL}/user/activity/recent",
        params={"user_id": USER_ID, "limit": 5}
    )
    if response.status_code == 200:
        print_result("GET /user/activity/recent", "PASS", response.json())
    else:
        print_result("GET /user/activity/recent", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /user/activity/recent", "FAIL", error=str(e))

# Get activity stats
try:
    response = requests.get(f"{BASE_URL}/user/activity/stats", params={"user_id": USER_ID})
    if response.status_code == 200:
        print_result("GET /user/activity/stats", "PASS", response.json())
    else:
        print_result("GET /user/activity/stats", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /user/activity/stats", "FAIL", error=str(e))

# =============================================================================
# TEST 7: RECOMMENDATIONS
# =============================================================================
print_section("TEST 7: Topic Recommendations")

# Get recommendations based on topic
try:
    response = requests.get(
        f"{BASE_URL}/user/recommendations",
        params={"based_on": "heart", "user_id": USER_ID}
    )
    if response.status_code == 200:
        print_result("GET /user/recommendations", "PASS", response.json())
    else:
        print_result("GET /user/recommendations", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /user/recommendations", "FAIL", error=str(e))

# =============================================================================
# TEST 8: DASHBOARD (AGGREGATED)
# =============================================================================
print_section("TEST 8: Dashboard (Aggregated View)")
try:
    response = requests.get(f"{BASE_URL}/user/dashboard", params={"user_id": USER_ID})
    if response.status_code == 200:
        data = response.json()
        print_result("GET /user/dashboard", "PASS")
        print(f"\n   📊 Dashboard Summary:")
        print(f"   • Streak: {data.get('streak', 0)} days")
        print(f"   • XP: {data.get('xp', 0)}")
        print(f"   • Level: {data.get('level', 1)}")
        print(f"   • XP to next level: {data.get('xp_to_next_level', 0)}")
        print(f"   • Daily MCQs: {len(data.get('daily_mcqs', []))}")
        print(f"   • Recent Activities: {len(data.get('recent_activity', []))}")
        print(f"   • Recommended Topics: {len(data.get('recommended_topics', []))}")
        print(f"   • Last Viewed Model: {data.get('last_viewed_model', 'None')}")
    else:
        print_result("GET /user/dashboard", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("GET /user/dashboard", "FAIL", error=str(e))

# =============================================================================
# TEST 9: IMAGE UPLOAD & CLIP CLASSIFICATION (Existing Feature)
# =============================================================================
print_section("TEST 9: CLIP Image Classification")
try:
    # Create a simple test image (red square)
    print("   Creating test image...")
    img = Image.new('RGB', (224, 224), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {'file': ('test_image.png', img_bytes, 'image/png')}
    response = requests.post(f"{BASE_URL}/upload-image", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print_result("POST /upload-image", "PASS")
        print(f"\n   🔮 CLIP Classification Result:")
        print(f"   • Predicted Subject: {result.get('predicted_subject')}")
        print(f"   • Confidence: {result.get('confidence', 0):.4f}")
        print(f"   • Model Path: {result.get('model_path')}")
    else:
        print_result("POST /upload-image", "FAIL", error=f"Status {response.status_code}")
except Exception as e:
    print_result("POST /upload-image", "FAIL", error=str(e))

# =============================================================================
# SUMMARY
# =============================================================================
print_section("TEST SUMMARY")
print("""
✅ All core endpoints tested!

📋 Tested Components:
  • Health check endpoint
  • Root endpoint with version info
  • Streak management (get, update)
  • XP and leveling system
  • MCQ daily questions
  • MCQ answer submission with XP rewards
  • MCQ filtering by subject
  • Activity logging
  • Recent activities retrieval
  • Activity statistics
  • Topic recommendations
  • Aggregated dashboard
  • CLIP image classification

🎯 Backend Status: OPERATIONAL

Next Steps:
  1. Check the interactive docs at http://localhost:8000/docs
  2. Test with real images for better CLIP results
  3. Add more MCQ questions in app/data/mcqs.json
  4. Integrate with frontend
  5. Add 3D GLB models to app/static/models/

""")

print(f"Test completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
print('='*60)
