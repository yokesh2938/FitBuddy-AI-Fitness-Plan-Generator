import os
import json
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

# Initialize Google Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing.")

client = genai.Client(api_key=GEMINI_API_KEY)

# Single HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fit Buddy - AI Fitness Assistant</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #f4f7f6;
            color: #333;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
        .card {
            background: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .card h2 {
            margin-bottom: 20px;
            color: #16a085;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }
        select, input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 1rem;
        }
        button {
            width: 100%;
            background-color: #16a085;
            color: white;
            border: none;
            padding: 12px;
            font-size: 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }
        button:hover {
            background-color: #117a65;
        }
        .hidden {
            display: none;
        }
        #workout-output {
            margin-top: 25px;
            border-top: 2px solid #eee;
            padding-top: 15px;
        }
        .exercise-card {
            background: #f8f9fa;
            border-left: 4px solid #16a085;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .disclaimer {
            font-size: 0.85rem;
            color: #7f8c8d;
            margin-top: 15px;
            font-style: italic;
        }
        .chat-box {
            height: 300px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 15px;
            overflow-y: auto;
            margin-bottom: 15px;
            background-color: #fafafa;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            padding: 10px 14px;
            border-radius: 10px;
            max-width: 80%;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        .message.user {
            background-color: #16a085;
            color: white;
            align-self: flex-end;
        }
        .message.bot {
            background-color: #e9ecef;
            color: #212529;
            align-self: flex-start;
        }
        .chat-input-container {
            display: flex;
            gap: 10px;
        }
        .chat-input-container button {
            width: 30%;
        }
    </style>
</head>
<body>
    <header>
        <h1>🏋️‍♂️ Fit Buddy</h1>
        <p>Your Personal AI Workout Coach & Nutritionist</p>
    </header>

    <main class="container">
        <!-- Generator Section -->
        <section class="card">
            <h2>Generate Your Workout</h2>
            <form id="workout-form">
                <div class="form-group">
                    <label for="goal">Fitness Goal</label>
                    <select id="goal">
                        <option value="Muscle Building">Muscle Building</option>
                        <option value="Fat Loss">Fat Loss</option>
                        <option value="Endurance & Cardio">Endurance & Cardio</option>
                        <option value="General Health">General Health</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="level">Experience Level</label>
                    <select id="level">
                        <option value="Beginner">Beginner</option>
                        <option value="Intermediate">Intermediate</option>
                        <option value="Advanced">Advanced</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="equipment">Equipment Available</label>
                    <select id="equipment">
                        <option value="Dumbbells Only">Dumbbells Only</option>
                        <option value="Bodyweight Only">Bodyweight Only</option>
                        <option value="Full Gym">Full Gym</option>
                        <option value="Resistance Bands">Resistance Bands</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="duration">Duration</label>
                    <select id="duration">
                        <option value="15 minutes">15 Minutes</option>
                        <option value="30 minutes" selected>30 Minutes</option>
                        <option value="45 minutes">45 Minutes</option>
                        <option value="60 minutes">60 Minutes</option>
                    </select>
                </div>

                <button type="submit" id="generate-btn">Generate Routine</button>
            </form>

            <div id="workout-output" class="hidden">
                <h3 id="workout-title"></h3>
                <div id="exercise-list"></div>
                <p id="safety-disclaimer" class="disclaimer"></p>
            </div>
        </section>

        <!-- Chat Section -->
        <section class="card">
            <h2>Chat with Fit Buddy</h2>
            <div id="chat-box" class="chat-box">
                <div class="message bot">Hi! I'm Fit Buddy. How can I help you reach your goals today?</div>
            </div>
            <div class="chat-input-container">
                <input type="text" id="chat-input" placeholder="Ask about exercises, form, or nutrition...">
                <button id="send-btn">Send</button>
            </div>
        </section>
    </main>

    <script>
        const chatHistory = [];

        // Handle Workout Generation
        document.getElementById('workout-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const generateBtn = document.getElementById('generate-btn');
            generateBtn.innerText = "Generating Routine...";
            generateBtn.disabled = true;

            const payload = {
                goal: document.getElementById('goal').value,
                level: document.getElementById('level').value,
                equipment: document.getElementById('equipment').value,
                duration: document.getElementById('duration').value
            };

            try {
                const response = await fetch('/api/workout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                
                if (result.success) {
                    displayWorkout(result.data);
                } else {
                    alert('Error generating workout: ' + result.error);
                }
            } catch (err) {
                alert('Network error. Failed to reach server.');
            } finally {
                generateBtn.innerText = "Generate Routine";
                generateBtn.disabled = false;
            }
        });

        function displayWorkout(data) {
            const outputDiv = document.getElementById('workout-output');
            const titleEl = document.getElementById('workout-title');
            const listEl = document.getElementById('exercise-list');
            const disclaimerEl = document.getElementById('safety-disclaimer');

            titleEl.innerText = data.title;
            listEl.innerHTML = '';

            data.exercises.forEach(ex => {
                const card = document.createElement('div');
                card.className = 'exercise-card';
                card.innerHTML = `
                    <strong>${ex.name}</strong><br>
                    <span>Sets: ${ex.sets} | Reps: ${ex.reps} | Rest: ${ex.rest}</span>
                    ${ex.notes ? `<p><small>${ex.notes}</small></p>` : ''}
                `;
                listEl.appendChild(card);
            });

            disclaimerEl.innerText = data.safety_disclaimer || '';
            outputDiv.classList.remove('hidden');
        }

        // Handle Chat
        document.getElementById('send-btn').addEventListener('click', sendMessage);
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        async function sendMessage() {
            const inputEl = document.getElementById('chat-input');
            const text = inputEl.value.trim();
            if (!text) return;

            appendMessage('user', text);
            inputEl.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, history: chatHistory })
                });

                const result = await response.json();

                if (result.success) {
                    appendMessage('bot', result.reply);
                    chatHistory.push({ sender: 'user', text: text });
                    chatHistory.push({ sender: 'bot', text: result.reply });
                } else {
                    appendMessage('bot', 'Sorry, I encountered an error answering that.');
                }
            } catch (err) {
                appendMessage('bot', 'Network error. Please try again.');
            }
        }

        function appendMessage(sender, text) {
            const chatBox = document.getElementById('chat-box');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            msgDiv.innerText = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

# Endpoint 1: Generate Structured Workout Plan
@app.route("/api/workout", methods=["POST"])
def generate_workout():
    try:
        data = request.json or {}
        goal = data.get("goal", "General Fitness")
        level = data.get("level", "Beginner")
        equipment = data.get("equipment", "Bodyweight")
        duration = data.get("duration", "30 minutes")

        prompt = f"""
        Generate a personalized workout routine for a user with the following details:
        - Fitness Goal: {goal}
        - Experience Level: {level}
        - Available Equipment: {equipment}
        - Workout Duration: {duration}

        Return a structured list of exercises with sets, reps, rest times, and safety tips.
        """

        system_instruction = "You are Fit Buddy, a certified AI fitness coach. Provide realistic, safe, and structured workout advice."

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
                    "required": ["title", "exercises", "safety_disclaimer"]
                }
            )
        )

        structured_data = json.loads(response.text)
        return jsonify({"success": True, "data": structured_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Endpoint 2: Interactive Fitness Chatbot
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "")
        history = data.get("history", [])

        if not user_message:
            return jsonify({"success": False, "error": "Message cannot be empty"}), 400

        contents = []
        for msg in history:
            role = "user" if msg.get("sender") == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.get("text", ""))]))
        
        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

        system_instruction = (
            "You are Fit Buddy, an empathetic, encouraging AI workout coach and nutritionist. "
            "Provide concise, actionable advice. If users ask about severe pain or medical conditions, "
            "advise them to consult a healthcare professional."
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
