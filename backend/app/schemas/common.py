"""Common schemas shared across the application."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    message: str = Field(..., description="Error message describing what went wrong")
    status_code: int = Field(..., description="HTTP status code")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Task with id '999' not found",
                    "status_code": 404,
                    "details": {},
                }
            ]
        }
    }
