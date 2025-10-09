#!/bin/bash

# Simple OEE Co-Pilot Frontend Startup Script
echo "🚀 Starting Simple OEE Co-Pilot Frontend..."

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Backend is not running on http://localhost:8000"
    echo "Please start the backend first with: python main.py"
    echo ""
    echo "Continuing with frontend startup..."
fi

echo "🎨 Starting simple frontend server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the simple frontend server
python3 serve_simple_frontend.py

