# Makefile for Saviynt Enterprise Search Platform

.PHONY: help install-frontend install-backend install dev-frontend dev-backend dev build test clean docker-build docker-run deploy-frontend deploy-backend setup-db migrate crawl

# Default target
help:
	@echo "Saviynt Enterprise Search Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  install          Install all dependencies"
	@echo "  install-frontend Install frontend dependencies"
	@echo "  install-backend  Install backend dependencies"
	@echo "  dev              Start development servers"
	@echo "  dev-frontend     Start frontend development server"
	@echo "  dev-backend      Start backend development server"
	@echo "  build            Build all components"
	@echo "  test             Run all tests"
	@echo "  clean            Clean build artifacts"
	@echo "  setup-db         Setup database and run migrations"
	@echo "  migrate          Run database migrations"
	@echo "  crawl            Trigger data crawling"
	@echo "  docker-build     Build Docker images"
	@echo "  docker-run       Run with Docker Compose"
	@echo "  deploy-frontend  Deploy frontend to GitHub Pages"
	@echo "  deploy-backend   Deploy backend to GCP Cloud Run"

# Installation
install: install-frontend install-backend

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && python -m pip install -r requirements.txt

# Development
dev:
	@echo "Starting development servers..."
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Backend will be available at http://localhost:8000"
	@echo "Press Ctrl+C to stop both servers"
	$(MAKE) -j2 dev-frontend dev-backend

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Building
build: build-frontend build-backend

build-frontend:
	@echo "Building frontend..."
	cd frontend && npm run build && npm run export

build-backend:
	@echo "Building backend..."
	cd backend && python -m pip install -e .

# Testing
test: test-frontend test-backend

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test

test-backend:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v

# Database operations
setup-db:
	@echo "Setting up database..."
	cd backend && python -c "from app.database import create_tables; create_tables()"

migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

# Data operations
crawl:
	@echo "Triggering data crawling..."
	cd backend && python -m app.ingestion.runner --sources forums,docs,freshservice

# Docker operations
docker-build:
	@echo "Building Docker images..."
	docker build -t saviynt-search-backend ./backend
	docker build -t saviynt-search-frontend ./frontend

docker-run:
	@echo "Starting services with Docker Compose..."
	docker-compose up -d

docker-stop:
	@echo "Stopping Docker services..."
	docker-compose down

# Deployment
deploy-frontend:
	@echo "Deploying frontend to GitHub Pages..."
	cd frontend && npm run build && npm run export
	@echo "Upload the 'out' directory to GitHub Pages"

deploy-backend:
	@echo "Deploying backend to GCP Cloud Run..."
	cd backend && gcloud builds submit --tag gcr.io/$(GOOGLE_CLOUD_PROJECT)/saviynt-search
	gcloud run deploy saviynt-search \
		--image gcr.io/$(GOOGLE_CLOUD_PROJECT)/saviynt-search \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated

# Infrastructure
infra-plan:
	@echo "Planning infrastructure changes..."
	cd infra && terraform plan

infra-apply:
	@echo "Applying infrastructure changes..."
	cd infra && terraform apply

infra-destroy:
	@echo "Destroying infrastructure..."
	cd infra && terraform destroy

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	cd frontend && rm -rf .next out node_modules/.cache
	cd backend && find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -name "*.pyc" -delete
	docker system prune -f

# Development utilities
format:
	@echo "Formatting code..."
	cd frontend && npm run format
	cd backend && black . && isort .

lint:
	@echo "Linting code..."
	cd frontend && npm run lint
	cd backend && flake8 . && mypy .

# Environment setup
env-check:
	@echo "Checking environment configuration..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Copy .env.example to .env and configure it."; \
		exit 1; \
	fi
	@echo "✅ Environment configuration found"

# Health checks
health-check:
	@echo "Checking service health..."
	@curl -f http://localhost:8000/healthz || echo "❌ Backend health check failed"
	@curl -f http://localhost:3000 || echo "❌ Frontend health check failed"

# Logs
logs-backend:
	@echo "Showing backend logs..."
	cd backend && tail -f logs/app.log

logs-frontend:
	@echo "Showing frontend logs..."
	cd frontend && npm run logs

# Database utilities
db-reset:
	@echo "Resetting database..."
	cd backend && python -c "from app.database import reset_database; reset_database()"

db-seed:
	@echo "Seeding database with sample data..."
	cd backend && python -m app.database.seed

# Monitoring
metrics:
	@echo "Opening metrics dashboard..."
	open http://localhost:9090  # Prometheus
	open http://localhost:3001  # Grafana

# Security
security-scan:
	@echo "Running security scans..."
	cd frontend && npm audit
	cd backend && safety check

# Quick setup for new developers
quick-start: env-check install setup-db build
	@echo ""
	@echo "🎉 Setup complete! Run 'make dev' to start development servers."
	@echo ""
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
