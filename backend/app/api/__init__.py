"""API router configuration."""

from fastapi import APIRouter
from app.api import tasks, categories

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
