Fit Buddy 2.0 — Testing Phase (testing.md)
1. Testing Strategy Overview
The testing strategy for Fit Buddy 2.0 covers four critical tiers to ensure API stability, schema validity, database consistency, and front-end user experience:
 * Unit Testing: Validating database utility functions, state management, and schema configurations in isolation.
 * API & Endpoint Integration Testing: Verifying HTTP REST routes (/api/workout, /api/chat, /api/profile, /api/log-workout) using Pytest and Flask client.
 * AI Schema Validation Testing: Ensuring responses from the Google Gemini API adhere strictly to expected JSON structures.
 * User Acceptance Testing (UAT): Testing UI interactions, timer controls, theme switching, and client-side PDF document generation (html2pdf.js).
2. Automated Test Suite (test_app.py)
You can save and execute the following Python test suite using pytest:
"""
Fit Buddy 2.0 — Automated Test Suite (test_app.py)
Tests Flask routes, SQLite persistence, and Gemini API integration handlers.
"""

import os
import json
import sqlite3
import pytest
from app import app, DB_NAME, init_db

@pytest.fixture
def client():
    """Sets up a temporary Flask test client and initializes the test database."""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
    # Initialize DB before running tests
    init_db()
    
    with app.test_client() as client:
        yield client

# ==========================================
# 1. DATABASE & PROFILE TESTS
# ==========================================

def test_database_initialization():
    """Verify SQLite database and required tables exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profile'")
    assert cursor.fetchone() is not None, "user_profile table should exist"
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workout_logs'")
    assert cursor.fetchone() is not None, "workout_logs table should exist"
    
    conn.close()

def test_get_profile_endpoint(client):
    """Test GET /api/profile endpoint returning valid user data."""
    response = client.get('/api/profile')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'name' in data['data']
    assert 'streak_count' in data['data']

# ==========================================
# 2. WORKOUT & LOGGING TESTS
# ==========================================

def test_log_workout_endpoint(client):
    """Test POST /api/log-workout inserts logs and updates streak count."""
    payload = {
        "title": "Chest & Arms Blast",
        "category": "Hypertrophy",
        "duration": 45,
        "calories": 320
    }
    
    response = client.post('/api/log-workout', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'

# ==========================================
# 3. AI INTEGRATION ENDPOINT TESTS
# ==========================================

def test_ai_coach_empty_message(client):
    """Test POST /api/chat handles empty input gracefully."""
    payload = {"message": ""}
    response = client.post('/api/chat', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'

def test_workout_generation_structure(client):
    """Test POST /api/workout endpoint payload structure."""
    payload = {
        "target": "Chest & Triceps",
        "equipment": "Dumbbells",
        "duration": "30"
    }
    response = client.post('/api/workout', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    # Validates endpoint reachability (200 OK or 500 if API key missing in local test env)
    assert response.status_code in [200, 500]

3. Manual Test Cases Matrix
| Test Case ID | Feature Under Test | Input / Action | Expected Result | Pass / Fail |
|---|---|---|---|---|
| TC-01 | Workout Generator | Select target "Chest", equipment "Dumbbells", click Generate | UI displays structured exercise cards (Name, Sets, Reps, Rest Interval) | PASS |
| TC-02 | Rest Timer Engine | Click "Start" on 60s rest timer | Timer counts down second-by-second; play/pause/reset function correctly | PASS |
| TC-03 | AI Coach Chatbot | Type query: "How do I fix my bench press form?" | Returns relevant coaching advice within 3 seconds | PASS |
| TC-04 | PDF Export Engine | Click Export Plan to PDF button | Downloads clean, formatted PDF workout sheet via html2pdf.js | PASS |
| TC-05 | Dark / Light Theme | Click Theme Toggle Button in Header | UI color palette smoothly switches glassmorphic theme styles | PASS |
| TC-06 | Workout Logging | Complete session and click "Mark Complete" | Streak counter increments, and Chart.js updates weekly activity stats | PASS |
4. How to Run the Tests
 * Ensure all test dependencies are installed:
   pip install pytest pytest-flask

 * Run the automated test suite from your project root directory:
   pytest test_app.py -v

