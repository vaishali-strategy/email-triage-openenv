import os
import json
from openai import OpenAI
from email_triage_env.env import EmailTriageEnv # Adjust this import if your env class is located elsewhere
from email_triage_env.models import Action

# --- 1. MANDATORY ENVIRONMENT VARIABLES ---
# The grader parses these exact lines using regex. Do not change the variable names.
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
HF_TOKEN = os.getenv("HF_TOKEN")

# Optional - if you use from_docker_image():
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# --- 2. CONFIGURE CLIENT ---
# The platform requires the client to use the API_BASE_URL variable
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN or os.getenv("OPENAI_API_KEY", "dummy-key")
)

def run_baseline():
    env = EmailTriageEnv()
    
    for task_idx in range(len(env.tasks)):
        # --- REQUIRED LOG: START ---
        print("START") 
        
        obs = env.reset(task_idx)
        done = False
        
        messages = [
            {"role": "system", "content": "You are a customer support agent. Goal: " + env.tasks[task_idx]['goal']},
            {"role": "user", "content": f"Initial state: {obs.model_dump_json()}"}
        ]

        while not done:
            # --- REQUIRED LOG: STEP ---
            print("STEP")
            
            response = client.chat.completions.create(
                model=MODEL_NAME, # MUST use the variable, not a hardcoded string
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "take_action",
                        "description": "Perform an action on an email.",
                        "parameters": Action.model_json_schema()
                    }
                }],
                tool_choice={"type": "function", "function": {"name": "take_action"}}
            )
            
            tool_call = response.choices[0].message.tool_calls[0]
            action_args = json.loads(tool_call.function.arguments)
            action = Action(**action_args)
            
            obs, reward, done, info = env.step(action)
            messages.append({"role": "assistant", "tool_calls": [tool_call]})
            messages.append({
                "role": "tool", 
                "tool_call_id": tool_call.id, 
                "name": "take_action", 
                "content": f"Observation: {obs.model_dump_json()} | Reward: {reward.value} | Done: {done}"
            })
            
            # Failsafe to prevent infinite loops locally
            if env.state_data["steps"] >= 10:
                break
                
        # --- REQUIRED LOG: END ---
        print("END")

if __name__ == "__main__":
    run_baseline()