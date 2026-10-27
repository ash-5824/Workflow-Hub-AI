# Workflow-Hub-AI
Hybrid Edge-Cloud AI Workflow Orchestration Engine

Architecture •
Neural Routing Matrix •
Quickstart •
Live Demo Payloads •
Directory Structure

📖 Overview

Modern operational workflows face a critical trade-off: data privacy and zero-latency execution versus high-reasoning cloud intelligence.

Workflow Hub solves this through a dual-tier orchestration engine:

Local Edge Tier: Utilizes local Ollama nodes (phi4-mini, nemotron-mini, qwen2.5-coder, gemma2:2b) for air-gapped tasks—such as sensitive intent classification, JSON extraction, and script generation—with zero API costs and full data sovereignty.

Hyperscale Cloud Tier: Employs Google Gemini 3.6 Flash to perform high-context semantic distillation, unstructured thread synthesis, dynamic Google Calendar web URL generation, and Twilio WhatsApp dispatching

🚦 Neural Routing Matrix
Route EndpointEngineModelAction TargetDescription/webhook/summarize-routeOllama gemma2:2b Discord Webhook Generates structured Discord updates with automated thread detection./webhook/extract-routeOllama phi4-miniDashboard UIZero-leakage extraction of entities into strict, validated JSON./webhook/triage-routeOllamanemotron-miniDashboard UIReal-time classification: Complaint, Question, or Registration./webhook/code-routeOllamaqwen2.5-coder:3bDashboard UIInterprets requirements and writes executable code blocks./webhook/whatsapp-routeGemini Cloudgemini-3.6-flashTwilio WhatsAppDistills dense logs into high-priority WhatsApp alerts with live terminal fallback./webhook/calendar-routeGemini Cloudgemini-3.6-flashInteractive UIExtracts event schedules and creates a direct Google Calendar template URL.
⚡Quickstart Guide1. Repository Setup# Clone the repository
git clone https://github.com/your-username/workflow-hub.git
cd workflow-hub

# Create a clean virtual environment
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate
2. Install Dependenciespip install fastapi uvicorn httpx python-dotenv google-genai twilio
3. Local Model Provisioning (Ollama)Ensure Ollama is running in the background, then pull the local models:ollama pull gemma2:2b
ollama pull nemotron-mini
ollama pull qwen2.5-coder:3b
ollama pull phi4-mini
4. Configure Environment VariablesCreate a .env file in the project root:# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Twilio Credentials (Optional - terminal sandbox fallback included)
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_auth_token
5. Launch the Serverpython -m uvicorn main:app --reload
Navigate to http://localhost:8000 in your browser. The frontend is served directly by the FastAPI backend to eliminate CORS issues and ERR_FILE_NOT_FOUND errors.

🧪 Live Demo PayloadsCopy and paste these snippets directly into the Raw Payload Data box on the dashboard:1. Discord Webhook & Dynamic Threading (/summarize-route)[Discord Channel: #dev-ops-announcements]
[Thread: Hacktoberfest-Release-Sync-104]

1.CRITICAL DEPLOYMENT SYNC: Pull Request #104 'Offline Ollama Model Switching & Vector Caching' was successfully merged into the main branch by lead maintainer rahul rastogi. Automated test suite reports all 42 FastAPI integration checks passed with 0 memory leaks.

2. Google Calendar Action Synthesis (/calendar-route)Reminder: The Autonomous Navigation Code Freeze and Hardware Requisition Window closes on October 28, 2026, starting at 4:30 PM until 6:00 PM in CS Lab Block B, Room 204.
   
3. Zero-Shot Intent Classification (/triage-route)Hello team, I submitted my paperwork three days ago for the autonomous robotics cohort but have not received any confirmation email or portal credentials yet. Could you check if my registration went through, or if there is an issue with my submission?
   
5. Code Generation (/code-route)Write a Python script that takes two arrays of equal length and adds them together element-wise. Provide a short test case printing the result.
   
7. Structured Data Extraction (/extract-route)URGENT REQUEST:
Hi administration, my name is Priya Sharma. I need an immediate reassignment to the Autonomous Vehicle Computer Vision sub-team before the project milestone lock at midnight. Please expedite this update as soon as possible.

📁 Repository Layout├── main.py              # FastAPI gateway, dashboard server, and dynamic action dispatcher
├── ai_processing.py     # Hybrid inference engine (Gemini SDK + Ollama HTTP), regex parsers
├── database.py          # SQLite schema creation and pre-configured default routes
├── index.html           # Dark-mode Tailwind CSS interface and execution log terminal
├── .env                 # Environment variables for Gemini and Twilio keys
├── requirements.txt     # Python library dependencies
└── README.md            # Technical documentation

🛡 Fault Tolerance & Safety FeaturesTwilio Sandbox Fallback: If Twilio's WhatsApp 24-hour sandbox template window has expired during a live demonstration, the backend automatically intercepts the error and outputs a formatted ASCII delivery box in the terminal while returning an HTTP 200 to keep the UI green.Smart Calendar Regex: Captures URLs inside generated Markdown output, scrubs duplicate query parameters, and renders a native browser action button without page refreshes.Auto-Tag Cleaning: Cleans control brackets ([Thread: ...]) from outgoing Discord webhooks so messages arrive looking pristine and human-authored.

📄 License
Distributed under the MIT License.
