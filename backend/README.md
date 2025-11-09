# TaskFlow API

A modern, production-ready FastAPI backend for task management with comprehensive CRUD operations, filtering, and category organization.

## Features

- **Complete Task Management**: Create, read, update, and delete tasks
- **Category Organization**: Organize tasks into customizable categories
- **Advanced Filtering**: Filter tasks by status, priority, and category
- **Status Management**: Quick status updates for tasks
- **Data Validation**: Comprehensive input validation using Pydantic
- **RESTful API**: Clean, intuitive API design following REST principles
- **Auto-Generated Documentation**: Interactive API docs with Swagger UI
- **Type Safety**: Full type hints throughout the codebase
- **Test Coverage**: Comprehensive test suite with pytest
- **CORS Support**: Pre-configured CORS middleware for frontend integration

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic 2.5.3
- **Testing**: pytest with pytest-asyncio and pytest-cov
- **Code Quality**: black, ruff, mypy

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── tasks.py        # Task endpoints
│   │   └── categories.py   # Category endpoints
│   ├── core/               # Core configuration
│   │   ├── config.py       # Settings management
│   │   ├── database.py     # Database configuration
│   │   └── exceptions.py   # Custom exceptions
│   ├── models/             # SQLAlchemy models
│   │   ├── task.py
│   │   └── category.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── task.py
│   │   ├── category.py
│   │   └── common.py
│   ├── services/           # Business logic layer
│   │   ├── task_service.py
│   │   └── category_service.py
│   ├── repositories/       # Data access layer
│   │   ├── task_repository.py
│   │   └── category_repository.py
│   └── main.py            # Application entry point
├── tests/                  # Test suite
│   ├── api/
│   │   ├── test_tasks.py
│   │   └── test_categories.py
│   ├── conftest.py
│   └── test_main.py
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

1. **Clone the repository** (or navigate to the backend directory):
   ```bash
   cd /Users/linus/taskflow-app/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

## Running the Application

### Development Server

Start the development server with auto-reload:

```bash
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks (with optional filters) |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get a specific task |
| PUT | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |
| PATCH | `/api/tasks/{id}/status` | Update task status only |

#### Query Parameters for GET /api/tasks

- `status` (optional): Filter by status (todo, in_progress, completed)
- `priority` (optional): Filter by priority (low, medium, high)
- `category_id` (optional): Filter by category ID

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | Get all categories |
| POST | `/api/categories` | Create a new category |
| GET | `/api/categories/{id}` | Get a specific category |

## Data Models

### Task

```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Write and submit the Q1 project proposal",
  "status": "in_progress",
  "priority": "high",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6"
  },
  "due_date": "2025-10-30T17:00:00",
  "created_at": "2025-10-22T10:00:00",
  "updated_at": "2025-10-22T14:30:00"
}
```

**Fields:**
- `id` (integer): Unique identifier
- `title` (string, required): Task title (1-200 characters)
- `description` (string, optional): Detailed description
- `status` (string, required): One of: `todo`, `in_progress`, `completed` (default: `todo`)
- `priority` (string, required): One of: `low`, `medium`, `high` (default: `medium`)
- `category_id` (integer, optional): Associated category ID
- `category` (object, optional): Category details (included in responses)
- `due_date` (datetime, optional): Task deadline
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Category

```json
{
  "id": 1,
  "name": "Work",
  "color": "#3B82F6"
}
```

**Fields:**
- `id` (integer): Unique identifier
- `name` (string, required): Category name (1-100 characters, unique)
- `color` (string, optional): Hex color code (e.g., #FF5733)

## Testing

Run the complete test suite:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=app --cov-report=html
```

Run specific test file:

```bash
pytest tests/api/test_tasks.py
```

Run tests with verbose output:

```bash
pytest -v
```

### Test Coverage

The test suite includes:
- **API endpoint tests**: All CRUD operations for tasks and categories
- **Validation tests**: Input validation and error handling
- **Integration tests**: Multi-task workflows and relationships
- **Edge case tests**: Empty databases, non-existent resources, duplicate entries

## Code Quality

Format code with black:

```bash
black app/ tests/
```

Lint code with ruff:

```bash
ruff check app/ tests/
```

Type check with mypy:

```bash
mypy app/
```

## Configuration

Environment variables (in `.env` file):

```env
# Database
DATABASE_URL=sqlite:///./taskflow.db

# API
API_V1_PREFIX=/api
PROJECT_NAME=TaskFlow API
PROJECT_VERSION=1.0.0

# CORS (comma-separated origins)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Logging
LOG_LEVEL=INFO
```

## CORS Configuration

The API is pre-configured to allow requests from common frontend development servers:
- http://localhost:3000 (React default)
- http://localhost:5173 (Vite default)
- http://localhost:8080 (Vue CLI default)

To add more origins, update the `ALLOWED_ORIGINS` variable in your `.env` file.

## Error Handling

The API returns consistent error responses:

```json
{
  "message": "Task with id '999' not found",
  "status_code": 404,
  "details": {}
}
```

### HTTP Status Codes

- `200 OK`: Successful GET/PUT/PATCH request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource (e.g., category name)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Architecture

The application follows a layered architecture:

1. **API Layer** (`app/api/`): Handles HTTP requests/responses
2. **Service Layer** (`app/services/`): Contains business logic
3. **Repository Layer** (`app/repositories/`): Manages data access
4. **Models** (`app/models/`): Database schema definitions
5. **Schemas** (`app/schemas/`): Request/response validation

This separation ensures:
- **Maintainability**: Clear separation of concerns
- **Testability**: Easy to test each layer independently
- **Scalability**: Simple to add new features
- **Reusability**: Business logic can be reused across endpoints

## Production Deployment

For production deployment:

1. **Set DEBUG to False** in `.env`:
   ```env
   DEBUG=False
   ```

2. **Use PostgreSQL** instead of SQLite:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/taskflow
   ```

3. **Run with Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Set up proper CORS origins**:
   ```env
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

## License

This project is part of the TaskFlow productivity application.

## Support

For issues or questions, please refer to the project documentation or create an issue in the repository.
