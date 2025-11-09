"""Pytest configuration and fixtures."""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.core.database import Base, get_db

# Create test database engine (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///./test_taskflow.db"
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.

    Yields:
        Session: Test database session
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with test database.

    Args:
        db: Test database session

    Yields:
        TestClient: FastAPI test client
    """

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_category(db: Session) -> dict:
    """
    Create a sample category for testing.

    Args:
        db: Database session

    Returns:
        dict: Sample category data
    """
    from app.models.category import Category

    category = Category(name="Work", color="#3B82F6")
    db.add(category)
    db.commit()
    db.refresh(category)

    return {
        "id": category.id,
        "name": category.name,
        "color": category.color,
    }


@pytest.fixture
def sample_task(db: Session, sample_category: dict) -> dict:
    """
    Create a sample task for testing.

    Args:
        db: Database session
        sample_category: Sample category fixture

    Returns:
        dict: Sample task data
    """
    from app.models.task import Task, TaskStatus, TaskPriority
    from datetime import datetime

    task = Task(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        category_id=sample_category["id"],
        due_date=datetime(2025, 12, 31, 23, 59, 59),
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "category_id": task.category_id,
        "due_date": task.due_date.isoformat(),
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }
