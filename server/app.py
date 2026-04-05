from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from typing import Optional, Dict, Any
import uvicorn
import os
import sys

# Ensure current directory is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "email_triage_env"))

from env import EmailTriageEnv
from models import Action, Observation, Reward, State
from tasks import TASKS

app = FastAPI(title="Email Triage OpenEnv")
env = EmailTriageEnv()

@app.get("/", response_class=HTMLResponse)
async def root():
    state = env.state()
    emails_html = ""
    if state:
        for email in state.all_emails:
            status = "Archived" if email.is_archived else "Active"
            emails_html += f"""
            <div style='border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;'>
                <strong>From:</strong> {email.sender} <br>
                <strong>Subject:</strong> {email.subject} <br>
                <strong>Status:</strong> {status} <br>
                <p>{email.body}</p>
            </div>
            """
    else:
        emails_html = "<p>Environment not reset yet. Call /reset to start.</p>"

    return f"""
    <html>
        <head>
            <title>Email Triage OpenEnv</title>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6; color: #333; }}
                h1 {{ color: #2563eb; }}
                .container {{ background: #f9fafb; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            <div class='container'>
                <h1> Email Triage OpenEnv</h1>
                <p>Status: <strong>Running</strong></p>
                <hr>
                <h2>Current Inbox State</h2>
                {emails_html}
                <hr>
                <p><small>This is an OpenEnv server. Use the <code>/step</code> and <code>/reset</code> endpoints for programmatic interaction.</small></p>
            </div>
        </body>
    </html>
    """

@app.post("/reset", response_model=Observation)
async def reset(task_id: str = Body("easy", embed=True)):
    try:
        return env.reset(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
async def step(action: Action):
    try:
        observation, reward, done, info = env.step(action)
        return {
            "observation": observation,
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
async def state():
    try:
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
async def get_tasks():
    return {
        "tasks": [
            {"id": task.id, "description": task.description, "difficulty": task.difficulty}
            for task in TASKS.values()
        ]
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
