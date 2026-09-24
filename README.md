Fit Buddy 2.0 🏋️‍♂️🤖
Fit Buddy 2.0 is an AI-powered fitness assistant and workout protocol generator built with Flask, Google Gemini 2.5 Flash API, SQLite, Chart.js, and html2pdf.js. It features structured routine generation, an interactive AI coach chatbot, performance analytics, and dynamic PDF export capabilities.
🛠️ Tech Stack & Features
 * Backend: Flask (Python)
 * AI Integration: Google GenAI SDK (google-genai) with Gemini 2.5 Flash
 * Database: SQLite (fitbuddy_pro.db)
 * Frontend: Glassmorphic Responsive Dashboard, Chart.js (Analytics), html2pdf.js (PDF Export)
 * Testing: Pytest & Flask Test Client
📁 Project Structure
fit-buddy-2.0/
├── app.py              # Main Flask application controller & API routes
├── test_app.py         # Automated test suite (Pytest)
├── design.md           # System design, architecture & schema docs
├── testing.md          # Testing strategy & manual QA matrix
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (API Keys)
├── fitbuddy_pro.db     # SQLite database (auto-generated)
├── static/             # CSS, JS, and UI assets
└── templates/
    └── index.html      # Main dashboard interface

⚙️ Environment & Setup Instructions
1. Prerequisites
Ensure you have the following installed on your system:
 * Python 3.10+
 * pip (Python package installer)
 * Google Gemini API Key (Obtainable from Google AI Studio)
2. Clone Repository & Setup Virtual Environment
# Clone the project repository
git clone https://github.com/your-username/fit-buddy-2.0.git
cd fit-buddy-2.0

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
Create or update your requirements.txt file with the following dependencies:
flask
python-dotenv
google-genai
pytest
pytest-flask

Install them running:
pip install -r requirements.txt

4. Configure Environment Variables (.env)
Create a .env file in the root directory of your project and add your Gemini API key:
GEMINI_API_KEY=your_google_gemini_api_key_here
FLASK_ENV=development
FLASK_APP=app.py

> Note: Make sure .env is added to your .gitignore so your API key is kept secure.
> 
🏃 Running the Application
1. Start Flask Server
Run the Flask server:
python app.py

The database fitbuddy_pro.db will automatically initialize with the required tables (user_profile and workout_logs) and default seed data on the first run.
2. Access the Application
Open your browser and navigate to:
http://127.0.0.1:5000

🧪 Running Automated Tests
To run the full test suite (database schema checks, API route tests, and Gemini structure validations):
pytest test_app.py -v

🛰️ REST API Documentation
| Endpoint | Method | Description |
|---|---|---|
| / | GET | Loads main dashboard UI |
| /api/profile | GET | Fetches active user profile & streak count |
| /api/workout | POST | Calls Gemini API to generate structured workout routines |
| /api/chat | POST | AI Coach conversational query handler |
| /api/log-workout | POST | Logs finished workouts to SQLite database and increments streak |
