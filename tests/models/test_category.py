from models.category import (
    categories,
    create_category,
    read_category,
    update_category,
    delete_category,
)


def setup_function(fn):
    categories.clear()


def test_category_crud():
    create_category(1, "Food", "expense")
    cat = read_category(1)
    assert cat is not None
    assert cat.name == "Food"
    update_category(1, name="Groceries")
    cat = read_category(1)
    assert cat.name == "Groceries"
    delete_category(1)
    assert read_category(1) is None
