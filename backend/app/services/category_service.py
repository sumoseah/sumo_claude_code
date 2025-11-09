"""Service layer for category business logic."""

from typing import List
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryListResponse
from app.core.exceptions import NotFoundException, DuplicateException


class CategoryService:
    """
    Service class for category business logic.
    Coordinates between API layer and repository layer.
    """

    def __init__(self, db: Session):
        """
        Initialize service with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.repository = CategoryRepository(db)

    def get_all_categories(self) -> CategoryListResponse:
        """
        Retrieve all categories.

        Returns:
            CategoryListResponse with list of categories and total count
        """
        categories = self.repository.get_all()
        return CategoryListResponse(
            categories=[CategoryResponse.model_validate(cat) for cat in categories],
            total=len(categories),
        )

    def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        """
        Create a new category.

        Args:
            category_data: Category creation data

        Returns:
            CategoryResponse with created category

        Raises:
            DuplicateException: If category with the same name already exists
        """
        # Check for duplicate name
        existing_category = self.repository.get_by_name(category_data.name)
        if existing_category:
            raise DuplicateException(
                resource="Category", field="name", value=category_data.name
            )

        category = self.repository.create(category_data)
        return CategoryResponse.model_validate(category)

    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        """
        Retrieve a category by its ID.

        Args:
            category_id: Category ID to retrieve

        Returns:
            CategoryResponse with category data

        Raises:
            NotFoundException: If category is not found
        """
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundException(resource="Category", resource_id=category_id)

        return CategoryResponse.model_validate(category)
