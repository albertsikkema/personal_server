# FastAPI Project Makefile
# Common commands for development workflow

.PHONY: help install run dev test lint format check clean setup venv

# Default target
help:
	@echo "Available commands:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  install   - Install dependencies"
	@echo "  run       - Start FastAPI development server"
	@echo "  dev       - Start FastAPI development server (alias for run)"
	@echo "  test      - Run all tests"
	@echo "  test-cov  - Run tests with coverage report"
	@echo "  lint      - Run linter (ruff check)"
	@echo "  format    - Format code with ruff"
	@echo "  check     - Run linter and formatter check"
	@echo "  fix       - Auto-fix linting issues and format code"
	@echo "  quality   - Run complete code quality workflow"
	@echo "  clean     - Clean up cache and temporary files"
	@echo "  venv      - Create virtual environment"

# Virtual environment creation
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

# Complete setup from scratch
setup: 
	@echo "Setting up the project..."
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt
	@echo "Setup complete! Run 'make run' to start the server"

# Install dependencies
install:
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt

# Start FastAPI development server
run:
	source venv/bin/activate && fastapi dev main.py

# Alias for run
dev: run

# Run tests
test:
	source venv/bin/activate && pytest

# Run tests with coverage
test-cov:
	source venv/bin/activate && pytest --cov=. --cov-report=term-missing

# Run linter
lint:
	source venv/bin/activate && ruff check .

# Format code
format:
	source venv/bin/activate && ruff format .

# Check formatting without making changes
check:
	source venv/bin/activate && ruff check .
	source venv/bin/activate && ruff format --check .

# Auto-fix linting issues and format code
fix:
	source venv/bin/activate && ruff check --fix .
	source venv/bin/activate && ruff format .

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

# Production commands
freeze:
	source venv/bin/activate && pip freeze > requirements.txt

# Update dependencies
update:
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install --upgrade -r requirements.txt
	$(MAKE) freeze