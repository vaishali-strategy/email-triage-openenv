from typing import List, Optional, Union
from pydantic import BaseModel, Field

class Email(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    label: Optional[str] = None
    is_archived: bool = False
    is_deleted: bool = False
    reply_sent: Optional[str] = None

class Action(BaseModel):
    action_type: str = Field(..., description="The type of action to perform: read, archive, reply, label, delete")
    email_id: Optional[str] = Field(None, description="The ID of the email to act upon")
    content: Optional[str] = Field(None, description="The content of the reply or the label to apply")

class Observation(BaseModel):
    emails: List[Email] = Field(..., description="List of emails currently in the inbox (not archived or deleted)")
    current_email: Optional[Email] = Field(None, description="The email currently being read")
    last_action_status: str = Field(..., description="Result of the last action: 'success' or an error message")
    done: bool = Field(False, description="Whether the episode is finished")

class Reward(BaseModel):
    value: float = Field(..., description="The reward value")
    reason: str = Field(..., description="Explanation for the reward")

class State(BaseModel):
    all_emails: List[Email]
    current_email_id: Optional[str] = None
    step_count: int = 0
    max_steps: int = 20
