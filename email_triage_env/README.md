---
title: Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
tags:
- openenv
---

# Email Triage OpenEnv

A real-world email triage environment for AI agents, built with the OpenEnv specification.

## Environment Description and Motivation
The **Email Triage Environment** simulates the common task of managing an inbox. AI agents are tasked with reading, replying to, labeling, and archiving emails based on specific objectives. This task represents a significant real-world utility as email management is a core part of many administrative and support roles.

## Action and Observation Space

### Action Space
Agents can perform the following actions:
- `read(email_id)`: Read the details of a specific email.
- `archive(email_id)`: Move an email to the archive.
- `reply(email_id, content)`: Send a reply to an email.
- `label(email_id, label)`: Apply a label to an email.
- `delete(email_id)`: Delete an email.

### Observation Space
Agents receive:
- `emails`: A list of emails currently in the inbox.
- `current_email`: Details of the email currently being read.
- `last_action_status`: Success/Error message from the last action.
- `done`: Boolean indicating if the task is complete.

## Task Descriptions

| Task ID | Description | Difficulty |
|---------|-------------|------------|
| `easy`  | Archive the email from 'boss@company.com'. | Easy |
| `medium`| Reply to the support email with 'Issue resolved'. | Medium |
| `hard`  | Label all spam emails as 'Spam' and archive them. | Hard |

## Setup and Usage

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn server.app:app --reload
   ```

### Using Docker
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

## Baseline Scores
The following scores were achieved using the `baseline.py` script with `gpt-4o-mini`:

| Task | Score |
|------|-------|
| Easy | 1.0   |
| Medium | 1.0 |
| Hard | 1.0   |

To run the baseline:
```bash
export OPENAI_API_KEY=your_key_here
python -m email_triage_env.baseline
```

## HF Space Deployment
This environment is designed to be deployed to a Hugging Face Space. It is already configured for Docker execution and tagged with `openenv` for discovery.
