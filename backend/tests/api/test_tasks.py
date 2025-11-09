"""Tests for task API endpoints."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestTaskEndpoints:
    """Test suite for task API endpoints."""

    def test_get_all_tasks_empty(self, client: TestClient):
        """Test getting all tasks when database is empty."""
        response = client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0

    def test_get_all_tasks(self, client: TestClient, sample_task):
        """Test getting all tasks with data."""
        response = client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["total"] == 1
        assert data["tasks"][0]["title"] == sample_task["title"]

    def test_get_tasks_filter_by_status(self, client: TestClient, sample_task):
        """Test filtering tasks by status."""
        response = client.get("/api/tasks?status=todo")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert all(task["status"] == "todo" for task in data["tasks"])

        # Test filtering with non-matching status
        response = client.get("/api/tasks?status=completed")
        data = response.json()
        assert data["total"] == 0

    def test_get_tasks_filter_by_priority(self, client: TestClient, sample_task):
        """Test filtering tasks by priority."""
        response = client.get("/api/tasks?priority=medium")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert all(task["priority"] == "medium" for task in data["tasks"])

    def test_get_tasks_filter_by_category(
        self, client: TestClient, sample_task, sample_category
    ):
        """Test filtering tasks by category."""
        response = client.get(f"/api/tasks?category_id={sample_category['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert all(
            task["category_id"] == sample_category["id"] for task in data["tasks"]
        )

    def test_get_tasks_filter_by_nonexistent_category(self, client: TestClient):
        """Test filtering by non-existent category returns 404."""
        response = client.get("/api/tasks?category_id=9999")

        assert response.status_code == 404

    def test_create_task_success(self, client: TestClient, sample_category):
        """Test creating a new task successfully."""
        task_data = {
            "title": "New Task",
            "description": "Task description",
            "status": "todo",
            "priority": "high",
            "category_id": sample_category["id"],
            "due_date": "2025-12-31T23:59:59",
        }

        response = client.post("/api/tasks", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert data["priority"] == task_data["priority"]
        assert data["category_id"] == task_data["category_id"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_minimal(self, client: TestClient):
        """Test creating a task with only required fields."""
        task_data = {"title": "Minimal Task"}

        response = client.post("/api/tasks", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["status"] == "todo"  # Default value
        assert data["priority"] == "medium"  # Default value
        assert data["description"] is None
        assert data["category_id"] is None

    def test_create_task_invalid_category(self, client: TestClient):
        """Test creating a task with non-existent category."""
        task_data = {
            "title": "Task with invalid category",
            "category_id": 9999,
        }

        response = client.post("/api/tasks", json=task_data)

        assert response.status_code == 404

    def test_create_task_empty_title(self, client: TestClient):
        """Test creating a task with empty title."""
        task_data = {"title": ""}

        response = client.post("/api/tasks", json=task_data)

        assert response.status_code == 422

    def test_get_task_by_id_success(self, client: TestClient, sample_task):
        """Test getting a task by ID successfully."""
        response = client.get(f"/api/tasks/{sample_task['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task["id"]
        assert data["title"] == sample_task["title"]
        assert data["description"] == sample_task["description"]

    def test_get_task_by_id_not_found(self, client: TestClient):
        """Test getting a non-existent task."""
        response = client.get("/api/tasks/9999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["message"]

    def test_update_task_success(self, client: TestClient, sample_task):
        """Test updating a task successfully."""
        update_data = {
            "title": "Updated Task",
            "status": "in_progress",
            "priority": "high",
        }

        response = client.put(f"/api/tasks/{sample_task['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
        assert data["priority"] == update_data["priority"]

    def test_update_task_partial(self, client: TestClient, sample_task):
        """Test partial update of a task."""
        update_data = {"title": "Partially Updated"}

        response = client.put(f"/api/tasks/{sample_task['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        # Other fields should remain unchanged
        assert data["description"] == sample_task["description"]
        assert data["status"] == sample_task["status"]

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task."""
        update_data = {"title": "Updated Task"}

        response = client.put("/api/tasks/9999", json=update_data)

        assert response.status_code == 404

    def test_update_task_invalid_category(self, client: TestClient, sample_task):
        """Test updating task with non-existent category."""
        update_data = {"category_id": 9999}

        response = client.put(f"/api/tasks/{sample_task['id']}", json=update_data)

        assert response.status_code == 404

    def test_update_task_status_success(self, client: TestClient, sample_task):
        """Test updating only task status."""
        status_data = {"status": "completed"}

        response = client.patch(
            f"/api/tasks/{sample_task['id']}/status", json=status_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == status_data["status"]
        # Other fields should remain unchanged
        assert data["title"] == sample_task["title"]
        assert data["description"] == sample_task["description"]

    def test_update_task_status_not_found(self, client: TestClient):
        """Test updating status of non-existent task."""
        status_data = {"status": "completed"}

        response = client.patch("/api/tasks/9999/status", json=status_data)

        assert response.status_code == 404

    def test_delete_task_success(self, client: TestClient, sample_task):
        """Test deleting a task successfully."""
        response = client.delete(f"/api/tasks/{sample_task['id']}")

        assert response.status_code == 204

        # Verify task is deleted
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task."""
        response = client.delete("/api/tasks/9999")

        assert response.status_code == 404


class TestTaskIntegration:
    """Integration tests for task-related workflows."""

    def test_task_with_category_relationship(
        self, client: TestClient, sample_category
    ):
        """Test that task includes category details in response."""
        task_data = {
            "title": "Task with Category",
            "category_id": sample_category["id"],
        }

        response = client.post("/api/tasks", json=task_data)
        assert response.status_code == 201

        data = response.json()
        assert data["category"] is not None
        assert data["category"]["id"] == sample_category["id"]
        assert data["category"]["name"] == sample_category["name"]
        assert data["category"]["color"] == sample_category["color"]

    def test_multiple_tasks_workflow(self, client: TestClient, sample_category):
        """Test creating multiple tasks and filtering them."""
        # Create tasks with different statuses
        tasks_data = [
            {"title": "Task 1", "status": "todo", "priority": "high"},
            {"title": "Task 2", "status": "in_progress", "priority": "medium"},
            {"title": "Task 3", "status": "completed", "priority": "low"},
        ]

        for task_data in tasks_data:
            response = client.post("/api/tasks", json=task_data)
            assert response.status_code == 201

        # Test filtering by different criteria
        response = client.get("/api/tasks?status=todo")
        assert response.json()["total"] == 1

        response = client.get("/api/tasks?priority=high")
        assert response.json()["total"] == 1

        response = client.get("/api/tasks")
        assert response.json()["total"] == 3
