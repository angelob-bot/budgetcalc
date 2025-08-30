class Budget:
    """Represents a spending category with a limit.

    Expenses can be recorded per period (e.g. by month). The remaining
    amount is calculated per period as the limit minus recorded expenses.
    """

    def __init__(self, category: str, limit: float):
        self.category = category
        self.limit = float(limit)
        self._expenses = {}

    def add_expense(self, amount: float, period: str = "default") -> None:
        """Record an expense for the given period."""
        self._expenses[period] = self._expenses.get(period, 0) + float(amount)

    def spent(self, period: str = "default") -> float:
        """Return the total amount spent for the given period."""
        return self._expenses.get(period, 0.0)

    def remaining_amount(self, period: str = "default") -> float:
        """Compute how much is left for the budget in the given period.

        A negative value indicates the budget has been exceeded.
        """
        return self.limit - self.spent(period)
