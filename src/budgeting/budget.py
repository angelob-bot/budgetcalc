class Budget:
    """Simple budget tracker."""

    def __init__(self, limit: float):
        self.limit = float(limit)
        self.expenses = 0.0

    def add_expense(self, amount: float) -> None:
        """Add an expense to the budget."""
        self.expenses += float(amount)

    def is_over_limit(self) -> bool:
        """Return True if expenses exceed the budget limit."""
        return self.expenses > self.limit
