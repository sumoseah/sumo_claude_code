"""Custom exception classes for the application."""

from typing import Any, Dict, Optional


class TaskFlowException(Exception):
    """Base exception class for TaskFlow application."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(TaskFlowException):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, resource_id: Any):
        message = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=message, status_code=404)


class ValidationException(TaskFlowException):
    """Exception raised when validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)


class DuplicateException(TaskFlowException):
    """Exception raised when attempting to create a duplicate resource."""

    def __init__(self, resource: str, field: str, value: Any):
        message = f"{resource} with {field} '{value}' already exists"
        super().__init__(message=message, status_code=409)
