#!/bin/bash

# OEE Co-Pilot Frontend Development Server
echo "🚀 Starting OEE Co-Pilot Frontend Development Server..."

# Check if we're in the right directory
if [ ! -d "ops-copilot-frontend" ]; then
    echo "❌ Error: ops-copilot-frontend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Navigate to frontend directory
cd ops-copilot-frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Backend is not running on http://localhost:8000"
    echo "Please start the backend first with: python main.py"
    echo "Or run: ./start_dev.sh"
    echo ""
    echo "Continuing with frontend startup..."
fi

echo "🎨 Starting Angular development server..."
echo "Frontend will be available at: http://localhost:4200"
echo "Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Angular development server using npm
# This will use the locally installed Angular CLI from node_modules
npm start
