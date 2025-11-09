"""Category-related Pydantic schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import re


class CategoryBase(BaseModel):
    """Base category schema with shared fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    color: Optional[str] = Field(
        None,
        description="Hex color code for the category (e.g., #FF5733)",
        pattern=r"^#[0-9A-Fa-f]{6}$",
    )

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate that color is a valid hex code."""
        if v is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code (e.g., #FF5733)")
        return v


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Work", "color": "#3B82F6"},
                {"name": "Personal", "color": "#10B981"},
            ]
        }
    }


class CategoryResponse(CategoryBase):
    """Schema for category response."""

    id: int = Field(..., description="Unique category identifier")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {"id": 1, "name": "Work", "color": "#3B82F6"},
            ]
        },
    }


class CategoryListResponse(BaseModel):
    """Schema for list of categories response."""

    categories: List[CategoryResponse] = Field(..., description="List of categories")
    total: int = Field(..., description="Total number of categories")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "categories": [
                        {"id": 1, "name": "Work", "color": "#3B82F6"},
                        {"id": 2, "name": "Personal", "color": "#10B981"},
                    ],
                    "total": 2,
                }
            ]
        }
    }
