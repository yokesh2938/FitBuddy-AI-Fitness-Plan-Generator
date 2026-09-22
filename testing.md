# Phase 6: Project Testing Phase

## 1. Test Cases & Results

| Test ID | Module | Scenario / Input Description | Expected Outcome | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Workout Generator | User submits form with valid inputs (Goal: Fat Loss, Level: Beginner, Time: 30m, Equip: Bodyweight). | Backend calls Gemini API and returns a structured JSON object containing workout title, exercise array, and safety disclaimer. | Structured JSON returned and rendered dynamically into clean exercise cards. | **PASS** |
| **TC-02** | Workout Generator | User submits empty/missing form fields. | Frontend uses fallback defaults or browser validation to prevent broken API requests. | Default values applied; valid API call sent without server errors. | **PASS** |
| **TC-03** | Interactive Chat | User asks a standard fitness query (e.g., "What are good warm-up drills?"). | Gemini processes chat history and returns a relevant, concise response in under 3 seconds. | Response received in 1.8s and displayed in chat bubble format. | **PASS** |
| **TC-04** | Interactive Chat | User inquires about medical advice (e.g., "I have sharp knee pain while squatting"). | System prompt triggers medical safety disclaimer advising consultation with a physician. | Fit Buddy provided alternate exercise options and explicitly advised consulting a medical professional. | **PASS** |
| **TC-05** | Backend / API | User sends rapid consecutive requests (Rate Limiting). | API handles concurrency without crashing or hanging client-side UI. | Server returns requests successfully or handles queue without dropping connection. | **PASS** |
| **TC-06** | Configuration | Launch application without `GEMINI_API_KEY` set in `.env`. | Backend throws a clear, handled error during initialization. | Server raised `ValueError: GEMINI_API_KEY environment variable is missing` and halted cleanly. | **PASS** |

---

## 2. Output Screenshots & UI Proofs

### Screenshot 1: Workout Generation Dashboard
```text
+-----------------------------------------------------------------------+
| 🏋️‍♂️ Fit Buddy - AI Workout Coach                                      |
+-----------------------------------------------------------------------+
| Generate Your Workout                  YOUR CUSTOM ROUTINE            |
| Goal: [ Muscle Building v ]           Full-Body Dumbbell Strength     |
| Level: [ Beginner v ]                 ------------------------------  |
| Equip: [ Dumbbells Only v ]           1. Dumbbell Goblet Squat        |
| Time: [ 30 Minutes v ]                   Sets: 3 | Reps: 10-12 | Rest: 60s  |
|                                       2. Dumbbell Floor Press         |
| [ GENERATE ROUTINE ]                     Sets: 3 | Reps: 10 | Rest: 60s     |
|                                       ------------------------------  |
|                                       * Disclaimer: Consult a doctor  |
|                                         before starting new exercises.|
+-----------------------------------------------------------------------+
+-----------------------------------------------------------------------+
| Chat with Fit Buddy                                                   |
+-----------------------------------------------------------------------+
| [Bot]: Hi! I'm Fit Buddy. How can I help you reach your goals today?  |
| [User]: Can you give me a high-protein vegetarian post-workout snack? |
| [Bot]: Sure! Here are 2 great options:                                |
|        1. Greek Yogurt Parfait with chia seeds, almonds, and honey.   |
|        2. Cottage cheese toast with sliced avocados & hemp seeds.     |
|                                                                       |
| [ Type your fitness question here...                       ] [ SEND ] |
+-----------------------------------------------------------------------+
