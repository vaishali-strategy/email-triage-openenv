from typing import Tuple, Dict, Any, Optional
from email_triage_env.models import Action, Observation, Reward, State, Email
from email_triage_env.tasks import TASKS

class EmailTriageEnv:
    def __init__(self):
        self._state: Optional[State] = None
        self._current_task_id: str = "easy"
        # Align with inference.py requirements
        self.tasks = [
            {'id': 'easy', 'goal': TASKS['easy'].description},
            {'id': 'medium', 'goal': TASKS['medium'].description},
            {'id': 'hard', 'goal': TASKS['hard'].description}
        ]

    def reset(self, task_idx: int = 0) -> Observation:
        # Map task_idx to task_id
        task_list = list(TASKS.keys())
        if task_idx < len(task_list):
            self._current_task_id = task_list[task_idx]
        else:
            self._current_task_id = "easy"
            
        task = TASKS[self._current_task_id]
        self._state = State(
            all_emails=task.get_initial_emails(),
            current_email_id=None,
            step_count=0,
            max_steps=20
        )
        return self._get_observation("Reset successful")

    @property
    def state_data(self) -> Dict[str, Any]:
        if self._state is None:
            return {"steps": 0}
        return {"steps": self._state.step_count}

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        if self._state is None:
            raise ValueError("Call reset() before step()")

        self._state.step_count += 1
        status = "Success"
        reward_value = 0.0
        reason = "No reward"

        try:
            if action.action_type == "read":
                email = next((e for e in self._state.all_emails if e.id == action.email_id), None)
                if email:
                    self._state.current_email_id = email.id
                else:
                    status = f"Error: Email with ID {action.email_id} not found"
            
            elif action.action_type == "archive":
                email = next((e for e in self._state.all_emails if e.id == action.email_id), None)
                if email:
                    email.is_archived = True
                    reward_value = 0.1 # Small reward for archiving
                    reason = "Email archived"
                else:
                    status = f"Error: Email with ID {action.email_id} not found"

            elif action.action_type == "reply":
                email = next((e for e in self._state.all_emails if e.id == action.email_id), None)
                if email:
                    email.reply_sent = action.content
                    reward_value = 0.2 # Small reward for replying
                    reason = "Reply sent"
                else:
                    status = f"Error: Email with ID {action.email_id} not found"

            elif action.action_type == "label":
                email = next((e for e in self._state.all_emails if e.id == action.email_id), None)
                if email:
                    email.label = action.content
                    reward_value = 0.1 # Small reward for labeling
                    reason = f"Labeled as {action.content}"
                else:
                    status = f"Error: Email with ID {action.email_id} not found"

            elif action.action_type == "delete":
                email = next((e for e in self._state.all_emails if e.id == action.email_id), None)
                if email:
                    email.is_deleted = True
                else:
                    status = f"Error: Email with ID {action.email_id} not found"
            
            else:
                status = f"Error: Unknown action type {action.action_type}"

        except Exception as e:
            status = f"Error: {str(e)}"

        # Task-specific reward (if any)
        task = TASKS[self._current_task_id]
        final_grade = task.grade(self._state)
        
        # If the task is fully completed, provide a larger reward
        if final_grade == 1.0:
            reward_value += 1.0
            reason += " | Task completed!"

        done = self._state.step_count >= self._state.max_steps or final_grade == 1.0
        observation = self._get_observation(status, done)
        reward = Reward(value=reward_value, reason=reason)
        
        info = {
            "step_count": self._state.step_count,
            "final_grade": final_grade
        }
        
        return observation, reward, done, info

    def state(self) -> State:
        return self._state

    def _get_observation(self, status: str, done: bool = False) -> Observation:
        active_emails = [e for e in self._state.all_emails if not e.is_archived and not e.is_deleted]
        current_email = next((e for e in self._state.all_emails if e.id == self._state.current_email_id), None)
        return Observation(
            emails=active_emails,
            current_email=current_email,
            last_action_status=status,
            done=done
        )
