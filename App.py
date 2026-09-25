import os
import json
import sqlite3
from flask import Flask, request, jsonify, render_template, g
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
DATABASE = 'database.db'

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

# --- DATABASE SETUP ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY DEFAULT 1,
                weight_kg REAL,
                height_cm REAL,
                age INTEGER,
                gender TEXT,
                activity_level TEXT,
                bmr INTEGER,
                tdee INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                plan_json TEXT
            )
        ''')
        db.commit()

init_db()

# --- BMR / TDEE MATH ENGINE ---
def calculate_metrics(weight, height, age, gender, activity):
    if gender.lower() == 'female':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725
    }
    tdee = bmr * multipliers.get(activity, 1.375)
    return int(bmr), int(tdee)

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/profile", methods=["GET", "POST"])
def user_profile():
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        data = request.json or {}
        weight = float(data.get("weight", 70))
        height = float(data.get("height", 175))
        age = int(data.get("age", 25))
        gender = data.get("gender", "male")
        activity = data.get("activity", "moderately_active")

        bmr, tdee = calculate_metrics(weight, height, age, gender, activity)

        cursor.execute('''
            INSERT INTO user_profile (id, weight_kg, height_cm, age, gender, activity_level, bmr, tdee)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                weight_kg=excluded.weight_kg,
                height_cm=excluded.height_cm,
                age=excluded.age,
                gender=excluded.gender,
                activity_level=excluded.activity_level,
                bmr=excluded.bmr,
                tdee=excluded.tdee
        ''', (weight, height, age, gender, activity, bmr, tdee))
        db.commit()

        return jsonify({"success": True, "bmr": bmr, "tdee": tdee})
    else:
        cursor.execute('SELECT * FROM user_profile WHERE id = 1')
        row = cursor.fetchone()
        if row:
            return jsonify({"success": True, "profile": dict(row)})
        return jsonify({"success": False, "message": "No profile saved yet"})

@app.route("/api/generate-master-plan", methods=["POST"])
def generate_master_plan():
    try:
        data = request.json or {}
        goal = data.get("goal", "Muscle Hypertrophy")
        level = data.get("level", "Intermediate")
        equipment = data.get("equipment", "Full Gym")
        dietary_style = data.get("dietary_style", "High Protein Balanced")
        allergies = data.get("allergies", "None")
        weight = data.get("weight", 70)
        height = data.get("height", 175)
        age = data.get("age", 25)
        gender = data.get("gender", "male")
        activity = data.get("activity", "moderately_active")

        bmr, tdee = calculate_metrics(float(weight), float(height), int(age), gender, activity)

        prompt = f"""
        Design an elite multi-tier training and clinical-grade nutrition roadmap for a client with the following metrics:
        - Biometrics: {weight} kg, {height} cm, {age} y/o, {gender}
        - Computed Basal Metabolic Rate (BMR): {bmr} kcal/day
        - Total Daily Energy Expenditure (TDEE): {tdee} kcal/day
        - Target Goal: {goal}
        - Experience Level: {level}
        - Equipment Available: {equipment}
        - Nutrition Style: {dietary_style}
        - Dietary Restrictions / Allergies: {allergies}

        Return a complete JSON dataset containing precise exercise routines, target macronutrient grams, complete daily meal schedules, and hydration protocols.
        """

        system_instruction = (
            "You are Fit Buddy Pro Master Engine, an expert sports scientist, clinical dietitian, and kinesiology researcher. "
            "Deliver strict, granular JSON output formatted to absolute professional standard."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "plan_title": {"type": "STRING"},
                        "target_daily_calories": {"type": "STRING"},
                        "macro_targets": {
                            "type": "OBJECT",
                            "properties": {
                                "protein_grams": {"type": "STRING"},
                                "carbs_grams": {"type": "STRING"},
                                "fats_grams": {"type": "STRING"}
                            },
                            "required": ["protein_grams", "carbs_grams", "fats_grams"]
                        },
                        "water_intake_liters": {"type": "STRING"},
                        "workout_protocol": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "exercise_name": {"type": "STRING"},
                                    "target_sets": {"type": "STRING"},
                                    "target_reps": {"type": "STRING"},
                                    "rest_period": {"type": "STRING"},
                                    "coaching_cue": {"type": "STRING"}
                                },
                                "required": ["exercise_name", "target_sets", "target_reps", "rest_period", "coaching_cue"]
                            }
                        },
                        "diet_protocol": {
                            "type": "OBJECT",
                            "properties": {
                                "breakfast": {"type": "STRING"},
                                "morning_snack": {"type": "STRING"},
                                "lunch": {"type": "STRING"},
                                "pre_workout": {"type": "STRING"},
                                "post_workout": {"type": "STRING"},
                                "dinner": {"type": "STRING"}
                            },
                            "required": ["breakfast", "lunch", "pre_workout", "post_workout", "dinner"]
                        },
                        "supplement_suggestions": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        },
                        "recovery_advice": {"type": "STRING"}
                    },
                    "required": ["plan_title", "target_daily_calories", "macro_targets", "water_intake_liters", "workout_protocol", "diet_protocol", "supplement_suggestions", "recovery_advice"]
                }
            )
        )

        structured_data = json.loads(response.text)

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO saved_plans (plan_json) VALUES (?)', (json.dumps(structured_data),))
        db.commit()

        return jsonify({"success": True, "bmr": bmr, "tdee": tdee, "data": structured_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/analyze-multimodal", methods=["POST"])
def analyze_multimodal():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files['image']
        analysis_mode = request.form.get("mode", "food_scan")
        image_bytes = file.read()
        mime_type = file.mimetype or "image/jpeg"

        if analysis_mode == "food_scan":
            prompt = """
            Analyze this meal image as a clinical nutritionist.
            1. Identify all visible ingredients.
            2. Estimate total calories and macronutrients (Protein, Carbs, Fat in grams).
            3. Rate meal healthiness (1-10) and provide 2 tips to optimize it.
            """
        else:
            prompt = """
            Analyze this exercise photo/posture as a certified biomechanics specialist.
            1. Identify the exercise being performed.
            2. Evaluate body posture, alignment, and joint stability.
            3. Highlight key safety checks and recommendations to reduce injury risk.
            """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt
            ]
        )

        return jsonify({"success": True, "analysis": response.text})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "")
        history = data.get("history", [])

        if not user_message:
            return jsonify({"success": False, "error": "Message required"}), 400

        contents = []
        for msg in history:
            role = "user" if msg.get("sender") == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.get("text", ""))]))

        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

        system_instruction = (
            "You are Fit Buddy Pro AI Assistant, a top-tier exercise scientist and sports dietitian. "
            "Provide direct, science-backed answers. Recommend physician consultation for severe pain."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )

        return jsonify({"success": True, "reply": response.text})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
