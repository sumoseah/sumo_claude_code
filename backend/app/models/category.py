"""Category database model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    """
    Category model for organizing tasks.

    Attributes:
        id: Unique identifier for the category
        name: Category name (must be unique)
        color: Optional hex color code for UI display (e.g., #FF5733)
        tasks: Relationship to associated tasks
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(7), nullable=True)  # Hex color format: #RRGGBB

    # Relationship to tasks
    tasks = relationship("Task", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"
