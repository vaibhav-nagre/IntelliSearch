#!/bin/bash

# ✨ IntelliSearch Enterprise - Simple Start Script
# Created by Vaibhav Nagre - Full-Stack Developer & AI Enthusiast
# AI-Powered Enterprise Search Platform with Real-time Content Scraping

set -e

echo "🚀 Starting IntelliSearch Enterprise Application"
echo "👨‍💻 Created by Vaibhav Nagre - https://github.com/vaibhavnagre"
echo "🔍 AI-Powered Enterprise Search Platform"
echo ""

# Function to start backend with minimal dependencies
start_backend_simple() {
    echo "🐍 Starting FastAPI backend (simple mode)..."
    cd backend
    
    # Activate existing virtual environment
    if [ -f "../.venv/bin/activate" ]; then
        source ../.venv/bin/activate
    else
        echo "❌ Virtual environment not found. Please run: python3 -m venv .venv"
        exit 1
    fi
    
    # Install only essential dependencies
    echo "📦 Installing essential backend dependencies..."
    pip install fastapi uvicorn pydantic-settings python-dotenv
    
    # Create a minimal .env if it doesn't exist
    if [ ! -f .env ]; then
        echo "⚠️  Creating minimal .env file..."
        cat > .env << EOF
APP_NAME="IntelliSearch Enterprise"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=True
AWS_REGION="us-east-1"
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]
EOF
    fi
    
    # Start the server
    echo "🌐 Starting server on http://localhost:8000"
    uvicorn app.main_simple:app --host 0.0.0.0 --port 8000 --reload
}

# Function to start frontend
start_frontend() {
    echo "⚛️  Starting Next.js frontend..."
    cd frontend
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    # Start development server
    echo "🌐 Starting frontend on http://localhost:3000"
    npm run dev
}

# Parse command line arguments
case "$1" in
    "backend")
        start_backend_simple
        ;;
    "frontend")
        start_frontend
        ;;
    "simple"|"dev"|"")
        echo "🔄 Starting both frontend and backend (simple mode)..."
        
        # Start backend in background
        start_backend_simple &
        BACKEND_PID=$!
        
        # Wait a bit for backend to start
        sleep 3
        
        # Start frontend
        start_frontend &
        FRONTEND_PID=$!
        
        # Function to cleanup background processes
        cleanup() {
            echo "🛑 Stopping services..."
            kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
            exit 0
        }
        
        # Set trap to cleanup on exit
        trap cleanup SIGINT SIGTERM
        
        # Wait for both processes
        wait
        ;;
    *)
        echo "Usage: $0 [backend|frontend|simple|dev]"
        echo "  backend  - Start only the FastAPI backend (simple mode)"
        echo "  frontend - Start only the Next.js frontend"
        echo "  simple   - Start both with minimal dependencies (recommended)"
        echo "  dev      - Same as simple (default)"
        exit 1
        ;;
esac
