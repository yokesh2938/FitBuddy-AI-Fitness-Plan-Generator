# Fit Buddy Pro — System Design & Architecture (`design.md`)

## 1. High-Level System Architecture


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

## 2. Component Workflow & Data Flow


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

## 3. Executive Interface Blueprint


+---------------------------------------------------------------------------------+
|  [LOGO] Fit Buddy Pro                       [🔥 3 Days Streak]  [PROFILE] [DARK] |
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

## 4. Database Schema Specification

### Entity 1: `user_profile`

| Column Name | Data Type | Key Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`id`** | INTEGER | PRIMARY KEY | NO | Unique record identifier |
| **`name`** | TEXT | - | NO | User's full name |
| **`age`** | INTEGER | - | YES | Age in years |
| **`weight`** | REAL | - | YES | Body weight in kilograms |
| **`height`** | REAL | - | YES | Height in centimeters |
| **`fitness_goal`**| TEXT | - | YES | Primary fitness objective |
| **`level`** | TEXT | - | YES | Experience level |
| **`streak_count`**| INTEGER | - | NO | Current active daily streak |
| **`last_workout`**| TEXT | - | YES | ISO timestamp of last workout |

### Entity 2: `workout_logs`

| Column Name | Data Type | Key Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`id`** | INTEGER | PRIMARY KEY | NO | Auto-incrementing log ID |
| **`title`** | TEXT | - | NO | Name of generated protocol |
| **`category`** | TEXT | - | YES | Target muscle group/category |
| **`completed_date`**| TEXT | - | YES | Timestamp of session completion |
| **`duration_min`**| INTEGER | - | YES | Active workout duration |
| **`calories_burned`**| INTEGER | - | YES | Estimated energy burned |

