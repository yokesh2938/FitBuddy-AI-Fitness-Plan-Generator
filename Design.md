# Fit Buddy Pro — Project Design Phase (design.md)

## 1. System Architecture Diagram

+-----------------------------------------------------------------------+
|                            CLIENT BROWSER                             |
|                                                                       |
|  +--------------------+   +-------------------+   +----------------+  |
|  | Modern Responsive  |   | Chart.js Engine   |   | html2pdf.js    |  |
|  | Glassmorphic UI    |   | (Analytics Visual)|   | (Export Engine)|  |
|  +---------+----------+   +---------+---------+   +-------+--------+  |
+------------|------------------------|---------------------|-----------+
|                        |                     |
+------------------+-----+---------------------+
|
| HTTP REST API (JSON)
v
+-----------------------------------------------------------------------+
|                       FLASK BACKEND ENGINE                            |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  | App Controller (app.py)                                         |  |
|  | - / (Main View)                                                 |  |
|  | - /api/workout (JSON Protocol Generation)                       |  |
|  | - /api/chat (Interactive Coach Assistant)                       |  |
|  +------------------------------+----------------------------------+  |
|                                 |                                     |
+---------------------------------|-------------------------------------+
|
+------------------+------------------+
|                                     |
v                                     v
+------------------------------+     +------------------------------+
|     GOOGLE GEMINI AI API     |     |       SQLITE DATABASE        |
|                              |     |      (fitbuddy_pro.db)       |
| - Model: gemini-2.5-flash    |     |                              |
| - Schema Validation          |     | - user_profile               |
| - Structured JSON Outputs    |     | - workout_logs               |
+------------------------------+     +------------------------------+
## 2. System Flow Chart
+-----------------------+
|   User Opens System   |
+-----------+-----------+
|
v
+-----------------------+
| Load UI & Dashboard   |
| (Fetch DB & Local)    |
+-----------+-----------+
|
+-----------------------+-----------------------+
|                       |                       |
v                       v                       v
[ Generate Routine ]     [ Ask AI Coach ]       [ View Analytics ]
|                       |                       |
v                       v                       v
Select Target, Equipment    Type Query into Chat    Render Weekly Chart
& Session Parameters        Box & Submit Prompt      & Calendar Progress
|                       |                       |
v                       v                       v
POST /api/workout Request   POST /api/chat Request  Query Local DB & State
|                       |                       |
v                       v                       v
Call Gemini AI Model        Call Gemini AI Model    Display Stats/Streaks
(Structured JSON Schema)    (Natural Language)      in Dashboard Cards
|                       |                       |
v                       v                       v
Render Dynamic Plan Cards   Render Chat Response    Interactive View Sync
|                       |                       |
v                       |                       |
[ Export Plan to PDF ]              |                       |
(html2pdf Client Engine)            |                       |
|                       |                       |
+-----------------------+-----------------------+
|
v
+-----------------------+
| Session Logs & Local  |
| Database Sync         |
+-----------------------+
## 3. Low-Fidelity UI Wireframes

### Main Layout Architecture (Desktop & Mobile)
+-------------------------------------------------------------------------+
| [LOGO] Fit Buddy Pro              🔥 3 Days Streak  [PROFILE] [THEME]   |
+-------------------------------------------------------------------------+
|                                                                         |
|  +-----------------------------------+   +---------------------------+  |
|  | WEEKLY SCHEDULE                   |   | PERFORMANCE ANALYTICS     |  |
|  | [Sun] [Mon] [Tue] [Wed] [Thu] ... |   | +-----------------------+ |  |
|  +-----------------------------------+   | | Volume Line Chart     | |  |
|                                          | +-----------------------+ |  |
|  +-----------------------------------+   +---------------------------+  |
|  | WORKOUT GENERATOR                 |                              |
|  | Focus: [ Chest & Triceps      v ] |   +---------------------------+  |
|  | Equip: [ Dumbbells & Bench    v ] |   | AI COACH ASSISTANT        |  |
|  |                                   |   | +-----------------------+ |  |
|  | [ GENERATE AI ROUTINE BUTTON    ] |   | | Bot: How can I help?  | |  |
|  +-----------------------------------+   | | User: Form check?     | |  |
|                                          | +-----------------------+ |  |
|  +-----------------------------------+   | [Type message...] [SEND]  |  |
|  | GENERATED ROUTINE                 |   +---------------------------+  |
|  | Plan: Custom Protocol             |                              |
|  | [ EXPORT PDF BUTTON ]             |                              |
|  | +-------------------------------+ |                              |
|  | | [Dumbbell Press] 3 Sets 10 Reps| |                              |
|  | +-------------------------------+ |                              |
|  +-----------------------------------+                              |
+-------------------------------------------------------------------------+

---

## 4. Database Schema Design

### Table 1: `user_profile`
| Field Name | Data Type | Constraint | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | User unique identifier |
| `name` | TEXT | NOT NULL | Full name of the user |
| `age` | INTEGER | - | Age in years |
| `weight` | REAL | - | Weight in kilograms |
| `height` | REAL | - | Height in centimeters |
| `fitness_goal` | TEXT | - | Primary training objective |
| `level` | TEXT | - | Experience level |
| `streak_count` | INTEGER | DEFAULT 0 | Active daily workout streak |
| `last_workout_date` | TEXT | - | ISO timestamp of last activity |

### Table 2: `workout_logs`
| Field Name | Data Type | Constraint | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Log entry unique identifier |
| `title` | TEXT | NOT NULL | Workout protocol title |
| `category` | TEXT | - | Muscle group focus |
| `completed_date` | TEXT | - | Completion timestamp |
| `duration_minutes` | INTEGER | - | Active workout time |
| `calories_burned` | INTEGER | - | Estimated energy expenditure |