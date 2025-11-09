#!/bin/bash

# TaskFlow API - Development Server Launcher

echo "Starting TaskFlow API..."
echo "========================"
echo ""
echo "API will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the application
python -m app.main
