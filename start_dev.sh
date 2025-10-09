#!/bin/bash

# OEE Co-Pilot Development Startup Script
echo "🚀 Starting OEE Co-Pilot Development Environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please create one first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one with your API keys:"
    echo "   DB_HOST=localhost"
    echo "   DB_USER=root"
    echo "   DB_PASSWORD=your_password"
    echo "   DB_NAME=MiningandFactoryData"
    echo "   DB_PORT=3307"
    echo "   GOOGLE_API_KEY=your_google_api_key"
    echo "   PINECONE_API_KEY=your_pinecone_api_key"
    exit 1
fi

# Start backend in background
echo "🔧 Starting FastAPI backend..."
python main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend failed to start. Check the logs above."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend is running on http://localhost:8000"

# Start frontend
echo "🎨 Starting Angular frontend..."
cd ops-copilot-frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🌐 Starting Angular development server..."
echo "   Frontend will be available at http://localhost:4200"
echo "   Backend API is available at http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Start frontend
npm start &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
