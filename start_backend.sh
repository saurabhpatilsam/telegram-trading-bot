#!/bin/bash

echo "🚀 Starting Telegram Trading Bot Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r backend_requirements.txt -q

# Initialize database
echo "Initializing database..."
python3 -c "from database import init_db; init_db()"

# Start the API server
echo ""
echo "✅ Starting API server on http://localhost:8000"
echo "📊 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 api_server.py
