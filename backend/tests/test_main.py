"""Tests for main application functionality."""

import pytest
from fastapi.testclient import TestClient


class TestMainEndpoints:
    """Test suite for main application endpoints."""

    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint returns API information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data
        assert data["name"] == "TaskFlow API"

    def test_health_check(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data

    def test_docs_available(self, client: TestClient):
        """Test that OpenAPI documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self, client: TestClient):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
