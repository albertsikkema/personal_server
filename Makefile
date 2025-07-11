# FastAPI Project Makefile
# Common commands for development workflow

.PHONY: help install run dev test lint format check clean setup sync check-commit security

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
	@echo "  lint      - Run linter (ruff check)"
	@echo "  format    - Format code with ruff"
	@echo "  check     - Run linter and formatter check"
	@echo "  fix       - Auto-fix linting issues and format code"
	@echo "  quality   - Run complete code quality workflow"
	@echo "  check-commit - Run quality checks without fixes (CI-safe)"
	@echo "  security  - Run security scans (safety, bandit, semgrep)"
	@echo "  clean     - Clean up cache and temporary files"

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

# Run tests
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

# Security scanning
security:
	@echo "Running security scans..."
	uv add --dev safety bandit semgrep
	uv run safety check --json --output security-report.json
	uv run bandit -r . -f json -o bandit-report.json -x tests/
	uv run semgrep --config=auto --json --output=semgrep-report.json

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