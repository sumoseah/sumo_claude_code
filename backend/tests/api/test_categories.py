"""Tests for category API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestCategoryEndpoints:
    """Test suite for category API endpoints."""

    def test_get_all_categories_empty(self, client: TestClient):
        """Test getting all categories when database is empty."""
        response = client.get("/api/categories")

        assert response.status_code == 200
        data = response.json()
        assert data["categories"] == []
        assert data["total"] == 0

    def test_get_all_categories(self, client: TestClient, sample_category):
        """Test getting all categories with data."""
        response = client.get("/api/categories")

        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 1
        assert data["total"] == 1
        assert data["categories"][0]["name"] == sample_category["name"]
        assert data["categories"][0]["color"] == sample_category["color"]

    def test_create_category_success(self, client: TestClient):
        """Test creating a new category successfully."""
        category_data = {"name": "Personal", "color": "#10B981"}

        response = client.post("/api/categories", json=category_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == category_data["name"]
        assert data["color"] == category_data["color"]
        assert "id" in data

    def test_create_category_without_color(self, client: TestClient):
        """Test creating a category without color (optional field)."""
        category_data = {"name": "Personal"}

        response = client.post("/api/categories", json=category_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == category_data["name"]
        assert data["color"] is None

    def test_create_category_duplicate_name(self, client: TestClient, sample_category):
        """Test creating a category with duplicate name."""
        category_data = {"name": sample_category["name"], "color": "#FF0000"}

        response = client.post("/api/categories", json=category_data)

        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["message"]

    def test_create_category_invalid_color(self, client: TestClient):
        """Test creating a category with invalid color format."""
        category_data = {"name": "Invalid", "color": "not-a-hex-color"}

        response = client.post("/api/categories", json=category_data)

        assert response.status_code == 422

    def test_create_category_empty_name(self, client: TestClient):
        """Test creating a category with empty name."""
        category_data = {"name": "", "color": "#10B981"}

        response = client.post("/api/categories", json=category_data)

        assert response.status_code == 422

    def test_get_category_by_id_success(self, client: TestClient, sample_category):
        """Test getting a category by ID successfully."""
        response = client.get(f"/api/categories/{sample_category['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_category["id"]
        assert data["name"] == sample_category["name"]
        assert data["color"] == sample_category["color"]

    def test_get_category_by_id_not_found(self, client: TestClient):
        """Test getting a non-existent category."""
        response = client.get("/api/categories/9999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["message"]
