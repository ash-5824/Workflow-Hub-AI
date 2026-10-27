import sqlite3
from dataclasses import dataclass

@dataclass
class Workflow:
    id: int
    workflow_name: str
    trigger_route: str
    ai_model: str
    ai_prompt: str
    action_url: str

def init_db():
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workflows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workflow_name TEXT NOT NULL,
            trigger_route TEXT NOT NULL,
            ai_model TEXT NOT NULL,
            ai_prompt TEXT NOT NULL,
            action_url TEXT NOT NULL
        )
    ''')
    
    # Check if empty, then insert multiple distinct workflows
    cursor.execute('SELECT COUNT(*) FROM workflows')
    if cursor.fetchone()[0] == 0:
        sample_workflows = [
            (
                "Gemma Summarizer", 
                "summarize-route", 
                "gemma2:2b", 
                "Summarize this payload into a short, engaging Discord announcement.", 
                "https://discord.com/api/webhooks/1564587258550681690/a6LGFPhUqCga1UfOu0tw6rw-waTANamNMPIUL1uxW-KhrMwPHE8HchIyWOfs4mne5SOx"
            ),
            (
                "Phi-4 Data Extractor", 
                "extract-route", 
                "phi4-mini", 
                "Extract the name, requested team, and urgency from this payload. Output only as strict JSON.", 
                "display_action"
            ),
            (
                "Nemotron Triage", 
                "triage-route", 
                "nemotron-mini", 
                "Analyze this payload. Is it a Complaint, a Question, or a Registration? Reply with exactly one word.", 
                "display_action"
            ),
            (
                "Qwen Code Generator", 
                "code-route", 
                "qwen2.5-coder:3b", 
                "You are an expert developer. Read this payload, identify the coding task requested, and write the Python script to solve it. Output ONLY the code inside Markdown blocks.", 
                "display_action"
            ),
            (
                "WhatsApp Email Summarizer", 
                "whatsapp-route", 
                "gemini-3.6-flash", 
                "Summarize this email payload into a short, punchy 2-sentence summary suitable for a WhatsApp alert.", 
                "whatsapp_action"
            ),
            (
                "AI Calendar Scheduler", 
                "calendar-route", 
                "gemini-3.6-flash", 
                "Extract the event name, date, and time from this email payload. Output ONLY a raw Google Calendar template URL format like this: https://calendar.google.com/calendar/render?action=TEMPLATE&text=[Event_Name]&dates=[YYYYMMDDTHHMMSSZ]/[YYYYMMDDTHHMMSSZ]&details=[Description]", 
                "calendar_action"
            )
        
        ]
        
        cursor.executemany('''
            INSERT INTO workflows (workflow_name, trigger_route, ai_model, ai_prompt, action_url)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_workflows)
        
    conn.commit()
    conn.close()

def get_workflow(trigger_route: str) -> Workflow | None:
    conn = sqlite3.connect('workflow.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workflows WHERE trigger_route = ?', (trigger_route,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Workflow(*row)
    return None
