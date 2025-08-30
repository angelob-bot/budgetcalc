import os
import sys

# Ensure the src directory is on the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from budgeting.budget import Budget


def test_remaining_amount_under_budget():
    budget = Budget("groceries", 100)
    budget.add_expense(40)
    assert budget.remaining_amount() == 60


def test_remaining_amount_over_budget():
    budget = Budget("groceries", 100)
    budget.add_expense(120)
    assert budget.remaining_amount() == -20


def test_remaining_amount_multiple_periods():
    budget = Budget("entertainment", 100)
    budget.add_expense(80, period="2023-01")  # under budget
    budget.add_expense(120, period="2023-02")  # over budget

    assert budget.remaining_amount("2023-01") == 20
    assert budget.remaining_amount("2023-02") == -20
    # no expenses recorded for March
    assert budget.remaining_amount("2023-03") == 100
