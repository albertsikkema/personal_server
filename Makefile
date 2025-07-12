# FastAPI Project Makefile
# Common commands for development workflow

.PHONY: help install run dev test lint format check clean setup sync check-commit security docker-build docker-dev docker-prod docker-test docker-clean docker-logs docker-logs-dev docker-logs-prod docker-ps docker-stop docker-restart docker-shell docker-health

# Default target
help:
	@echo "Available commands:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  install   - Install dependencies (alias for sync)"
	@echo "  sync      - Sync dependencies with uv"
	@echo "  run       - Start FastAPI development server"
	@echo "  dev       - Start FastAPI development server (alias for run)"
	@echo "  test      - Run all tests"
	@echo "  test-cov  - Run tests with coverage report"
	@echo "  test-ci   - Run tests with separate database (CI simulation)"
	@echo "  lint      - Run linter (ruff check)"
	@echo "  format    - Format code with ruff"
	@echo "  check     - Run linter and formatter check"
	@echo "  fix       - Auto-fix linting issues and format code"
	@echo "  quality   - Run complete code quality workflow"
	@echo "  check-commit - Run quality checks without fixes (CI-safe)"
	@echo "  security  - Run security scans (safety, bandit, semgrep)"
	@echo "  clean     - Clean up cache and temporary files"
	@echo ""
	@echo "Docker commands:"
	@echo "  docker-build    - Build production Docker image"
	@echo "  docker-dev      - Start development environment with Docker Compose"
	@echo "  docker-prod     - Start production environment with Docker Compose"
	@echo "  docker-test     - Run tests in Docker container"
	@echo "  docker-clean    - Clean up Docker containers and images"
	@echo ""
	@echo "Docker Compose management:"
	@echo "  docker-logs     - Show logs from running containers"
	@echo "  docker-logs-dev - Show logs from development environment"
	@echo "  docker-logs-prod - Show logs from production environment"
	@echo "  docker-ps       - Show status of all containers"
	@echo "  docker-stop     - Stop all running containers"
	@echo "  docker-restart  - Restart containers"
	@echo "  docker-shell    - Open shell in running container"
	@echo "  docker-health   - Check health status of containers"

# Complete setup from scratch
setup: 
	@echo "Setting up the project..."
	@echo "Creating virtual environment and installing dependencies..."
	uv sync
	@echo "Setup complete! Run 'make run' to start the server"

# Sync dependencies
sync:
	uv sync

# Install dependencies (alias for sync)
install: sync

# Start FastAPI development server
run:
	uv run fastapi dev main.py

# Alias for run
dev: run

# Run tests (automatically sets up test database)
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=. --cov-report=term-missing

# Run linter
lint:
	uv run ruff check .

# Format code
format:
	uv run ruff format .

# Check formatting without making changes
check:
	uv run ruff check .
	uv run ruff format --check .

# Auto-fix linting issues and format code
fix:
	uv run ruff check --fix .
	uv run ruff format .

# Complete code quality workflow
quality: fix test
	@echo "Code quality check complete!"

# Clean up cache and temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "Cleaned up cache and temporary files"

# Update dependencies
update:
	uv sync --upgrade

# Check code quality without making changes (CI-safe)
check-commit: check test
	@echo "Code quality check complete (no fixes applied)!"

# Test with separate database (like CI) - now same as regular test
test-ci: test
	@echo "CI test simulation complete (uses same database setup as regular tests)!"

# Security scanning
security:
	@echo "Running security scans..."
	uv add --dev pip-audit bandit
	uv run pip-audit --format=json --output=security-report.json
	uv run bandit -r . -f json -o bandit-report.json -x tests/,.venv/,personal_server.egg-info/ || true

# Test MCP server
test-mcp:
	uv run python -c "import asyncio; from fastmcp import Client; \
	async def test(): \
		async with Client('http://localhost:8000/mcp-server/mcp') as client: \
			tools = await client.list_tools(); \
			print(f'Available tools: {[tool.name for tool in tools]}'); \
			result = await client.call_tool('geocode_city', {'city': 'London'}); \
			print(f'Result: {result}'); \
	asyncio.run(test())"

# Docker Commands

# Build production Docker image
docker-build:
	@echo "Building production Docker image..."
	docker build -t personal-server:latest .
	@echo "Docker image built successfully!"
	@echo "Image size:"
	@docker images personal-server:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Start development environment with Docker Compose
docker-dev:
	@echo "Starting development environment..."
	@if [ ! -f .env.dev ]; then \
		echo "Warning: .env.dev not found. Creating from template..."; \
		cp .env.dev .env.dev 2>/dev/null || echo "Please create .env.dev file"; \
	fi
	docker compose -f docker-compose.dev.yml up --build

# Start production environment with Docker Compose
docker-prod:
	@echo "Starting production environment..."
	@if [ ! -f .env.prod ]; then \
		echo "Error: .env.prod not found. Please copy .env.prod.example to .env.prod and configure it."; \
		echo "Run: cp .env.prod.example .env.prod"; \
		exit 1; \
	fi
	docker compose -f docker-compose.prod.yml up --build -d
	@echo "Production environment started in background"
	@echo "Check status with: docker compose -f docker-compose.prod.yml ps"

# Run tests in Docker container
docker-test:
	@echo "Running tests in Docker container..."
	docker build -t personal-server:test .
	docker run --rm \
		-e API_KEY=test-api-key-12345678 \
		-e ENV=development \
		personal-server:test \
		pytest -v

# Clean up Docker containers and images
docker-clean:
	@echo "Cleaning up Docker containers and images..."
	docker compose -f docker-compose.dev.yml down --remove-orphans 2>/dev/null || true
	docker compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true
	docker rmi personal-server:latest personal-server:test 2>/dev/null || true
	docker system prune -f
	@echo "Docker cleanup complete!"

# Docker Compose Management Commands

# Show logs from running containers (auto-detect environment)
docker-logs:
	@if docker compose -f docker-compose.dev.yml ps --quiet 2>/dev/null | grep -q .; then \
		echo "Showing development environment logs:"; \
		docker compose -f docker-compose.dev.yml logs -f; \
	elif docker compose -f docker-compose.prod.yml ps --quiet 2>/dev/null | grep -q .; then \
		echo "Showing production environment logs:"; \
		docker compose -f docker-compose.prod.yml logs -f; \
	else \
		echo "No running containers found. Start an environment first:"; \
		echo "  make docker-dev   (for development)"; \
		echo "  make docker-prod  (for production)"; \
	fi

# Show logs from development environment
docker-logs-dev:
	@echo "Showing development environment logs..."
	docker compose -f docker-compose.dev.yml logs -f

# Show logs from production environment
docker-logs-prod:
	@echo "Showing production environment logs..."
	docker compose -f docker-compose.prod.yml logs -f

# Show status of all containers
docker-ps:
	@echo "=== Development Environment ==="
	@docker compose -f docker-compose.dev.yml ps 2>/dev/null || echo "Development environment not running"
	@echo ""
	@echo "=== Production Environment ==="
	@docker compose -f docker-compose.prod.yml ps 2>/dev/null || echo "Production environment not running"
	@echo ""
	@echo "=== All Docker Containers ==="
	@docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Stop all running containers
docker-stop:
	@echo "Stopping all containers..."
	@docker compose -f docker-compose.dev.yml down 2>/dev/null || true
	@docker compose -f docker-compose.prod.yml down 2>/dev/null || true
	@echo "All containers stopped"

# Restart containers (auto-detect environment)
docker-restart:
	@if docker compose -f docker-compose.dev.yml ps --quiet 2>/dev/null | grep -q .; then \
		echo "Restarting development environment..."; \
		docker compose -f docker-compose.dev.yml restart; \
	elif docker compose -f docker-compose.prod.yml ps --quiet 2>/dev/null | grep -q .; then \
		echo "Restarting production environment..."; \
		docker compose -f docker-compose.prod.yml restart; \
	else \
		echo "No running containers found to restart"; \
		echo "Start an environment first with 'make docker-dev' or 'make docker-prod'"; \
	fi

# Open shell in running container
docker-shell:
	@if docker compose -f docker-compose.dev.yml ps --quiet fastapi 2>/dev/null | grep -q .; then \
		echo "Opening shell in development container..."; \
		docker compose -f docker-compose.dev.yml exec fastapi /bin/bash; \
	elif docker compose -f docker-compose.prod.yml ps --quiet fastapi 2>/dev/null | grep -q .; then \
		echo "Opening shell in production container..."; \
		docker compose -f docker-compose.prod.yml exec fastapi /bin/bash; \
	else \
		echo "No running FastAPI container found"; \
		echo "Start an environment first with 'make docker-dev' or 'make docker-prod'"; \
	fi

# Check health status of containers
docker-health:
	@echo "=== Container Health Status ==="
	@docker ps --format "table {{.Names}}\t{{.Status}}" --filter "name=personal_server" 2>/dev/null || echo "No containers running"
	@echo ""
	@echo "=== Health Check Endpoints ==="
	@if docker compose -f docker-compose.dev.yml ps --quiet fastapi 2>/dev/null | grep -q .; then \
		echo "Development environment:"; \
		sleep 5; \
		curl -s http://localhost:8000/health | python3 -m json.tool || echo "Health endpoint not accessible - container may still be starting"; \
	fi
	@if docker compose -f docker-compose.prod.yml ps --quiet fastapi 2>/dev/null | grep -q .; then \
		echo "Production environment:"; \
		sleep 2; \
		curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Health endpoint not accessible - container may still be starting"; \
	fi