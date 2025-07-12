# Multi-stage build for FastAPI application with UV package manager
# Based on official UV documentation: https://docs.astral.sh/uv/guides/integration/docker/

# Build stage
FROM python:3.13-slim AS builder

# Install UV from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Set environment variables for UV optimization
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files first for optimal layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount for faster builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

# Copy application source code
COPY . .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Runtime stage with security hardening
FROM python:3.13-slim

# Install curl for health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user with specific UID/GID for security
RUN groupadd -r fastapi --gid=1001 && \
    useradd -r -g fastapi --uid=1001 --home-dir=/app --shell=/bin/bash fastapi

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app .

# Set ownership to non-root user
RUN chown -R fastapi:fastapi /app

# Set environment variables for runtime
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/app/.venv"

# Switch to non-root user
USER fastapi

# Expose port
EXPOSE 8000

# Health check using existing /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use exec form for proper signal handling
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]