import os
import json
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing.")

client = genai.Client(api_key=GEMINI_API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fit Buddy Pro — AI Fitness & Nutrition Companion</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-main: #0b0f19;
            --card-bg: rgba(22, 30, 46, 0.7);
            --card-border: rgba(255, 255, 255, 0.08);
            --primary: #00f2fe;
            --primary-gradient: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
            --accent-gradient: linear-gradient(135deg, #f857a6 0%, #ff5858 100%);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --glass-glow: rgba(0, 198, 255, 0.15);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-main);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 114, 255, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(248, 87, 166, 0.08) 0%, transparent 40%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px 16px;
        }

        /* Top Bar */
        header {
            max-width: 1200px;
            margin: 0 auto 32px auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(16px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 44px;
            height: 44px;
            background: var(--primary-gradient);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            color: #fff;
            box-shadow: 0 4px 15px rgba(0, 198, 255, 0.4);
        }

        .brand h1 {
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #ffffff, #a5f3fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .streak-badge {
            background: rgba(255, 88, 88, 0.15);
            border: 1px solid rgba(255, 88, 88, 0.3);
            color: #ff5858;
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Main Grid Layout */
        .dashboard-grid {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1.1fr;
            gap: 28px;
        }

        @media (max-width: 992px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.25);
            position: relative;
            overflow: hidden;
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }

        .card-header i {
            font-size: 1.2rem;
            color: var(--primary);
        }

        .card-header h2 {
            font-size: 1.25rem;
            font-weight: 700;
        }

        /* Form Controls */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .form-group.full-width {
            grid-column: span 2;
        }

        label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        select, input[type="text"] {
            width: 100%;
            background: rgba(11, 15, 25, 0.6);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s ease;
        }

        select:focus, input[type="text"]:focus {
            border-color: #00c6ff;
            box-shadow: 0 0 12px rgba(0, 198, 255, 0.25);
        }

        .btn-primary {
            width: 100%;
            background: var(--primary-gradient);
            color: #fff;
            border: none;
            padding: 14px;
            border-radius: 14px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 6px 20px rgba(0, 198, 255, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 198, 255, 0.45);
        }

        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* Dynamic Workout Display */
        #workout-output {
            margin-top: 28px;
            border-top: 1px solid var(--card-border);
            padding-top: 24px;
        }

        .workout-title-card {
            background: rgba(0, 198, 255, 0.08);
            border: 1px solid rgba(0, 198, 255, 0.2);
            padding: 16px 20px;
            border-radius: 16px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .workout-title-card h3 {
            font-size: 1.1rem;
            color: #fff;
        }

        .exercise-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 16px 20px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: border-color 0.2s, transform 0.2s;
        }

        .exercise-card:hover {
            border-color: rgba(0, 198, 255, 0.4);
            transform: translateX(4px);
        }

        .ex-info h4 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .ex-meta {
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            gap: 12px;
        }

        .ex-meta span {
            color: var(--primary);
            font-weight: 600;
        }

        .timer-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background 0.2s;
        }

        .timer-btn:hover {
            background: var(--primary-gradient);
            color: #fff;
        }

        /* Live Timer Widget */
        .timer-widget {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 16px 20px;
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .timer-display {
            font-size: 1.8rem;
            font-weight: 800;
            font-family: monospace;
            color: var(--primary);
        }

        /* Chat Window */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 520px;
        }

        .chat-box {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 14px;
            padding-right: 8px;
            margin-bottom: 16px;
        }

        .chat-box::-webkit-scrollbar {
            width: 6px;
        }

        .chat-box::-webkit-scrollbar-thumb {
            background: var(--card-border);
            border-radius: 10px;
        }

        .msg {
            max-width: 82%;
            padding: 12px 18px;
            border-radius: 18px;
            font-size: 0.95rem;
            line-height: 1.5;
            animation: fadeIn 0.3s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .msg.user {
            align-self: flex-end;
            background: var(--primary-gradient);
            color: #fff;
            border-bottom-right-radius: 4px;
            box-shadow: 0 4px 15px rgba(0, 114, 255, 0.2);
        }

        .msg.bot {
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            border-bottom-left-radius: 4px;
        }

        .prompt-chips {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 12px;
            margin-bottom: 8px;
        }

        .chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text-muted);
        }

        .chip:hover {
            background: rgba(0, 198, 255, 0.15);
            border-color: rgba(0, 198, 255, 0.4);
            color: var(--primary);
        }

        .chat-input-row {
            display: flex;
            gap: 10px;
        }

        .chat-input-row input {
            flex: 1;
        }

        .chat-input-row button {
            width: auto;
            padding: 0 20px;
        }

        .disclaimer {
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 14px;
            font-style: italic;
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="brand-icon"><i class="fa-solid fa-bolt"></i></div>
            <div>
                <h1>Fit Buddy Pro</h1>
                <p style="font-size: 0.8rem; color: var(--text-muted);">AI Fitness & Nutrition Engine</p>
            </div>
        </div>
        <div class="streak-badge">
            <i class="fa-solid fa-fire"></i> <span id="streak-count">1</span> Day Streak
        </div>
    </header>

    <main class="dashboard-grid">
        
        <!-- WORKOUT GENERATOR -->
        <section class="card">
            <div class="card-header">
                <i class="fa-solid fa-dumbbell"></i>
                <h2>Routine Builder</h2>
            </div>

            <form id="workout-form">
                <div class="form-grid">
                    <div class="form-group">
                        <label>Target Goal</label>
                        <select id="goal">
                            <option value="Hypertrophy & Muscle Building">Muscle Building</option>
                            <option value="Fat Loss & Calorie Burn">Fat Loss</option>
                            <option value="Functional Endurance">Endurance</option>
                            <option value="Core & Mobility">Core & Mobility</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Experience</label>
                        <select id="level">
                            <option value="Beginner">Beginner</option>
                            <option value="Intermediate" selected>Intermediate</option>
                            <option value="Advanced">Advanced</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Equipment</label>
                        <select id="equipment">
                            <option value="Dumbbells Only">Dumbbells Only</option>
                            <option value="Bodyweight Only">Bodyweight Only</option>
                            <option value="Full Commercial Gym">Full Gym</option>
                            <option value="Resistance Bands">Resistance Bands</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Duration</label>
                        <select id="duration">
                            <option value="20 minutes">20 Minutes</option>
                            <option value="35 minutes" selected>35 Minutes</option>
                            <option value="50 minutes">50 Minutes</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="generate-btn" class="btn-primary">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Generate Custom Plan
                </button>
            </form>

            <div id="workout-output" class="hidden">
                <div class="workout-title-card">
                    <div>
                        <h3 id="workout-title"></h3>
                        <p id="workout-duration-text" style="font-size:0.8rem; color: var(--text-muted);"></p>
                    </div>
                    <button class="btn-primary" onclick="markWorkoutComplete()" style="width:auto; padding: 8px 16px; font-size: 0.85rem;">
                        <i class="fa-solid fa-check"></i> Complete
                    </button>
                </div>

                <div id="exercise-list"></div>

                <!-- Timer Widget -->
                <div id="timer-widget" class="timer-widget hidden">
                    <div>
                        <p style="font-size:0.8rem; color:var(--text-muted);">Rest Timer</p>
                        <div id="timer-display" class="timer-display">00:45</div>
                    </div>
                    <div style="display:flex; gap:8px;">
                        <button class="timer-btn" onclick="toggleTimer()"><i id="timer-icon" class="fa-solid fa-play"></i></button>
                        <button class="timer-btn" onclick="resetTimer()"><i class="fa-solid fa-rotate-right"></i></button>
                    </div>
                </div>

                <p id="safety-disclaimer" class="disclaimer"></p>
            </div>
        </section>

        <!-- AI CHAT ASSISTANT -->
        <section class="card chat-container">
            <div class="card-header">
                <i class="fa-solid fa-comments"></i>
                <h2>Fit Buddy Assistant</h2>
            </div>

            <div id="chat-box" class="chat-box">
                <div class="msg bot">
                    Hello Yokesh! I am your AI Coach. Ask me anything about diet, exercise execution, or post-workout recovery.
                </div>
            </div>

            <div class="prompt-chips">
                <div class="chip" onclick="quickPrompt('Give me a 5-minute pre-workout warm-up routine.')">⚡ 5-min Warmup</div>
                <div class="chip" onclick="quickPrompt('High protein vegetarian snack ideas?')">🥗 High Protein Snacks</div>
                <div class="chip" onclick="quickPrompt('How to prevent lower back pain during squats?')">🛡️ Squat Form Tips</div>
            </div>

            <div class="chat-input-row">
                <input type="text" id="chat-input" placeholder="Ask about workouts, form, or nutrition...">
                <button id="send-btn" class="btn-primary"><i class="fa-solid fa-paper-plane"></i></button>
            </div>
        </section>

    </main>

    <script>
        const chatHistory = [];
        let timerInterval = null;
        let secondsLeft = 45;
        let isTimerRunning = false;

        // Workout Generation
        document.getElementById('workout-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('generate-btn');
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Engine Crafting Routine...`;
            btn.disabled = true;

            const payload = {
                goal: document.getElementById('goal').value,
                level: document.getElementById('level').value,
                equipment: document.getElementById('equipment').value,
                duration: document.getElementById('duration').value
            };

            try {
                const res = await fetch('/api/workout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (result.success) {
                    renderWorkout(result.data);
                } else {
                    alert('Error generating routine: ' + result.error);
                }
            } catch (err) {
                alert('Network connection error.');
            } finally {
                btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Custom Plan`;
                btn.disabled = false;
            }
        });

        function renderWorkout(data) {
            document.getElementById('workout-title').innerText = data.title;
            document.getElementById('workout-duration-text').innerText = `Est. Duration: ${data.duration || 'Custom'}`;
            
            const listEl = document.getElementById('exercise-list');
            listEl.innerHTML = '';

            data.exercises.forEach(ex => {
                const card = document.createElement('div');
                card.className = 'exercise-card';
                card.innerHTML = `
                    <div class="ex-info">
                        <h4>${ex.name}</h4>
                        <div class="ex-meta">
                            <span>${ex.sets} Sets</span> • 
                            <span>${ex.reps} Reps</span> • 
                            <span>${ex.rest} Rest</span>
                        </div>
                    </div>
                    <button class="timer-btn" title="Start Rest Timer" onclick="startRestTimer('${ex.rest}')">
                        <i class="fa-solid fa-stopwatch"></i>
                    </button>
                `;
                listEl.appendChild(card);
            });

            document.getElementById('safety-disclaimer').innerText = data.safety_disclaimer || '';
            document.getElementById('workout-output').classList.remove('hidden');
        }

        // Rest Timer System
        function startRestTimer(restString) {
            let seconds = 45;
            const match = restString.match(/(\\d+)/);
            if (match) seconds = parseInt(match[0]);

            secondsLeft = seconds;
            updateTimerDisplay();
            document.getElementById('timer-widget').classList.remove('hidden');
            
            clearInterval(timerInterval);
            isTimerRunning = true;
            document.getElementById('timer-icon').className = 'fa-solid fa-pause';

            timerInterval = setInterval(() => {
                secondsLeft--;
                updateTimerDisplay();
                if (secondsLeft <= 0) {
                    clearInterval(timerInterval);
                    isTimerRunning = false;
                    document.getElementById('timer-icon').className = 'fa-solid fa-play';
                    alert('Rest timer finished! Ready for your next set.');
                }
            }, 1000);
        }

        function toggleTimer() {
            if (isTimerRunning) {
                clearInterval(timerInterval);
                isTimerRunning = false;
                document.getElementById('timer-icon').className = 'fa-solid fa-play';
            } else {
                isTimerRunning = true;
                document.getElementById('timer-icon').className = 'fa-solid fa-pause';
                timerInterval = setInterval(() => {
                    secondsLeft--;
                    updateTimerDisplay();
                    if (secondsLeft <= 0) {
                        clearInterval(timerInterval);
                        isTimerRunning = false;
                        document.getElementById('timer-icon').className = 'fa-solid fa-play';
                    }
                }, 1000);
            }
        }

        function resetTimer() {
            clearInterval(timerInterval);
            secondsLeft = 45;
            isTimerRunning = false;
            document.getElementById('timer-icon').className = 'fa-solid fa-play';
            updateTimerDisplay();
        }

        function updateTimerDisplay() {
            const mins = Math.floor(secondsLeft / 60).toString().padStart(2, '0');
            const secs = (secondsLeft % 60).toString().padStart(2, '0');
            document.getElementById('timer-display').innerText = `${mins}:${secs}`;
        }

        // Streak Count Counter
        function markWorkoutComplete() {
            let current = parseInt(localStorage.getItem('fit_streak') || '1');
            current += 1;
            localStorage.setItem('fit_streak', current);
            document.getElementById('streak-count').innerText = current;
            alert('Workout completed! Streak updated.');
        }

        // Chat System
        document.getElementById('send-btn').addEventListener('click', () => sendChatMessage());
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendChatMessage();
        });

        function quickPrompt(text) {
            document.getElementById('chat-input').value = text;
            sendChatMessage();
        }

        async function sendChatMessage() {
            const inputEl = document.getElementById('chat-input');
            const message = inputEl.value.trim();
            if (!message) return;

            appendMsg('user', message);
            inputEl.value = '';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, history: chatHistory })
                });
                const result = await res.json();
                if (result.success) {
                    appendMsg('bot', result.reply);
                    chatHistory.push({ sender: 'user', text: message });
                    chatHistory.push({ sender: 'bot', text: result.reply });
                } else {
                    appendMsg('bot', 'Sorry, I encountered an issue processing that.');
                }
            } catch (err) {
                appendMsg('bot', 'Network error. Please try again.');
            }
        }

        function appendMsg(sender, text) {
            const box = document.getElementById('chat-box');
            const msg = document.createElement('div');
            msg.className = `msg ${sender}`;
            msg.innerText = text;
            box.appendChild(msg);
            box.scrollTop = box.scrollHeight;
        }

        // Load Streak on Start
        document.getElementById('streak-count').innerText = localStorage.getItem('fit_streak') || '1';
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

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
