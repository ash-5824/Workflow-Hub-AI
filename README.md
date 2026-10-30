# Workflow-Hub-AI
**A simple, hybrid AI engine that combines local and cloud AI models to automate workflows.**

---

## 📖 Overview

Most AI applications face a choice:
* **Local AI:** Private and free, but has limited reasoning capabilities.
* **Cloud AI:** Very smart and powerful, but costs money and requires sending data to external servers.

**Workflow Hub** combines both:
1. **Local Edge AI (Ollama):** Handles quick, sensitive, or basic tasks (like sorting messages, extracting simple data, or writing code) right on your computer. It is completely free and private.
2. **Cloud AI (Google Gemini):** Handles complex tasks (like summarizing long logs, generating calendar links, or sending WhatsApp alerts) where higher intelligence is required.

---

## 🚦 How Tasks Are Routed

| Webhook Route | AI Engine | Model Used | Destination | What It Does |
| :---          | :--- | :--- | :--- | :--- |
| `/webhook/summarize-route` | Ollama | `gemma2:2b` | Discord Webhook | Creates structured summaries for Discord messages. |
| `/webhook/extract-route` | Ollama | `phi4-mini` | Dashboard UI | Pulls specific details out of text into JSON format without sharing data online. |
| `/webhook/triage-route` | Ollama | `nemotron-mini` | Dashboard UI | Sorts incoming messages into categories (e.g., Complaint, Question, Registration). |
| `/webhook/code-route` | Ollama | `qwen2.5-coder:3b` | Dashboard UI | Turns plain language requirements into runnable code. |
| `/webhook/whatsapp-route` | Cloud | `gemini-3.6-flash` | WhatsApp (Twilio) | Summarizes long logs and sends high-priority alerts to WhatsApp. |
| `/webhook/calendar-route` | Cloud | `gemini-3.6-flash` | Interactive UI | Reads event details from text and generates a clickable Google Calendar link. |

---

## ⚡ Quickstart Guide

### 1. Set Up the Project
Clone the repository and set up a Python virtual environment:

```bash
# Clone the repository
git clone https://github.com/your-username/workflow-hub.git
cd workflow-hub

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate
```

### 2. Install Required Packages
```bash
pip install fastapi uvicorn httpx python-dotenv google-genai twilio
```

### 3. Download Local AI Models (Ollama)
Make sure [Ollama](https://ollama.com/) is installed and running, then pull the required models:
```bash
ollama pull gemma2:2b
ollama pull nemotron-mini
ollama pull qwen2.5-coder:3b
ollama pull phi4-mini
```

### 4. Configure Environment Variables
Create a file named `.env` in the root folder of the project:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Twilio Credentials (Optional - fallback mode available if missing)
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_auth_token
```

### 5. Start the Server
Run the web server:
```bash
python -m uvicorn main:app --reload
```

Open `http://localhost:8000` in your browser to access the dashboard.

---

## 🧪 Example Test Inputs

You can copy and paste these sample inputs directly into the **Raw Payload Data** field on the dashboard:

<details>
<summary><b>1. Discord Webhook Summary (`/summarize-route`)</b></summary>

```text
[Discord Channel: #dev-ops-announcements]
[Thread: Release-Sync-104]

1. DEPLOYMENT UPDATE: Pull Request #104 'Offline Ollama Model Switching' was merged into main by Rahul. All 42 automated tests passed with zero errors.
```
</details>

<details>
<summary><b>2. Google Calendar Link Generation (`/calendar-route`)</b></summary>

```text
Reminder: The Navigation Code Review and Hardware Check closes on October 28, 2026, from 4:30 PM to 6:00 PM in CS Lab Block B, Room 204.
```
</details>

<details>
<summary><b>3. Message Classification (`/triage-route`)</b></summary>

```text
Hello team, I submitted my paperwork three days ago for the robotics workshop but haven't received a confirmation email yet. Could you check if my registration went through?
```
</details>

<details>
<summary><b>4. Code Generation (`/code-route`)</b></summary>

```text
Write a Python function that takes two lists of equal length and adds them together element by element. Include a brief test case showing the output.
```
</details>

<details>
<summary><b>5. Structured Data Extraction (`/extract-route`)</b></summary>

```text
URGENT REQUEST:
Hi, my name is Priya Sharma. I need to be moved to the Autonomous Vehicle Computer Vision team before midnight tonight. Please update my record.
```
</details>

---

## 📁 File Structure

```text
├── main.py              # Main API server and dashboard handler
├── ai_processing.py     # Logic for routing requests to Gemini and Ollama
├── database.py          # SQLite database setup and route configs
├── index.html           # Web dashboard interface
├── .env                 # API keys and secret config
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🛡️ Key Features & Safeguards

* **Twilio Terminal Fallback:** If Twilio is not set up or fails, the message will print directly in your server terminal as a preview box without breaking the app.
* **Automatic Calendar Link Formatting:** Automatically extracts dates and times to create clean Google Calendar event URLs.
* **Message Cleaning:** Cleans up internal tag metadata (e.g., `[Thread: ...]`) before sending output to webhooks like Discord.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
