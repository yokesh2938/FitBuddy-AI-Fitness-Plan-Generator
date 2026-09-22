# Phase 3: Project Design Phase

## 1. System Architecture Diagram

The Fit Buddy system follows a standard three-tier architecture: Presentation Layer (Client UI), Application/Logic Layer (Flask/Node Backend + Gemini Integration), and Data Layer (Database).

```mermaid
graph TD
    %% User Tier
    subgraph Client Tier [Presentation Layer]
        UI[User Interface - Web/Mobile]
    end

    %% Backend Tier
    subgraph Server Tier [Application Layer]
        API[Backend API Gateway - Flask/Node.js]
        Auth[Auth & Session Manager]
        PromptEng[Prompt Engineering Engine]
    end

    %% External Services & Database
    subgraph Services & Storage [Data & AI Layer]
        Gemini[Google Gemini API]
        DB[(Database - User Data & Logs)]
    end

    %% Connections
    UI <-->|HTTP/HTTPS Requests| API
    API <--> Auth
    API <--> DB
    API -->|Formatted Prompt + Context| PromptEng
    PromptEng -->|API Request| Gemini
    Gemini -->|Structured JSON Response| PromptEng
    PromptEng -->|Processed Data| API
flowchart TD
    A([User Opens Fit Buddy App]) --> B{User Logged In?}
    B -- No --> C[Register / Login]
    C --> D[Input Profile & Goals]
    D --> E[Save Profile to Database]
    B -- Yes --> F[Dashboard]
    E --> F

    F --> G{Choose Action}
    
    %% Branch 1: Request Routine
    G -->|Generate Workout| H[Select Workout Duration, Focus & Equipment]
    H --> I[Backend Builds System Prompt + User Context]
    I --> J[Send Request to Gemini API]
    J --> K[Gemini Returns Structured Routine]
    K --> L[Render Workout Cards on Screen]
    L --> M[User Completes & Logs Workout]
    M --> N[(Save Log to Database)]

    %% Branch 2: Chat Assistant
    G -->|Chat with Buddy| O[Open Interactive Chat UI]
    O --> P[User Sends Fitness / Diet Query]
    P --> Q[Backend Appends History + System Prompt]
    Q --> R[Send Chat Context to Gemini API]
    R --> S[Gemini Responds with Advice]
    S --> O
+-------------------------------------------------------------+
| FIT BUDDY                                    [Logout / Help]|
+-------------------------------------------------------------+
|                                                             |
|  Welcome! Let's set up your profile.                        |
|                                                             |
|  Fitness Goal:                                              |
|  [ (o) Build Muscle   ( ) Fat Loss   ( ) General Health ]   |
|                                                             |
|  Experience Level:                                          |
|  [ (o) Beginner   ( ) Intermediate   ( ) Advanced ]         |
|                                                             |
|  Available Equipment:                                       |
|  [ [x] Dumbbells   [x] Resistance Bands   [ ] Full Gym ]    |
|                                                             |
|  Dietary Restrictions (Optional):                           |
|  [ e.g., Vegetarian, High Protein, Peanut Allergy       ]   |
|                                                             |
|                    [ SAVE PROFILE & CONTINUE ]              |
+-------------------------------------------------------------+
+-------------------------------------------------------------+
| FIT BUDDY - AI COACH                                   [X]  |
+-------------------------------------------------------------+
| [Buddy]: Hi Alex! How can I help with your training today?  |
|                                                             |
| [User]: My lower back hurts a bit. Can I swap push-ups?     |
|                                                             |
| [Buddy]: Absolutely! To protect your lower back while still |
|          targeting your chest, try Seated Dumbbell Press or |
|          Chest Dips with bodyweight.                        |
|                                                             |
| Quick Prompts:                                              |
| [ "High-protein snack ideas?" ] [ "How to warm up shoulders?" ]|
|                                                             |
| +---------------------------------------------------------+ |
| | Type your fitness question here...               [SEND] | |
| +---------------------------------------------------------+ |
+-------------------------------------------------------------+
