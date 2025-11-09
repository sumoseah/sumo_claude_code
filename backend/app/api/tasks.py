"""Task API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskListResponse,
)
from app.schemas.common import ErrorResponse
from app.models.task import TaskStatus, TaskPriority

router = APIRouter()


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Get all tasks",
    description="Retrieve a list of all tasks with optional filtering by status, priority, and category.",
    responses={
        200: {"description": "Successfully retrieved tasks", "model": TaskListResponse},
        404: {
            "description": "Category not found (when filtering by category)",
            "model": ErrorResponse,
        },
    },
)
def get_tasks(
    status: Optional[TaskStatus] = Query(
        None, description="Filter tasks by status (todo, in_progress, completed)"
    ),
    priority: Optional[TaskPriority] = Query(
        None, description="Filter tasks by priority (low, medium, high)"
    ),
    category_id: Optional[int] = Query(
        None, description="Filter tasks by category ID"
    ),
    db: Session = Depends(get_db),
) -> TaskListResponse:
    """
    Get all tasks with optional filters.

    Args:
        status: Optional filter by task status
        priority: Optional filter by task priority
        category_id: Optional filter by category ID
        db: Database session

    Returns:
        TaskListResponse: List of tasks matching the filters with total count

    Raises:
        NotFoundException: If specified category_id doesn't exist
    """
    service = TaskService(db)
    return service.get_all_tasks(
        status=status, priority=priority, category_id=category_id
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with the provided information.",
    responses={
        201: {"description": "Task created successfully", "model": TaskResponse},
        404: {
            "description": "Category not found (if category_id provided)",
            "model": ErrorResponse,
        },
        422: {"description": "Validation error", "model": ErrorResponse},
    },
)
def create_task(
    task_data: TaskCreate, db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task.

    Args:
        task_data: Task creation data
        db: Database session

    Returns:
        TaskResponse: The created task

    Raises:
        NotFoundException: If specified category_id doesn't exist
        ValidationException: If validation fails
    """
    service = TaskService(db)
    return service.create_task(task_data)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    description="Retrieve a task by its ID.",
    responses={
        200: {"description": "Task found", "model": TaskResponse},
        404: {"description": "Task not found", "model": ErrorResponse},
    },
)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """
    Get a task by ID.

    Args:
        task_id: The task ID to retrieve
        db: Database session

    Returns:
        TaskResponse: The task data

    Raises:
        NotFoundException: If task is not found
    """
    service = TaskService(db)
    return service.get_task_by_id(task_id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task with the provided information.",
    responses={
        200: {"description": "Task updated successfully", "model": TaskResponse},
        404: {
            "description": "Task or category not found",
            "model": ErrorResponse,
        },
        422: {"description": "Validation error", "model": ErrorResponse},
    },
)
def update_task(
    task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update an existing task.

    Args:
        task_id: The task ID to update
        task_data: Updated task data
        db: Database session

    Returns:
        TaskResponse: The updated task

    Raises:
        NotFoundException: If task or category is not found
        ValidationException: If validation fails
    """
    service = TaskService(db)
    return service.update_task(task_id, task_data)


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Update task status",
    description="Update only the status of an existing task.",
    responses={
        200: {"description": "Task status updated successfully", "model": TaskResponse},
        404: {"description": "Task not found", "model": ErrorResponse},
        422: {"description": "Validation error", "model": ErrorResponse},
    },
)
def update_task_status(
    task_id: int, status_data: TaskStatusUpdate, db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update task status only.

    Args:
        task_id: The task ID to update
        status_data: New status data
        db: Database session

    Returns:
        TaskResponse: The updated task

    Raises:
        NotFoundException: If task is not found
    """
    service = TaskService(db)
    return service.update_task_status(task_id, status_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete an existing task by its ID.",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found", "model": ErrorResponse},
    },
)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a task.

    Args:
        task_id: The task ID to delete
        db: Database session

    Raises:
        NotFoundException: If task is not found
    """
    service = TaskService(db)
    service.delete_task(task_id)
