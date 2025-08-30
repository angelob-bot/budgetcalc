from __future__ import annotations
from typing import Callable, Optional

from budgeting.budget import Budget


class AlertService:
    """Service responsible for sending alerts when a budget is exceeded."""

    def __init__(self, channel: str = "console", email_sender: Optional[Callable[[str, str], None]] = None):
        self.channel = channel
        self.email_sender = email_sender or self._default_email_sender

    def _default_email_sender(self, recipient: str, message: str) -> None:
        """Fallback email sender that prints to stdout."""
        print(f"Email to {recipient}: {message}")

    def send_console_alert(self, message: str) -> None:
        print(message)

    def send_email_alert(self, recipient: str, message: str) -> None:
        self.email_sender(recipient, message)

    def check_budget(self, budget: Budget, recipient: Optional[str] = None) -> None:
        """Check the provided budget and send an alert if it is over limit."""
        if budget.is_over_limit():
            message = "Budget limit exceeded"
            if self.channel == "email":
                if recipient is None:
                    raise ValueError("recipient required for email alerts")
                self.send_email_alert(recipient, message)
            else:
                self.send_console_alert(message)
