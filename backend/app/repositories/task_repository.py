"""Repository for task data access operations."""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """
    Repository class for Task database operations.
    Encapsulates all database queries related to tasks.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_all(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        category_id: Optional[int] = None,
    ) -> List[Task]:
        """
        Retrieve tasks with optional filtering.

        Args:
            status: Filter by task status
            priority: Filter by task priority
            category_id: Filter by category ID

        Returns:
            List of Task objects matching the filters
        """
        query = self.db.query(Task).options(joinedload(Task.category))

        if status is not None:
            query = query.filter(Task.status == status)
        if priority is not None:
            query = query.filter(Task.priority == priority)
        if category_id is not None:
            query = query.filter(Task.category_id == category_id)

        return query.order_by(Task.created_at.desc()).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID with category relationship loaded.

        Args:
            task_id: The task ID to search for

        Returns:
            Task object if found, None otherwise
        """
        return (
            self.db.query(Task)
            .options(joinedload(Task.category))
            .filter(Task.id == task_id)
            .first()
        )

    def create(self, task_data: TaskCreate) -> Task:
        """
        Create a new task in the database.

        Args:
            task_data: Pydantic schema with task data

        Returns:
            Created Task object
        """
        db_task = Task(**task_data.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        # Explicitly load category relationship
        self.db.refresh(db_task, ["category"])
        return db_task

    def update(self, task: Task, task_data: TaskUpdate) -> Task:
        """
        Update an existing task with provided data.

        Args:
            task: Task object to update
            task_data: Pydantic schema with updated task data

        Returns:
            Updated Task object
        """
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        # Explicitly load category relationship
        self.db.refresh(task, ["category"])
        return task

    def update_status(self, task: Task, status: TaskStatus) -> Task:
        """
        Update only the status of a task.

        Args:
            task: Task object to update
            status: New status value

        Returns:
            Updated Task object
        """
        task.status = status
        self.db.commit()
        self.db.refresh(task)
        # Explicitly load category relationship
        self.db.refresh(task, ["category"])
        return task

    def delete(self, task: Task) -> None:
        """
        Delete a task from the database.

        Args:
            task: Task object to delete
        """
        self.db.delete(task)
        self.db.commit()

    def count(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        category_id: Optional[int] = None,
    ) -> int:
        """
        Count tasks with optional filtering.

        Args:
            status: Filter by task status
            priority: Filter by task priority
            category_id: Filter by category ID

        Returns:
            Count of tasks matching the filters
        """
        query = self.db.query(Task)

        if status is not None:
            query = query.filter(Task.status == status)
        if priority is not None:
            query = query.filter(Task.priority == priority)
        if category_id is not None:
            query = query.filter(Task.category_id == category_id)

        return query.count()
