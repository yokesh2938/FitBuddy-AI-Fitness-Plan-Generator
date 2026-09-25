import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing in .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/workout", methods=["POST"])
def generate_workout():
    try:
        data = request.json or {}
        goal = data.get("goal", "General Fitness")
        level = data.get("level", "Intermediate")
        equipment = data.get("equipment", "Dumbbells Only")
        duration = data.get("duration", "35 minutes")

        prompt = f"""
        Generate a personalized workout routine for a user with the following details:
        - Goal: {goal}
        - Level: {level}
        - Equipment: {equipment}
        - Duration: {duration}

        Return a structured workout plan.
        """

        system_instruction = "You are Fit Buddy Pro, an elite certified AI fitness trainer. Return concise, highly optimized exercise protocols."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING"},
                        "duration": {"type": "STRING"},
                        "exercises": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "name": {"type": "STRING"},
                                    "sets": {"type": "STRING"},
                                    "reps": {"type": "STRING"},
                                    "rest": {"type": "STRING"},
                                    "notes": {"type": "STRING"}
                                },
                                "required": ["name", "sets", "reps", "rest"]
                            }
                        },
                        "safety_disclaimer": {"type": "STRING"}
                    },
                    "required": ["title", "duration", "exercises", "safety_disclaimer"]
                }
            )
        )

        structured_data = json.loads(response.text)
        return jsonify({"success": True, "data": structured_data})

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
            "You are Fit Buddy Pro, an empathetic and highly knowledgeable AI exercise scientist and sports nutritionist. "
            "Deliver direct, actionable answers. Warn users to consult physicians for joint pain or injuries."
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
