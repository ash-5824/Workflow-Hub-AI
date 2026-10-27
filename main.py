import os
from dotenv import load_dotenv

load_dotenv() # This loads the keys from your .env file
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_workflow
from ai_processing import process_text, send_to_action_url, send_whatsapp_alert

# Import Twilio for the SMS routing
from twilio.rest import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the SQLite database on startup
init_db()

# --- TWILIO SETUP ---
TWILIO_SID = os.environ.get("TWILIO_SID", "Enter your TWILIO_SID HERE")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN", "Enter your TWILIO_TOKEN HERE")
TWILIO_PHONE = "+1234567890"  # Your Twilio Sandbox Number
YOUR_PHONE = "+919690662431"  # Your Verified Personal Phone Number

async def send_sms_alert(summary_text: str):
    """Helper function to send SMS using Twilio"""
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=f"⚡ Hub Alert:\n{summary_text}",
            from_=TWILIO_PHONE,
            to=YOUR_PHONE
        )
        return 200 # Success HTTP status code
    except Exception as e:
        print(f"Twilio Error: {e}")
        return 500

@app.on_event("startup")
async def startup():
    pass

# --- DASHBOARD UI SERVING ROUTE ---
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """
    Serves index.html directly from the backend root directory.
    """
    index_path = "index.html"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Workflow Hub backend is running, but index.html was not found in the project root directory.</h3>"

@app.post("/webhook/{trigger_route}")
async def webhook(trigger_route: str, request: Request):
    # Query the database for the workflow matching the trigger_route
    workflow = get_workflow(trigger_route)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Robustly extract the text string from whatever key the frontend sends
    try:
        body = await request.json()
        if isinstance(body, dict):
            incoming_text = (
                body.get("payload") or 
                body.get("text") or 
                body.get("message") or 
                body.get("input") or 
                str(body)
            )
        else:
            incoming_text = str(body)
    except Exception:
        incoming_text = "GDG Hacktoberfest workshop update: Session moved to Lab Block B Room 204, starting at 9:00 AM."

    # Final safety fallback if the input box was completely empty
    if not incoming_text or not incoming_text.strip():
        incoming_text = "GDG Hacktoberfest workshop update: Session moved to Lab Block B Room 204, starting at 9:00 AM."

    # Process the clean text string using your AI logic
    processed_text = await process_text(incoming_text, workflow.ai_model, workflow.ai_prompt)

    # -----------------------------------------
    # 🔀 DYNAMIC ACTION ROUTER
    # -----------------------------------------
    status_code = 200
    
    if workflow.action_url in ["calendar_action", "email_action", "display_action"]:
        # UI-rendered actions: Passed directly back in JSON response to display on the webpage
        status_code = 200
        
    elif workflow.action_url == "whatsapp_action":
        # Route to Twilio WhatsApp
        status_code = await send_whatsapp_alert(processed_text)
        
    else:
        # Default Route: Send to Discord / Standard Webhook
        response = await send_to_action_url(processed_text, workflow.action_url)
        status_code = response.status_code

    # Return a JSON success response to the dashboard
    return JSONResponse(
        content={
            "generated_text": processed_text,
            "executor_status_code": status_code
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
