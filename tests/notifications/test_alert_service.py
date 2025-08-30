import pytest

from budgeting.budget import Budget
from notifications.alert_service import AlertService


def test_console_alert_triggered_when_over_limit(capsys):
    budget = Budget(limit=100)
    budget.add_expense(150)
    alert = AlertService(channel="console")
    alert.check_budget(budget)
    captured = capsys.readouterr()
    assert "Budget limit exceeded" in captured.out


def test_email_alert_triggered_when_over_limit():
    budget = Budget(limit=100)
    budget.add_expense(150)
    sent = []

    def fake_sender(recipient, message):
        sent.append((recipient, message))

    alert = AlertService(channel="email", email_sender=fake_sender)
    alert.check_budget(budget, recipient="user@example.com")
    assert sent == [("user@example.com", "Budget limit exceeded")]
