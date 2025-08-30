from dataclasses import dataclass
from datetime import date
from typing import Dict, Optional


@dataclass
class Transaction:
    id: int
    amount: float
    date: date
    category_id: int
    notes: str = ""


# In-memory storage for transactions
transactions: Dict[int, Transaction] = {}
_transaction_counter = 0


def create_transaction(amount: float, date: date, category_id: int, notes: str = "") -> Transaction:
    """Create and store a new transaction."""
    global _transaction_counter
    _transaction_counter += 1
    transaction = Transaction(id=_transaction_counter, amount=amount, date=date, category_id=category_id, notes=notes)
    transactions[transaction.id] = transaction
    return transaction


def read_transaction(transaction_id: int) -> Optional[Transaction]:
    """Retrieve a transaction by its id."""
    return transactions.get(transaction_id)


def update_transaction(transaction_id: int, amount: Optional[float] = None, date: Optional[date] = None,
                       category_id: Optional[int] = None, notes: Optional[str] = None) -> Optional[Transaction]:
    """Update fields of an existing transaction."""
    transaction = transactions.get(transaction_id)
    if transaction:
        if amount is not None:
            transaction.amount = amount
        if date is not None:
            transaction.date = date
        if category_id is not None:
            transaction.category_id = category_id
        if notes is not None:
            transaction.notes = notes
    return transaction


def delete_transaction(transaction_id: int) -> Optional[Transaction]:
    """Remove a transaction from storage."""
    return transactions.pop(transaction_id, None)


def total_by_category(category_id: int) -> float:
    """Aggregate the total amount for a given category."""
    return sum(t.amount for t in transactions.values() if t.category_id == category_id)
