#!/bin/bash

# Start script for Saviynt Enterprise Search
set -e

echo "🚀 Starting Saviynt Enterprise Search Application"

# Check if .env file exists
if [ ! -f backend/.env ]; then
    echo "⚠️  Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "📝 Please update backend/.env with your AWS credentials and other settings"
fi

# Function to start backend
start_backend() {
    echo "🐍 Starting FastAPI backend..."
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "📦 Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Start the server
    echo "🌐 Starting server on http://localhost:8000"
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to start frontend
start_frontend() {
    echo "⚛️  Starting Next.js frontend..."
    cd frontend
    
    # Install dependencies
    echo "📦 Installing frontend dependencies..."
    npm install
    
    # Start development server
    echo "🌐 Starting frontend on http://localhost:3000"
    npm run dev
}

# Parse command line arguments
case "$1" in
    "backend")
        start_backend
        ;;
    "frontend")
        start_frontend
        ;;
    "dev"|"")
        echo "🔄 Starting both frontend and backend..."
        
        # Start backend in background
        start_backend &
        BACKEND_PID=$!
        
        # Wait a bit for backend to start
        sleep 3
        
        # Start frontend
        start_frontend &
        FRONTEND_PID=$!
        
        # Wait for both processes
        wait $BACKEND_PID $FRONTEND_PID
        ;;
    *)
        echo "Usage: $0 [backend|frontend|dev]"
        echo "  backend  - Start only the FastAPI backend"
        echo "  frontend - Start only the Next.js frontend"
        echo "  dev      - Start both (default)"
        exit 1
        ;;
esac
