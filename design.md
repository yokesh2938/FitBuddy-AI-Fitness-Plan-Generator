# Fit Buddy Pro — Project Design Phase (design.md)

## 1. System Architecture Diagram

```mermaid
graph TD
    %% Client Layer
    subgraph Client ["Client Browser Layer"]
        UI["Modern Glassmorphic UI"]
        Chart["Chart.js Analytics"]
        PDF["html2pdf.js Export"]
    end

    %% API Layer
    API["HTTP REST API (JSON)"]

    %% Backend Layer
    subgraph Backend ["Flask Backend Engine (app.py)"]
        Controller["App Controller & Routes"]
    end

    %% External & Storage
    Gemini["Google Gemini AI API (gemini-2.5-flash)"]
    DB[("SQLite Database (fitbuddy_pro.db)")]

    %% Connections
    UI <--> API
    API <--> Controller
    Controller <--> Gemini
    Controller <--> DB
flowchart TD
    A[User Opens App] --> B[Load Dashboard & Sync Local DB]
    
    %% Branch 1: Routine Generation
    B --> C[Select Goal & Equipment]
    C --> D[POST /api/workout]
    D --> E[Gemini API: Structured Schema]
    E --> F[Render Plan Cards]
    F --> G[Export Plan to PDF]

    %% Branch 2: AI Coach
    B --> H[Ask AI Coach Query]
    H --> I[POST /api/chat]
    I --> J[Gemini API: Natural Response]
    J --> K[Update Chat Window]

    %% Branch 3: Performance Tracking
    B --> L[View Calendar & Stats]
    L --> M[Query SQLite DB]
    M --> N[Update Chart.js Analytics]
graph TD
    subgraph Dashboard ["Main Application Dashboard Layout"]
        Header["Top Navigation Bar<br>• Logo & Branding<br>• Streak Counter (Days)<br>• Profile & Dark/Light Theme Toggle"]
        
        subgraph MainContent ["2-Column Responsive Layout"]
            subgraph LeftCol ["Left Column"]
                Calendar["Interactive Weekly Schedule Strip"]
                Generator["AI Workout Routine Generator Form"]
                Results["Generated Exercise Cards & PDF Export"]
            end
            
            subgraph RightCol ["Right Column"]
                Analytics["Performance Analytics Chart (Chart.js)"]
                Chat["Interactive AI Coach Assistant Interface"]
            end
        end
    end

    Header --> MainContent
