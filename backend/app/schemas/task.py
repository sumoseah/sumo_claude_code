"""Task-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.task import TaskStatus, TaskPriority
from app.schemas.category import CategoryResponse


class TaskBase(BaseModel):
    """Base task schema with shared fields."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Task title"
    )
    description: Optional[str] = Field(None, description="Detailed task description")
    status: TaskStatus = Field(
        default=TaskStatus.TODO, description="Current status of the task"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="Priority level of the task"
    )
    category_id: Optional[int] = Field(
        None, description="ID of the category this task belongs to"
    )
    due_date: Optional[datetime] = Field(
        None, description="Optional deadline for the task"
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Complete project proposal",
                    "description": "Write and submit the Q1 project proposal",
                    "status": "todo",
                    "priority": "high",
                    "category_id": 1,
                    "due_date": "2025-10-30T17:00:00",
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Task title"
    )
    description: Optional[str] = Field(None, description="Detailed task description")
    status: Optional[TaskStatus] = Field(None, description="Current status of the task")
    priority: Optional[TaskPriority] = Field(
        None, description="Priority level of the task"
    )
    category_id: Optional[int] = Field(
        None, description="ID of the category this task belongs to"
    )
    due_date: Optional[datetime] = Field(
        None, description="Optional deadline for the task"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Complete project proposal (Updated)",
                    "status": "in_progress",
                    "priority": "high",
                }
            ]
        }
    }


class TaskStatusUpdate(BaseModel):
    """Schema for updating only the task status."""

    status: TaskStatus = Field(..., description="New status for the task")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "in_progress"},
                {"status": "completed"},
            ]
        }
    }


class TaskResponse(TaskBase):
    """Schema for task response including computed fields."""

    id: int = Field(..., description="Unique task identifier")
    created_at: datetime = Field(..., description="Timestamp when task was created")
    updated_at: datetime = Field(..., description="Timestamp when task was last updated")
    category: Optional[CategoryResponse] = Field(
        None, description="Category details if task is categorized"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Complete project proposal",
                    "description": "Write and submit the Q1 project proposal",
                    "status": "in_progress",
                    "priority": "high",
                    "category_id": 1,
                    "category": {"id": 1, "name": "Work", "color": "#3B82F6"},
                    "due_date": "2025-10-30T17:00:00",
                    "created_at": "2025-10-22T10:00:00",
                    "updated_at": "2025-10-22T14:30:00",
                }
            ]
        },
    }


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""

    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks matching the query")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tasks": [
                        {
                            "id": 1,
                            "title": "Complete project proposal",
                            "description": "Write and submit the Q1 project proposal",
                            "status": "in_progress",
                            "priority": "high",
                            "category_id": 1,
                            "category": {"id": 1, "name": "Work", "color": "#3B82F6"},
                            "due_date": "2025-10-30T17:00:00",
                            "created_at": "2025-10-22T10:00:00",
                            "updated_at": "2025-10-22T14:30:00",
                        }
                    ],
                    "total": 1,
                }
            ]
        }
    }
