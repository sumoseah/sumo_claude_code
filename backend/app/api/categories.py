"""Category API endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryListResponse
from app.schemas.common import ErrorResponse

router = APIRouter()


@router.get(
    "",
    response_model=CategoryListResponse,
    summary="Get all categories",
    description="Retrieve a list of all categories in the system.",
    responses={
        200: {
            "description": "Successfully retrieved categories",
            "model": CategoryListResponse,
        }
    },
)
def get_categories(db: Session = Depends(get_db)) -> CategoryListResponse:
    """
    Get all categories.

    Returns:
        CategoryListResponse: List of all categories with total count
    """
    service = CategoryService(db)
    return service.get_all_categories()


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Create a new category with the provided information.",
    responses={
        201: {"description": "Category created successfully", "model": CategoryResponse},
        409: {
            "description": "Category with this name already exists",
            "model": ErrorResponse,
        },
        422: {"description": "Validation error", "model": ErrorResponse},
    },
)
def create_category(
    category_data: CategoryCreate, db: Session = Depends(get_db)
) -> CategoryResponse:
    """
    Create a new category.

    Args:
        category_data: Category creation data
        db: Database session

    Returns:
        CategoryResponse: The created category

    Raises:
        DuplicateException: If category with the same name already exists
    """
    service = CategoryService(db)
    return service.create_category(category_data)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get a specific category",
    description="Retrieve a category by its ID.",
    responses={
        200: {"description": "Category found", "model": CategoryResponse},
        404: {"description": "Category not found", "model": ErrorResponse},
    },
)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryResponse:
    """
    Get a category by ID.

    Args:
        category_id: The category ID to retrieve
        db: Database session

    Returns:
        CategoryResponse: The category data

    Raises:
        NotFoundException: If category is not found
    """
    service = CategoryService(db)
    return service.get_category_by_id(category_id)
