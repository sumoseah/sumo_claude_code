"""Task database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Enum for task status values."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, enum.Enum):
    """Enum for task priority values."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    """
    Task model representing a user's task.

    Attributes:
        id: Unique identifier for the task
        title: Task title (required)
        description: Detailed description (optional)
        status: Current status (todo, in_progress, completed)
        priority: Priority level (low, medium, high)
        category_id: Foreign key to category (optional)
        due_date: Optional deadline for the task
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        category: Relationship to category object
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.TODO,
        index=True,
    )
    priority = Column(
        Enum(TaskPriority),
        nullable=False,
        default=TaskPriority.MEDIUM,
        index=True,
    )
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationship to category
    category = relationship("Category", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
