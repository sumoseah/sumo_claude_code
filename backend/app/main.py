"""Main FastAPI application module."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import TaskFlowException
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan event handler.
    Initializes database on startup.
    """
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: Add cleanup logic here if needed


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="""
    TaskFlow API - A modern task management application backend.

    ## Features

    * **Task Management**: Create, read, update, and delete tasks
    * **Category Organization**: Organize tasks into categories
    * **Filtering**: Filter tasks by status, priority, and category
    * **Status Updates**: Quickly update task status
    * **Data Validation**: Comprehensive input validation using Pydantic

    ## Task Status Values

    * `todo` - Task not yet started
    * `in_progress` - Task currently being worked on
    * `completed` - Task finished

    ## Task Priority Values

    * `low` - Low priority task
    * `medium` - Medium priority task
    * `high` - High priority task
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for custom exceptions
@app.exception_handler(TaskFlowException)
async def taskflow_exception_handler(
    request: Request, exc: TaskFlowException
) -> JSONResponse:
    """
    Handle custom TaskFlow exceptions.

    Args:
        request: The request that caused the exception
        exc: The TaskFlowException instance

    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "status_code": exc.status_code,
            "details": exc.details,
        },
    )


# Health check endpoint
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check if the API is running and healthy.",
    response_description="API health status",
)
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }


# Include API router with prefix
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Get information about the API.",
)
async def root() -> dict:
    """
    Root endpoint providing API information.

    Returns:
        dict: API metadata
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
