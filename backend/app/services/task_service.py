"""Service layer for task business logic."""

from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.task_repository import TaskRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskListResponse,
)
from app.models.task import TaskStatus, TaskPriority
from app.core.exceptions import NotFoundException, ValidationException


class TaskService:
    """
    Service class for task business logic.
    Coordinates between API layer and repository layer.
    """

    def __init__(self, db: Session):
        """
        Initialize service with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.task_repository = TaskRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        category_id: Optional[int] = None,
    ) -> TaskListResponse:
        """
        Retrieve all tasks with optional filtering.

        Args:
            status: Filter by task status
            priority: Filter by task priority
            category_id: Filter by category ID

        Returns:
            TaskListResponse with list of tasks and total count

        Raises:
            NotFoundException: If specified category_id doesn't exist
        """
        # Validate category exists if filtering by category
        if category_id is not None:
            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise NotFoundException(resource="Category", resource_id=category_id)

        tasks = self.task_repository.get_all(
            status=status, priority=priority, category_id=category_id
        )
        total = self.task_repository.count(
            status=status, priority=priority, category_id=category_id
        )

        return TaskListResponse(
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            total=total,
        )

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """
        Create a new task.

        Args:
            task_data: Task creation data

        Returns:
            TaskResponse with created task

        Raises:
            NotFoundException: If specified category_id doesn't exist
            ValidationException: If validation fails
        """
        # Validate category exists if provided
        if task_data.category_id is not None:
            category = self.category_repository.get_by_id(task_data.category_id)
            if not category:
                raise NotFoundException(
                    resource="Category", resource_id=task_data.category_id
                )

        task = self.task_repository.create(task_data)
        return TaskResponse.model_validate(task)

    def get_task_by_id(self, task_id: int) -> TaskResponse:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            TaskResponse with task data

        Raises:
            NotFoundException: If task is not found
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundException(resource="Task", resource_id=task_id)

        return TaskResponse.model_validate(task)

    def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        """
        Update an existing task.

        Args:
            task_id: Task ID to update
            task_data: Updated task data

        Returns:
            TaskResponse with updated task

        Raises:
            NotFoundException: If task or category is not found
            ValidationException: If validation fails
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundException(resource="Task", resource_id=task_id)

        # Validate category exists if being updated
        if task_data.category_id is not None:
            category = self.category_repository.get_by_id(task_data.category_id)
            if not category:
                raise NotFoundException(
                    resource="Category", resource_id=task_data.category_id
                )

        updated_task = self.task_repository.update(task, task_data)
        return TaskResponse.model_validate(updated_task)

    def update_task_status(
        self, task_id: int, status_data: TaskStatusUpdate
    ) -> TaskResponse:
        """
        Update only the status of a task.

        Args:
            task_id: Task ID to update
            status_data: New status data

        Returns:
            TaskResponse with updated task

        Raises:
            NotFoundException: If task is not found
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundException(resource="Task", resource_id=task_id)

        updated_task = self.task_repository.update_status(task, status_data.status)
        return TaskResponse.model_validate(updated_task)

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task.

        Args:
            task_id: Task ID to delete

        Raises:
            NotFoundException: If task is not found
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundException(resource="Task", resource_id=task_id)

        self.task_repository.delete(task)
