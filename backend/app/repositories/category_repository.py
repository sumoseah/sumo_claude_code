"""Repository for category data access operations."""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryRepository:
    """
    Repository class for Category database operations.
    Encapsulates all database queries related to categories.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_all(self) -> List[Category]:
        """
        Retrieve all categories from the database.

        Returns:
            List of all Category objects
        """
        return self.db.query(Category).order_by(Category.name).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """
        Retrieve a category by its ID.

        Args:
            category_id: The category ID to search for

        Returns:
            Category object if found, None otherwise
        """
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Retrieve a category by its name.

        Args:
            name: The category name to search for

        Returns:
            Category object if found, None otherwise
        """
        return self.db.query(Category).filter(Category.name == name).first()

    def create(self, category_data: CategoryCreate) -> Category:
        """
        Create a new category in the database.

        Args:
            category_data: Pydantic schema with category data

        Returns:
            Created Category object
        """
        db_category = Category(**category_data.model_dump())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def delete(self, category: Category) -> None:
        """
        Delete a category from the database.

        Args:
            category: Category object to delete
        """
        self.db.delete(category)
        self.db.commit()

    def count(self) -> int:
        """
        Count total number of categories.

        Returns:
            Total count of categories
        """
        return self.db.query(Category).count()
