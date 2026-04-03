from typing import List, Dict, Any
from models import State, Email

class Task:
    def __init__(self, id: str, description: str, difficulty: str):
        self.id = id
        self.description = description
        self.difficulty = difficulty

    def get_initial_emails(self) -> List[Email]:
        raise NotImplementedError

    def grade(self, state: State) -> float:
        raise NotImplementedError

class EasyTask(Task):
    def __init__(self):
        super().__init__("archive_boss", "Archive the email from boss@company.com", "easy")

    def get_initial_emails(self) -> List[Email]:
        return [
            Email(id="1", sender="boss@company.com", subject="Meeting", body="Let's meet at 10am."),
            Email(id="2", sender="friend@home.com", subject="Dinner?", body="Want to grab dinner?"),
        ]

    def grade(self, state: State) -> float:
        for email in state.all_emails:
            if email.sender == "boss@company.com" and email.is_archived:
                return 1.0
        return 0.0

class MediumTask(Task):
    def __init__(self):
        super().__init__("reply_support", "Reply to the support email with 'Issue resolved'", "medium")

    def get_initial_emails(self) -> List[Email]:
        return [
            Email(id="1", sender="support@service.com", subject="Ticket #123", body="Please confirm if your issue is resolved."),
            Email(id="2", sender="newsletter@tech.com", subject="Weekly Update", body="Here's what happened this week."),
        ]

    def grade(self, state: State) -> float:
        for email in state.all_emails:
            if email.sender == "support@service.com" and email.reply_sent == "Issue resolved":
                return 1.0
        return 0.0

class HardTask(Task):
    def __init__(self):
        super().__init__("spam_triage", "Label all spam emails as 'Spam' and archive them", "hard")

    def get_initial_emails(self) -> List[Email]:
        return [
            Email(id="1", sender="spammer@spam.com", subject="Win a prize!", body="You've won a million dollars!"),
            Email(id="2", sender="scammer@scam.com", subject="Account locked", body="Please login to unlock your account."),
            Email(id="3", sender="colleague@work.com", subject="Project Update", body="The project is on track."),
        ]

    def grade(self, state: State) -> float:
        total_spam = 2
        correctly_handled = 0
        for email in state.all_emails:
            if email.sender in ["spammer@spam.com", "scammer@scam.com"]:
                if email.label == "Spam" and email.is_archived:
                    correctly_handled += 1
        return correctly_handled / total_spam

TASKS = {
    "easy": EasyTask(),
    "medium": MediumTask(),
    "hard": HardTask(),
}
