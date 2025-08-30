from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Category:
    id: int
    name: str
    type: str  # income or expense


# In-memory storage for categories
categories: Dict[int, Category] = {}


def create_category(id: int, name: str, type: str) -> Category:
    """Create and store a new category."""
    category = Category(id=id, name=name, type=type)
    categories[id] = category
    return category


def read_category(id: int) -> Optional[Category]:
    """Retrieve a category by its id."""
    return categories.get(id)


def update_category(id: int, name: Optional[str] = None, type: Optional[str] = None) -> Optional[Category]:
    """Update fields of an existing category."""
    category = categories.get(id)
    if category:
        if name is not None:
            category.name = name
        if type is not None:
            category.type = type
    return category


def delete_category(id: int) -> Optional[Category]:
    """Remove a category from storage."""
    return categories.pop(id, None)
