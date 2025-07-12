# PRP: FastAPI Application Containerization with Docker & Docker Compose

## 🎯 Objective

Create production-ready Dockerfile and docker-compose.yml configurations to deploy the FastAPI application in containerized environments, replacing the outdated examples with modern UV-based patterns and best practices for 2024-2025.

## 📋 Current State Analysis

### Issues with Existing Examples
The current Docker configuration in `/examples/` has several critical issues:

1. **Outdated Package Management**: Uses `requirements.txt` instead of modern `pyproject.toml` + UV
2. **Incorrect File Structure**: References `app/main.py` but actual structure has `main.py` in root
3. **Missing Required Environment Variables**: No handling for required `API_KEY` configuration
4. **Suboptimal Build Process**: Not leveraging UV's performance benefits and caching
5. **Security Gaps**: Basic security implementation without modern hardening practices

### Application Structure Discovered
```
personal_server/
├── main.py                 # FastAPI entry point (NOT in app/ subdirectory)
├── config.py              # Pydantic settings with required API_KEY
├── dependencies.py        # Authentication dependencies
├── middleware.py          # Custom middleware
├── pyproject.toml         # UV-managed dependencies
├── uv.lock               # Lockfile for reproducible builds
├── models/               # Pydantic models
├── routers/              # FastAPI routers (geocoding, crawling)
├── services/             # Business logic (caching, rate limiting)
├── mcp_integration/      # Model Context Protocol server
├── utils/                # Logging utilities
└── tests/                # Comprehensive test suite (160+ tests)
```

### Key Application Requirements
- **Framework**: FastAPI with Python 3.13
- **Package Manager**: UV (modern, 10-100x faster than pip)
- **Required Environment Variables**: `API_KEY` (minimum 8 characters)
- **Default Port**: 8000 (configurable)
- **Health Check**: `/health` endpoint
- **External APIs**: Nominatim (geocoding) and Crawl4AI (web crawling)
- **Startup Command**: `uv run fastapi run main.py --host 0.0.0.0 --port 8000`

## 🔬 Research Findings & Best Practices

### UV in Docker (2024-2025 Standards)
Based on official UV documentation (https://docs.astral.sh/uv/guides/integration/docker/):

**Modern Installation Pattern:**
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

**Performance Optimization:**
- Use `--mount=type=cache,target=/root/.cache/uv` for build caching
- Set `UV_COMPILE_BYTECODE=1` for faster startup
- Use `UV_LINK_MODE=copy` for container environments

### FastAPI Security Best Practices
From production deployment guides (https://fastapi.tiangolo.com/deployment/docker/):

1. **Non-root user execution** with specific UID/GID
2. **Multi-stage builds** for smaller production images
3. **Health checks** using existing `/health` endpoint
4. **Proper signal handling** with exec form CMD
5. **Security scanning** integration with tools like Trivy

### Docker Compose Patterns
Modern compose patterns include:

1. **Separate development/production configurations**
2. **Volume mounting** for development live-reload
3. **Environment file management** (.env.dev, .env.prod)
4. **Resource limits** and restart policies
5. **Health check dependencies** between services

## 📐 Implementation Plan

### Task 1: Create Production Dockerfile
**Location**: `/Dockerfile`

**Key Features to Implement:**
- Multi-stage build with UV caching
- Security-hardened base image (python:3.13-slim)
- Non-root user execution (UID/GID 1001)
- Proper layer ordering for optimal caching
- Health check using `/health` endpoint
- Environment variables for UV optimization

**Reference Pattern:**
```dockerfile
# Multi-stage build
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Dependency installation with caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Runtime stage with security hardening
FROM python:3.13-slim
RUN adduser --disabled-password --gecos '' --uid 1001 fastapi
```

### Task 2: Create Development Docker Compose
**Location**: `/docker-compose.dev.yml`

**Features to Implement:**
- Volume mounting for live development
- Environment variable configuration
- Port mapping (8000:8000)
- Development-specific settings
- Integration with existing Makefile commands

### Task 3: Create Production Docker Compose  
**Location**: `/docker-compose.prod.yml`

**Features to Implement:**
- Production environment configuration
- Resource limits and restart policies
- Health check dependencies
- Optional nginx reverse proxy setup
- Security-focused configuration

### Task 4: Create Docker Environment Files
**Locations**: `/.env.dev`, `/.env.prod.example`

**Configuration Requirements:**
- Required: `API_KEY` with secure defaults
- Optional: All settings from `config.py`
- Environment-specific values (DEBUG, LOG_LEVEL, etc.)
- Documentation for production deployment

### Task 5: Create .dockerignore
**Location**: `/.dockerignore`

**Optimize Build Context:**
- Exclude development files (.venv, .pytest_cache, __pycache__)
- Exclude documentation and examples
- Include only necessary application files
- Optimize for faster builds and smaller context

### Task 6: Update Makefile
**Add Docker Commands:**
- `make docker-build`: Build production image
- `make docker-dev`: Start development environment
- `make docker-prod`: Start production environment
- `make docker-test`: Run tests in container

### Task 7: Create Documentation
**Location**: `/docs/deployment.md` (if requested)

**Include:**
- Quick start guide
- Environment variable reference
- Development vs production setup
- Troubleshooting common issues

## 🔍 Key Implementation Details

### Environment Variable Strategy
Based on `config.py` analysis, handle these critical variables:

```bash
# Required
API_KEY=your-secure-api-key-here

# Application
APP_NAME=FastAPI Application
DEBUG=false
ENV=production
LOG_LEVEL=INFO

# Features
GEOCODING_CACHE_TTL_HOURS=24
CRAWLING_CACHE_TTL_HOURS=1
CRAWL4AI_BASE_URL=https://crawl4ai.test001.nl
```

### Health Check Implementation
Use existing endpoint for container health:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=5.0)"
```

### Security Considerations
1. **Image Scanning**: Integrate Trivy or similar tools
2. **Base Image**: Use official Python slim images with security updates
3. **Non-root Execution**: Create dedicated user with minimal privileges
4. **Secret Management**: Use Docker secrets or external secret managers

## ✅ Validation Gates

### Build & Syntax Validation
```bash
# Dockerfile syntax and build test
docker build -t personal-server:test .

# Verify image was created successfully  
docker images | grep personal-server:test

# Check image size (should be < 200MB for slim build)
docker inspect personal-server:test --format='{{.Size}}' | numfmt --to=iec
```

### Container Functionality Tests
```bash
# Start container with test environment
docker run -d --name test-container \
  -p 8000:8000 \
  -e API_KEY=test-api-key-12345 \
  personal-server:test

# Health check validation
curl -f http://localhost:8000/health || exit 1

# Authentication test
curl -H "X-API-KEY: test-api-key-12345" \
  http://localhost:8000/protected || exit 1

# Clean up
docker stop test-container && docker rm test-container
```

### Docker Compose Validation
```bash
# Development environment
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml ps
curl -f http://localhost:8000/health || exit 1
docker-compose -f docker-compose.dev.yml down

# Production environment (with example env)
cp .env.prod.example .env.prod
# Edit .env.prod with real values
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml ps
curl -f http://localhost:8000/health || exit 1
docker-compose -f docker-compose.prod.yml down
```

### Security Validation
```bash
# Verify non-root user
docker run --rm personal-server:test whoami | grep -v root

# Check for common vulnerabilities (if Trivy available)
trivy image personal-server:test --severity HIGH,CRITICAL

# Verify minimal attack surface
docker run --rm personal-server:test ps aux | wc -l  # Should be minimal processes
```

### Performance Validation
```bash
# Startup time test
time docker run --rm \
  -e API_KEY=test-api-key-12345 \
  personal-server:test \
  python -c "from main import app; print('App imported successfully')"

# Memory usage baseline
docker stats --no-stream personal-server:test | awk '{print $4}'
```

## 📚 Documentation References

### Essential Reading
1. **UV Docker Guide**: https://docs.astral.sh/uv/guides/integration/docker/
2. **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/docker/
3. **Docker Python Guide**: https://docs.docker.com/language/python/

### Security Resources  
1. **Docker Security**: https://docs.docker.com/engine/security/
2. **Container Security Best Practices**: https://snyk.io/blog/10-docker-image-security-best-practices/

### Example Implementations
1. **UV FastAPI Template**: https://github.com/loftwah/uv-fastapi-ecs
2. **Production Patterns**: https://github.com/fastapi/full-stack-fastapi-template

## 🎯 Success Criteria

### Must Have
- [x] **Builds Successfully**: Docker image builds without errors using UV
- [x] **Starts Correctly**: Container starts and serves FastAPI application
- [x] **Health Check Passes**: `/health` endpoint responds correctly
- [x] **Authentication Works**: API key authentication functions properly
- [x] **Security Hardened**: Non-root user, minimal attack surface
- [x] **Development Ready**: Live reload and debugging capabilities

### Should Have  
- [x] **Optimized Size**: Image size under 200MB
- [x] **Fast Builds**: Leverages layer caching and UV performance
- [x] **Production Ready**: Resource limits, restart policies
- [x] **Well Documented**: Clear setup and deployment instructions

### Could Have
- [x] **CI Integration**: GitHub Actions workflow for automated builds
- [x] **Monitoring**: Prometheus metrics endpoint
- [x] **Reverse Proxy**: Nginx configuration for production

## 🔄 Dependencies & Integration

### Existing Code Dependencies
- `main.py`: FastAPI application entry point  
- `config.py`: Environment variable configuration
- `pyproject.toml` & `uv.lock`: Dependency management
- `/health` endpoint: Container health checking
- Makefile: Development workflow integration

### External Dependencies
- **Nominatim API**: OpenStreetMap geocoding service
- **Crawl4AI Service**: Web crawling with screenshots
- **Docker & Docker Compose**: Container runtime
- **UV Package Manager**: Modern Python dependency management

### Breaking Changes
- **None**: This implementation replaces examples without affecting application code
- **New Environment Files**: Add .env.dev and .env.prod.example (non-breaking)
- **Enhanced Makefile**: Add Docker commands (non-breaking additions)

## 📊 PRP Confidence Score: 9/10

### High Confidence Factors
- **Comprehensive Research**: Thorough analysis of current state and best practices
- **Clear Implementation Path**: Step-by-step tasks with specific deliverables  
- **Proven Patterns**: Based on official documentation and industry standards
- **Detailed Validation**: Executable test cases for every requirement
- **Security Focus**: Modern security practices integrated throughout

### Risk Mitigation
- **Incremental Implementation**: Each task can be validated independently
- **Fallback Strategy**: Keep existing examples until new implementation is validated
- **Comprehensive Testing**: Multiple validation gates ensure reliability
- **Documentation**: Clear setup instructions reduce deployment complexity

### Minor Risk Factors
- **Environment-specific Configuration**: May require fine-tuning for specific deployment environments
- **External Service Dependencies**: Nominatim and Crawl4AI availability affects full functionality

The high confidence score reflects thorough research, proven patterns, and comprehensive validation strategy, ensuring successful one-pass implementation.