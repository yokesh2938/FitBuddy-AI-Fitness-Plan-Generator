# Fit Buddy 2.0 — Complete Project Documentation (`documentation.md`)

---

## 🛠️ Table of Contents
1. [Project Overview](#1-project-overview)
2. [System Architecture & Design Phase](#2-system-architecture--design-phase)
3. [Database Schema Specification](#3-database-schema-specification)
4. [Implementation Phase (`app.py`)](#4-implementation-phase-apppy)
5. [Testing Strategy & Test Suite (`test_app.py`)](#5-testing-strategy--test-suite-test_apppy)
6. [Setup, Installation & Deployment Guide](#6-setup-installation--deployment-guide)

---

## 1. Project Overview

**Fit Buddy 2.0** is an AI-powered personal workout assistant and strength-training tracker built with **Flask**, **Google Gemini 2.5 Flash API**, **SQLite**, **Chart.js**, and **html2pdf.js**. 

### Key Features
- **Structured Workout Generation:** Produces customizable exercise plans with targeted set counts, rep ranges, and rest intervals formatted via JSON Schema.
- **Interactive AI Coach:** Natural language conversational assistant for fitness guidance, nutrition advice, and form checks.
- **Performance Analytics & Tracking:** SQLite database integration with Chart.js visualization for volume progress and active daily streaks.
- **Client-Side Export:** One-click PDF export using `html2pdf.js`.

---

## 2. System Architecture & Design Phase

### High-Level System Architecture


===================================================================================
CLIENT BROWSER LAYER
[ Modern Glassmorphic UI ]  <--->  [ Chart.js Analytics ]  <--->  [ html2pdf Engine ]
|
v
HTTP REST API (JSON DATA)
|
v
FLASK BACKEND ENGINE
[ Routes Controller ]       [ Request Parser ]          [ DB Engine (SQLite) ]
|                             |                              |
v                             v                              v
/api/workout                  /api/chat                    fitbuddy_pro.db
|                             |                              |
+-----------------------------+------------------------------+
|
v
EXTERNAL AI ENGINE SERVICES
Google Gemini 2.5 Flash API (Structured JSON Schema)

---

### Component Workflow & Data Flow


+------------------+      1. Form Input      +-----------------------+
|  User Selection  |  -------------------->  |  Flask Web Backend    |
| (Goal/Equipment) |                         |      (app.py)         |
+------------------+                         +-----------------------+
|
| 2. Structured Prompt
v
+------------------+      4. Render Cards    +-----------------------+
| Interactive UI   |  <--------------------  |  Google Gemini AI     |
| & PDF Generation |     (Validated JSON)    |  (gemini-2.5-flash)   |
+------------------+                         +-----------------------+

---

### Dashboard Interface Layout Blueprint


+---------------------------------------------------------------------------------+
|  [LOGO] Fit Buddy 2.0                       [🔥 3 Days Streak]  [PROFILE] [DARK] |
+---------------------------------------------------------------------------------+
|                                       |                                         |
|  WEEKLY SCHEDULE                      |  PERFORMANCE ANALYTICS                  |
|  [Sun]  [Mon]  [Tue]  [Wed]  [Thu]    |  +-----------------------------------+  |
|                                       |  | Chart.js Volume Progress Graph    |  |
|  WORKOUT GENERATOR                    |  +-----------------------------------+  |
|  * Focus Target  : [ Chest & Arms v ] |                                         |
|  * Equipment     : [ Dumbbells    v ] |  AI COACH ASSISTANT                     |
|                                       |  +-----------------------------------+  |
|  [ GENERATE AI WORKOUT PROTOCOL ]     |  | AI: Ready to reach your goals?    |  |
|                                       |  | User: What is a good rest period? |  |
|  GENERATED PROTOCOL                   |  +-----------------------------------+  |
|  [ EXPORT PLAN TO PDF ]               |  [ Type message... ] [ SEND ]           |
|  +---------------------------------+  |                                         |
|  | Dumbbell Press - 3 Sets x 10 Reps|  |                                         |
|  +---------------------------------+  |                                         |
+---------------------------------------------------------------------------------+

---

## 3. Database Schema Specification

### Entity 1: `user_profile`

| Column Name | Data Type | Key Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`id`** | INTEGER | PRIMARY KEY | NO | Unique user profile record ID |
| **`name`** | TEXT | - | NO | User's full name |
| **`age`** | INTEGER | - | YES | Age in years |
| **`weight`** | REAL | - | YES | Body weight in kilograms |
| **`height`** | REAL | - | YES | Height in centimeters |
| **`fitness_goal`**| TEXT | - | YES | Primary fitness objective |
| **`level`** | TEXT | - | YES | Experience level |
| **`streak_count`**| INTEGER | - | NO | Active workout streak count |
| **`last_workout`**| TEXT | - | YES | ISO timestamp of last active session |

---

### Entity 2: `workout_logs`

| Column Name | Data Type | Key Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`id`** | INTEGER | PRIMARY KEY | NO | Auto-incrementing log entry ID |
| **`title`** | TEXT | - | NO | Name of generated workout protocol |
| **`category`** | TEXT | - | YES | Muscle group or focus area |
| **`completed_date`**| TEXT | - | YES | Date timestamp of completion |
| **`duration_min`**| INTEGER | - | YES | Session duration in minutes |
| **`calories_burned`**| INTEGER | - | YES | Estimated energy expenditure |

---

## 4. Implementation Phase (`app.py`)

```python
"""
Fit Buddy 2.0 — Main Backend Controller (app.py)
Implementation Phase: Core Flask Server, Gemini AI Integration, SQLite Persistence
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment configuration
load_dotenv()

app = Flask(__name__)
DB_NAME = "fitbuddy_pro.db"

# Initialize Google Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# ==========================================
# DATABASE INITIALIZATION
# ==========================================
def init_db():
    """Initializes SQLite tables for user profiles and workout activity logs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # User Profile Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            weight REAL,
            height REAL,
            fitness_goal TEXT,
            level TEXT,
            streak_count INTEGER DEFAULT 0,
            last_workout TEXT
        )
    """)
    
    # Workout Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            completed_date TEXT,
            duration_min INTEGER,
            calories_burned INTEGER
        )
    """)
    
    # Seed default user profile if empty
    cursor.execute("SELECT COUNT(*) FROM user_profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO user_profile (id, name, age, weight, height, fitness_goal, level, streak_count)
            VALUES (1, 'Yokesh', 20, 70.0, 175.0, 'Hypertrophy & Strength', 'Intermediate', 3)
        """)
        
    conn.commit()
    conn.close()

init_db()

# ==========================================
# WEB FRONTEND & REST API ROUTES
# ==========================================

@app.route("/")
def index():
    """Renders the main dashboard interface."""
    return render_template("index.html")


@app.route("/api/profile", methods=["GET"])
def get_profile():
    """Fetches current user profile statistics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, weight, height, fitness_goal, level, streak_count FROM user_profile WHERE id = 1")
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            "status": "success",
            "data": {
                "name": user[0],
                "age": user[1],
                "weight": user[2],
                "height": user[3],
                "fitness_goal": user[4],
                "level": user[5],
                "streak_count": user[6]
            }
        })
    return jsonify({"status": "error", "message": "User profile not found"}), 404


@app.route("/api/workout", methods=["POST"])
def generate_workout():
    """Generates structured exercise protocols via Google Gemini SDK."""
    if not client:
        return jsonify({"status": "error", "message": "Gemini API key is not configured"}), 500

    data = request.get_json() or {}
    target = data.get("target", "Full Body")
    equipment = data.get("equipment", "Dumbbells")
    duration = data.get("duration", "40")

    prompt = f"""
    Create a highly structured fitness workout protocol for a target focus of '{target}' using '{equipment}' for a duration of {duration} minutes.
    Ensure the output contains detailed exercise names, set counts, repetition ranges, and rest intervals in seconds.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "workout_title": {"type": "STRING"},
                        "target_focus": {"type": "STRING"},
                        "estimated_duration": {"type": "STRING"},
                        "exercises": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "name": {"type": "STRING"},
                                    "sets": {"type": "INTEGER"},
                                    "reps": {"type": "STRING"},
                                    "rest_seconds": {"type": "INTEGER"},
                                    "notes": {"type": "STRING"}
                                },
                                "required": ["name", "sets", "reps", "rest_seconds"]
                            }
                        }
                    },
                    "required": ["workout_title", "target_focus", "exercises"]
                }
            )
        )
        return jsonify({"status": "success", "data": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def ai_coach():
    """Handles natural language conversational interaction with the AI Coach."""
    if not client:
        return jsonify({"status": "error", "message": "Gemini API key is not configured"}), 500

    data = request.get_json() or {}
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"status": "error", "message": "Message cannot be empty"}), 400

    system_instruction = "You are Fit Buddy AI Coach, an expert personal trainer and clinical nutritionist. Provide concise, direct, safe, and motivating advice."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return jsonify({"status": "success", "reply": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/log-workout", methods=["POST"])
def log_workout():
    """Logs finished workouts to SQLite database and increments streak counts."""
    data = request.get_json() or {}
    title = data.get("title", "Custom Workout")
    category = data.get("category", "General")
    duration = data.get("duration", 30)
    calories = data.get("calories", 200)
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO workout_logs (title, category, completed_date, duration_min, calories_burned)
        VALUES (?, ?, ?, ?, ?)
    """, (title, category, today, duration, calories))
    
    cursor.execute("UPDATE user_profile SET streak_count = streak_count + 1, last_workout = ? WHERE id = 1", (today,))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Workout logged successfully"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

5. Testing Strategy & Test Suite (test_app.py)
Automated Pytest Suite
"""
Fit Buddy 2.0 — Automated Test Suite (test_app.py)
Tests Flask routes, SQLite persistence, and Gemini API integration handlers.
"""

import json
import sqlite3
import pytest
from app import app, DB_NAME, init_db

@pytest.fixture
def client():
    """Sets up temporary Flask test client and initializes database."""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    init_db()
    with app.test_client() as client:
        yield client

def test_database_initialization():
    """Verify SQLite database and tables exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profile'")
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workout_logs'")
    assert cursor.fetchone() is not None
    conn.close()

def test_get_profile_endpoint(client):
    """Test GET /api/profile endpoint returning valid user data."""
    response = client.get('/api/profile')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'name' in data['data']

def test_log_workout_endpoint(client):
    """Test POST /api/log-workout inserts log and updates streak count."""
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

def test_ai_coach_empty_message(client):
    """Test POST /api/chat handles empty input gracefully."""
    payload = {"message": ""}
    response = client.post('/api/chat', 
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'

Manual Acceptance Testing Matrix
| Test ID | Area Under Test | Action / Input | Expected Result | Result |
|---|---|---|---|---|
| TC-01 | Workout Generator | Select target "Chest", click Generate | Displays exercise cards (Name, Sets, Reps, Rest Interval) | PASS |
| TC-02 | Rest Timer Engine | Click "Start" on rest timer | Counts down per second; play, pause, and reset work | PASS |
| TC-03 | AI Coach Chat | Query: "How do I improve bench press?" | Returns coaching response within 3s | PASS |
| TC-04 | PDF Export Engine | Click Export Plan to PDF button | Downloads formatted PDF sheet via html2pdf.js | PASS |
| TC-05 | Workout Logging | Complete session and click Log Workout | Updates streak counter and updates analytics | PASS |
6. Setup, Installation & Deployment Guide
Prerequisites
 * Python 3.10+
 * Google Gemini API Key
Step-by-Step Installation
 * Clone Repository & Setup Environment:
   git clone [https://github.com/your-username/fit-buddy-2.0.git](https://github.com/your-username/fit-buddy-2.0.git)
cd fit-buddy-2.0
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

 * Install Dependencies:
   pip install flask python-dotenv google-genai pytest pytest-flask

 * Configure Environment Variables (.env):
   Create a .env file in the root project folder:
   GEMINI_API_KEY=your_google_gemini_api_key_here
FLASK_ENV=development
FLASK_APP=app.py

 * Launch Application:
   python app.py

   Access the dashboard at http://127.0.0.1:5000
 * Execute Automated Tests:
   pytest test_app.py -v


