# Fit Buddy Pro — Requirement Analysis Phase (requirements.md)

## 1. Functional Requirements (FR)

### FR-1: Dynamic AI Workout Generator
* **FR-1.1:** The system shall accept user inputs for target goal, muscle group, equipment availability, and target duration.
* **FR-1.2:** The system shall send structured prompt requests to the Google Gemini API using strictly typed JSON schema validation.
* **FR-1.3:** The system shall render structured workout plans detailing exercise names, set counts, repetition ranges, and rest intervals.

### FR-2: Interactive Rest Timer
* **FR-2.1:** The system shall parse rest interval durations from workout plans and auto-configure a digital rest timer.
* **FR-2.2:** The system shall allow users to play, pause, and reset the countdown timer.

### FR-3: Performance Analytics & Weekly Calendar
* **FR-3.1:** The system shall display an interactive 7-day weekly schedule strip indicating completed and upcoming workout sessions.
* **FR-3.2:** The system shall visualize weekly training volume, streak counters, and performance stats using Chart.js.

### FR-4: AI Coach Assistant (Chatbot)
* **FR-4.1:** The system shall provide an inline chat interface for users to ask fitness, form execution, and nutrition queries.
* **FR-4.2:** The assistant shall maintain context across messages and deliver actionable coaching guidance.

### FR-5: Profile Management & PDF Export
* **FR-5.1:** The system shall allow users to update demographic data (e.g., name, age, weight, height) and store them locally.
* **FR-5.2:** The system shall generate and download professional, print-ready PDF files of workout protocols using client-side rendering (`html2pdf.js`).

---

## 2. Non-Functional Requirements (NFR)

### NFR-1: Performance & Response Time
* The UI shall render workout routines within **3 seconds** of API response receipt.
* Local UI interactions (theme toggle, timer start/stop, calendar filtering) shall execute in under **100ms**.

### NFR-2: Usability & Accessibility
* The application shall feature a responsive design optimized for desktop, tablet, and mobile screens.
* The application shall support high-contrast Dark Mode and Light Mode themes.

### NFR-3: Reliability & Data Persistence
* User profile records and workout session history shall persist reliably in a local SQLite database (`fitbuddy_pro.db`).
* Client-side localStorage shall serve as a fallback state sync for active session timers and streak counters.

---

## 3. Technical Stack

* **Backend Framework:** Python 3.10+ / Flask Web Framework
* **Artificial Intelligence Engine:** Google Gemini API (`gemini-2.5-flash`) via `google-genai` SDK
* **Database:** SQLite3
* **Frontend Technologies:** HTML5, CSS3 (Modern Glassmorphism Design System), JavaScript (ES6+)
* **Visualization & Utilities:** Chart.js (Data Analytics), Font Awesome 6 (Iconography), `html2pdf.js` (Client-side PDF Export)

---

## 4. Hardware & Software Requirements

### Software Requirements
* **Operating System:** Windows 10/11, macOS, or Linux (Ubuntu 20.04+)
* **Runtime Environment:** Python 3.10 or higher
* **Web Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari (modern browser with ES6 capability)
* **Package Dependencies:** `flask`, `python-dotenv`, `google-genai`

### Hardware Requirements
* **Processor:** Dual-core 2.0 GHz or higher (Intel/AMD/Apple Silicon)
* **RAM:** Minimum 4 GB (8 GB recommended)
* **Storage:** Minimum 500 MB free space for code repository, dependencies, and SQLite database
* **Network:** Active internet connection required for Google Gemini API model calls
