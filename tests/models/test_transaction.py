from datetime import date

from models.category import create_category, categories
from models.transaction import (
    create_transaction,
    read_transaction,
    update_transaction,
    delete_transaction,
    total_by_category,
    transactions,
)


def setup_function(fn):
    categories.clear()
    transactions.clear()


def test_transaction_crud_and_aggregation():
    create_category(1, "Salary", "income")
    create_category(2, "Food", "expense")
    t1 = create_transaction(100.0, date(2023, 1, 1), 1)
    t2 = create_transaction(50.0, date(2023, 1, 2), 2)
    t3 = create_transaction(25.0, date(2023, 1, 3), 2)

    assert read_transaction(t1.id).amount == 100.0

    update_transaction(t1.id, amount=150.0)
    assert read_transaction(t1.id).amount == 150.0

    assert total_by_category(2) == 75.0

    delete_transaction(t2.id)
    assert total_by_category(2) == 25.0
