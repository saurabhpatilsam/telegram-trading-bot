#!/bin/bash

echo "🎨 Starting Telegram Trading Bot Frontend..."
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "✅ Starting React app on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm run dev
