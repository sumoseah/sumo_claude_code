# TaskFlow API - Quick Start Guide

Get the TaskFlow API up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher installed
- pip (Python package manager)

## Installation (3 steps)

### 1. Set up virtual environment

```bash
cd /Users/linus/taskflow-app/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
python -m app.main
```

Or use the convenience script:

```bash
./run.sh
```

## Access the API

Once running, open your browser to:

- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## Try It Out

### Using the Interactive Docs (Easiest)

1. Go to http://localhost:8000/docs
2. Click on any endpoint (e.g., "POST /api/categories")
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

### Using cURL

Create a category:
```bash
curl -X POST "http://localhost:8000/api/categories" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#3B82F6"}'
```

Create a task:
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "My first task", "priority": "high"}'
```

Get all tasks:
```bash
curl "http://localhost:8000/api/tasks"
```

## Run Tests

```bash
pytest
```

## Project Structure

```
backend/
├── app/                    # Main application code
│   ├── api/               # API endpoints
│   ├── core/              # Configuration & database
│   ├── models/            # Database models
│   ├── schemas/           # Request/response validation
│   ├── services/          # Business logic
│   └── repositories/      # Data access
├── tests/                 # Test suite
├── requirements.txt       # Dependencies
└── README.md             # Full documentation
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API_EXAMPLES.md](API_EXAMPLES.md) for more usage examples
- Explore the interactive docs at http://localhost:8000/docs
- Run the test suite: `pytest`
- Start building your frontend!

## Common Commands

```bash
# Start the server
python -m app.main

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type check
mypy app/
```

## Troubleshooting

### Port already in use

Change the port in `.env`:
```env
PORT=8001
```

### Import errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Database issues

Delete the database file and restart:
```bash
rm taskflow.db
python -m app.main
```

## Configuration

Edit the `.env` file to customize:

```env
DATABASE_URL=sqlite:///./taskflow.db
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Support

For more information, see:
- [README.md](README.md) - Full documentation
- [API_EXAMPLES.md](API_EXAMPLES.md) - API usage examples
- http://localhost:8000/docs - Interactive API documentation

Happy coding!
