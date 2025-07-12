# Claude.md - Project Documentation Reference

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Principles

KISS (Keep It Simple, Stupid): Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

YAGNI (You Aren't Gonna Need It): Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

Dependency Inversion: High-level modules should not depend on low-level modules. Both should depend on abstractions. This principle enables flexibility and testability.

Open/Closed Principle: Software entities should be open for extension but closed for modification. Design your systems so that new functionality can be added with minimal changes to existing code.

## 🤖 AI Assistant Guidelines

### Context Awareness

- When implementing features, always check existing patterns first
- Prefer composition over inheritance in all designs
- Use existing utilities before creating new ones
- Check for similar functionality in other domains/features

### Common Pitfalls to Avoid

- Creating duplicate functionality
- Overwriting existing tests
- Modifying core frameworks without explicit instruction
- Adding dependencies without checking existing alternatives

### Workflow Patterns

- Preferably create tests BEFORE implementation (TDD, Test Driven Development)
- Use "think hard" for architecture decisions
- Break complex tasks into smaller, testable units
- Validate understanding before implementation

## 🧱 Code Structure & Modularity

- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Functions should be short and focused sub 50 lines of code** and have a single responsibility.
- **Classes should be short and focused sub 50 lines of code** and have a single responsibility.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.

## Architecture

Strict vertical slice architecture with tests that live next to the code they test.

```
src/project/
    __init__.py
    main.py
    tests/test_main.py
    conftest.py
    module_one/  (eg. database, core, auth)
        __init__.py
        module_one.py
        tests/
            test_module_one.py
    module_two/  (eg. api, ui, cli)
        __init__.py
        module_two.py
        tests/
            test_module_two.py
    
    features/  (eg. business logic, tools, etc.)
        feature_one/
            __init__.py
            feature.py
            tests/
                test_feature.py
```

Features can also be part of modules if the module for example is a api integration or a cli tool.

eg
```
src/project/
    module_one/  (api integration with crm service)
        __init__.py
        module_one.py
        tests/
            test_module_one.py
        features/
            feature_one/  (CRM service integration slice)
                __init__.py
                feature.py
                tests/
                    test_feature.py
```

## Documentation Reference

Documentation can be found in /ai_info/docs. 

### FastAPI Documentation
**File:** `ai_info/docs/fasttapi.md`  
**Description:** Comprehensive FastAPI code snippets and examples  
**Key Topics:**
- Installation and setup (pip install "fastapi[standard]", virtual environments)
- Basic application structure (creating FastAPI app, defining endpoints)
- HTTP methods (GET, POST, PUT, DELETE decorators)
- Request handling (path parameters, query parameters, request bodies)
- Pydantic models integration for data validation
- Type hints and automatic validation
- Dependency injection system
- Authentication (OAuth2, security schemes)
- Middleware (CORS, TrustedHost)
- Advanced features (sub-applications, APIRouter, WebSocket)
- Testing with TestClient
- Deployment (Uvicorn, Gunicorn, Docker)
- Database integration examples
- Settings and configuration management
- Async/await patterns

### Pydantic Documentation
**File:** `ai_info/docs/pydantic.md`  
**Description:** Comprehensive Pydantic v2 code snippets and examples  
**Key Topics:**
- Installation (pip, uv, conda)
- BaseModel definition and usage
- Data validation and type coercion
- Field constraints and metadata
- Model serialization (model_dump, model_dump_json)
- Model validation methods (model_validate, model_validate_json)
- Custom validators (field_validator, model_validator, BeforeValidator)
- Generic models and type variables
- Nested models and complex data structures
- Performance optimization (TypeAdapter, tagged unions)
- JSON schema generation
- Migration from Pydantic v1 to v2
- Error handling and ValidationError
- Advanced features (RootModel, computed fields)
- Integration with external services (Redis, HTTP APIs)


## Project Dependencies

### Core Dependencies
- **FastAPI**: Modern web framework for building APIs with Python 3.9+ based on standard Python type hints
- **Pydantic**: Data validation and settings management using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server implementation, using uvloop and httptools

### Optional Dependencies (from fastapi[standard])
- **python-multipart**: Required for form data parsing
- **httpx**: Modern HTTP client for testing and external API calls
- **jinja2**: Templating engine for HTML responses
- **python-jose**: For JWT token handling in authentication

## Common Usage Patterns

### FastAPI Quick Start
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    tax: float | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Running the Application
```bash
# Development
$ fastapi dev main.py

# Production
$ fastapi run main.py --port 80
```

## Project-Specific Implementation

### Authentication System

This project implements **FastAPI-Users with JWT Bearer token authentication** for modern, scalable user management:

#### Core Components

**User Model (models/user.py)**
```python
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, DateTime

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    
    # Additional fields beyond FastAPI-Users base
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    role = Column(String(20), default="user")  # user, admin, premium
```

**JWT Authentication Backend (auth/backend.py)**
```python
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.JWT_EXPIRE_MINUTES * 60,
        algorithm=settings.JWT_ALGORITHM,
    )

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```

**User Dependencies (auth/users.py)**
```python
from fastapi_users import FastAPIUsers

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

# User dependencies for protecting routes
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, verified=True, superuser=True)
```

#### Authentication Routes

The application includes these authentication endpoints:

```python
# Authentication routes (main.py)
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth/jwt", 
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)
```

#### Available Endpoints

**User Registration**
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**User Login**
```bash
POST /auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Protected Endpoint Usage**
```python
@app.get("/protected")
async def protected_endpoint(user: User = Depends(current_active_user)):
    return {
        "message": "Access granted",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        }
    }
```

**API Request with Bearer Token**
```bash
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Configuration

**Environment Variables (.env)**
```bash
# JWT Authentication (required)
JWT_SECRET=your-secure-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
JWT_ISSUER=fastapi-app
JWT_AUDIENCE=fastapi-users

# Database
DATABASE_URL=sqlite+aiosqlite:///./fastapi_users.db

# Legacy API Key (optional, for backward compatibility)
API_KEY=your-legacy-api-key
```

#### Database Migration

```bash
# Initialize Alembic (already done)
uv run alembic init alembic

# Create migration for users table
uv run alembic revision --autogenerate -m "Add users table"

# Apply migration
uv run alembic upgrade head
```

#### Security Features

- **JWT Bearer Tokens**: Industry standard OAuth2 Bearer token authentication
- **User Management**: Registration, login, password reset, email verification
- **Role-Based Access**: Foundation for multi-user features with role support
- **Token Expiration**: Configurable JWT lifetime with refresh capability
- **Password Hashing**: Secure bcrypt password hashing
- **Type Safety**: Full type hints and validation with Pydantic
- **OpenAPI Integration**: Automatic documentation with security schemas

## 📍 Geocoding API

The application includes a comprehensive geocoding API that converts city names to geographic coordinates using the Nominatim service.

**Key Features**: Rate limiting (1 req/sec), caching (24h TTL), user rate limiting (10 req/min), authentication, error handling

**Main Endpoints**: `/geocode/city`, `/geocode/health`, `/geocode/cache/clear`

**Architecture**: Vertical slice with models, services (rate_limiter, cache, geocoding), routers, and tests

**📖 Detailed Implementation**: See [geocoding-implementation.md](ai_info/app/docs/geocoding-implementation.md) for complete patterns, examples, and configuration.

## Testing

**Always create Pytest unit tests for new features** (functions, classes, routes, etc)
Tests are always created in the same directory as the code they test in a tests/ directory. Create the tests directory if it doesn't exist.

**After updating any logic**, check whether existing unit tests need to be updated. If so, do it following the implementation.

Always test individual functions and classes.

### Testing Approach

#### Unit Tests (9 tests)
- Authentication dependency validation
- Custom exception handling
- Error response format verification

#### Integration Tests (31 tests)  
- Full API endpoint testing
- Security attack simulations
- OpenAPI documentation verification
- Environment-based behavior testing

#### Running Tests
```bash
# All tests
make test

# With coverage
pytest --cov=.

# Quality workflow (lint + test)
make quality
```

## Best Practices

1. **Type Hints**: Always use type hints for automatic validation and documentation
2. **Pydantic Models**: Define request/response schemas using Pydantic BaseModel
3. **Dependency Injection**: Use FastAPI's dependency system for shared logic and authentication
4. **Async/Await**: Use async functions for I/O-bound operations
5. **Error Handling**: Utilize HTTPException and proper status codes with request tracking
6. **Security**: Use FastAPI Security classes (`APIKeyHeader`, `Security()`, `Depends()`)
7. **Testing**: Use TestClient for comprehensive API testing with dependency mocking
8. **Documentation**: FastAPI automatically generates OpenAPI documentation with security schemas

For more best practices, see /ai_info/fastapi-best-practices.md

## Project Structure

```
fastapi_template/
├── main.py              # FastAPI application with dependency injection
├── config.py            # Pydantic settings configuration
├── dependencies.py      # FastAPI security dependencies (APIKeyHeader, etc.)
├── middleware.py        # Utility functions for error responses
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures  
│   ├── test_unit.py     # Unit tests for authentication dependencies
│   └── test_integration.py  # Integration tests with FastAPI security
├── utils/               # Utility modules
│   └── logging.py       # Advanced logging utilities
├── .env                 # Environment variables (not in git)
├── requirements.txt     # Python dependencies
├── Makefile            # Common development commands
└── Claude.md           # This documentation file
```

## Common Commands

### Development Workflow
```bash
# Start development server
make run

# Run complete quality workflow (lint + format + test)
make quality

# Run tests only
make test

# Run with coverage
make test-cov

# Lint and format code
make fix

# See all available commands
make help
```

### Docker Development Workflow
```bash
# Build production Docker image
make docker-build

# Start development environment with live reload
make docker-dev

# Start production environment (requires .env.prod)
make docker-prod

# Run tests in container
make docker-test

# Show container status
make docker-ps

# Show logs (auto-detects environment)
make docker-logs

# Check health status and endpoints
make docker-health

# Open shell in running container
make docker-shell

# Stop all containers
make docker-stop

# Clean up containers and images
make docker-clean
```

### Key Environment Variables
```bash
# Required
API_KEY=your-secret-api-key-here    # Minimum 8 characters

# Optional
ENV=development                     # Controls docs visibility
DEBUG=true                         # Debug mode
LOG_LEVEL=INFO                     # Logging level
```

## Configuration Notes

- Virtual environment setup is recommended before installation
- Upgrade pip before installing dependencies: `python -m pip install --upgrade pip`
- For production deployment, use Gunicorn with Uvicorn workers
- Environment variables can be managed using Pydantic Settings
- Tests ensure all 40 test cases pass before deployment
- Use `make quality` before committing code changes
- When writing titles and descriptions for comments and PRs, always follow the standards in ai_info/docs/conventional_commits.md

## 📎 Style & Conventions

- **Use Python** as the primary language.
- **Follow PEP8**, always use type hints, and format with `ruff`.
- **Use `pydanticv2` for data validation**.
- **ALWAYS use classes, data types, data models, for typesafety and verifiability**
- **ALWAYS use docstrings for every function** using the Google style:

  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.

      Raises:
          Exception: Description.
      """
  ```

## 🛠️ Environment Setup

```bash
# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate  # On Windows

# Install dependencies
uv sync

# Install package in development mode
uv pip install -e .
```

## 🛠️ Development Commands

```bash
# Run all tests
uv run pytest

# Run specific tests
uv run pytest concept_library/full_review_loop/tests/ -v

# Format code
uv run ruff format .

# Run linter
uv run ruff check .

# Run type checker
uv run mypy .
```

## 🛠️ UV Package Management

This project has been successfully migrated from pip to uv for Python package management. Key commands include:

```bash
# Create virtual environment and install dependencies
uv sync

# Install a specific package
uv add requests

# Remove a package
uv remove requests

# Run a Python script or command
uv run python script.py
uv run pytest

# Update all dependencies
uv sync --upgrade

# Install editable packages
uv pip install -e .
```

When running scripts or tools, always use `uv run` to ensure proper virtual environment activation:

```bash
# Preferred way to run commands
uv run pytest
uv run ruff check .
uv run fastapi dev main.py

# Running tools without installing
uvx black .
uvx ruff check .
```

### Migration Completed

✅ **Successfully migrated from pip to uv (2025-01-11)**

**Migration Summary:**
- **pyproject.toml**: Updated with all dependencies organized into main and dev groups
- **Makefile**: All pip commands replaced with uv equivalents
- **Dependencies**: 72 packages successfully resolved with no conflicts
- **Testing**: All 160 tests pass with uv run pytest
- **Linting**: All code quality checks pass with uv run ruff check
- **Performance**: 10-100x faster dependency resolution and installation
- **Cleanup**: Removed requirements.txt, fastapi_app.egg-info/, and old venv/ directory

**Key Benefits Achieved:**
1. **Faster dependency resolution**: UV resolves 72 packages in milliseconds vs. minutes with pip
2. **Unified project management**: Single tool for virtual environments, dependencies, and script execution
3. **Better reproducibility**: uv.lock ensures consistent environments across machines
4. **Improved developer experience**: Simplified commands and better error messages
5. **Modern Python packaging**: Following current best practices with pyproject.toml

## 🛠️ BRANCHING STRATEGY

This repository follows a develop → main branching strategy, where:

- `main` is the production branch containing stable releases
- `dev` is the integration branch where features are merged
- Feature branches are created from `dev` for work in progress

When creating branches, follow these naming conventions:

- Feature branches: `feature/descriptive-name`
- Bug fix branches: `fix/issue-description`
- Documentation branches: `docs/what-is-changing`
- Refactoring branches: `refactor/what-is-changing`

## Behavioural Guidelines

- Always use `uv` for package management.
- Always use `ruff` for linting.

- **NEVER ASSUME OR GUESS**
- When in doubt, ask for clarification or ask for help. More often than not you can do websearch to find relevant examples or check ai_info/docs/ for examples that the user have added.

- **Always confirm file paths & module names** exist before using them.

- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

- **KEEP README.md UPDATED**
- Whenever you make changes to the codebase, update the README.md file to reflect the changes. Especially if you add configuration changes or new features.

- **ALWAYS keep CLAUDE.md UPDATED**
- Add new dependencies to CLAUDE.md
- Add important types and patterns to CLAUDE.md

## IMPORTANT TYPES & PATTERNS

### Core Patterns
- **Rate Limiting**: AsyncLock-based pattern for API compliance (1 req/sec)
- **Caching**: TTL-based in-memory caching with MD5 key normalization  
- **Router**: FastAPI router with dependency injection and rate limiting
- **Service**: HTTP client pattern with proper headers and error handling
- **Models**: Pydantic models with field validation and constraints

**📖 Complete Implementation Details**:
- **Geocoding**: [geocoding-implementation.md](ai_info/app/docs/geocoding-implementation.md)
- **Web Crawling**: [crawling-implementation.md](ai_info/app/docs/crawling-implementation.md)
- **MCP Integration**: [mcp-implementation.md](ai_info/app/docs/mcp-implementation.md)
- **CI/CD Workflows**: [ci-cd-patterns.md](ai_info/app/docs/ci-cd-patterns.md)

## 📍 Web Crawling API

The application includes a comprehensive web crawling API that integrates with Crawl4AI to provide advanced crawling capabilities.

**Key Features**: Multi-URL crawling (up to 10 URLs), screenshot capture, recursive crawling, URL deduplication, rate limiting, caching with O(1) invalidation

**Architecture**: Vertical slice with models (advanced validation), services (crawling, cache, rate_limiter), routers, and comprehensive tests

**Advanced Features**: URL normalization, security validation, 4K screenshot limits, breadth-first crawling, async task polling

**📖 Detailed Implementation**: See [crawling-implementation.md](ai_info/app/docs/crawling-implementation.md) for complete patterns, examples, and configuration.

## 🤖 MCP Integration with JWT Bearer Authentication

The application includes a FastMCP server that exposes geocoding functionality through the Model Context Protocol with JWT Bearer token authentication.

**Security**: Dual authentication system supporting both FastAPI-Users and legacy API key authentication

**Integration**: Mounted at `/mcp-server` with proper lifespan management and tool registration

**Authentication Flow**:
1. **FastAPI-Users**: Authenticate via `/auth/jwt/login` → Request MCP token via `/auth/mcp-token` → Use Bearer token for MCP access
2. **Legacy API Key**: Use X-API-KEY → Request MCP token via `/auth/mcp-token/legacy` → Use Bearer token for MCP access

**Key Components**:
- **RSA Key Management**: `services/mcp_rsa_keys.py` - FastMCP RSAKeyPair integration with auto-generation in development
- **MCP Authentication Service**: `services/mcp_auth.py` - Bridges HMAC-based FastAPI-Users with RSA-based MCP requirements  
- **Token Generation Endpoints**: `routers/mcp_auth.py` - Dual authentication support with comprehensive error handling
- **MCP Server**: `mcp_integration/server.py` - BearerAuthProvider with RSA JWT validation

**Configuration**:
```bash
# MCP JWT Configuration (extends existing JWT settings)
MCP_JWT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."  # RSA private key (PEM format)
MCP_JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----..."    # RSA public key (PEM format)
MCP_JWT_ALGORITHM=RS256                               # RSA algorithm
MCP_JWT_EXPIRE_MINUTES=60                            # Token expiration
MCP_JWT_ISSUER=personal-server                       # Token issuer
MCP_JWT_AUDIENCE=mcp-server                          # Token audience
```

**Development**: Auto-generates RSA keys with warnings. Production requires explicit keys.

**Tools Available**: `geocode_city` with type-safe parameters, error handling, and same caching/rate limiting as REST API

**📖 Detailed Implementation**: See [mcp-implementation.md](ai_info/app/docs/mcp-implementation.md) for complete patterns, testing, and extension examples.

## 🚀 CI/CD Pipeline

The project implements a comprehensive CI/CD pipeline using GitHub Actions with modern best practices for Python projects using uv.

**Key Features**: Path-based filtering, uv caching (10-100x faster), parallel job execution, security scanning, artifact management

**Workflows**: Quality & testing, security (dependency review, multi-tool scanning), automated dependency updates

**Best Practices**: CI-safe commands, local/CI parity, Python 3.13, comprehensive testing (160+ tests)

**Performance**: Dramatically faster pipelines, better dependency resolution, modern Python packaging

**📖 Detailed Implementation**: See [ci-cd-patterns.md](ai_info/app/docs/ci-cd-patterns.md) for complete workflow configurations, security patterns, and performance optimizations.

## IMPORTANT TYPES & PATTERNS

### Core Patterns
- **Rate Limiting**: AsyncLock-based pattern for API compliance (1 req/sec)
- **Caching**: TTL-based in-memory caching with MD5 key normalization  
- **Router**: FastAPI router with dependency injection and rate limiting
- **Service**: HTTP client pattern with proper headers and error handling
- **Models**: Pydantic models with field validation and constraints

**📖 Complete Implementation Details**:
- **Geocoding**: [geocoding-implementation.md](ai_info/app/docs/geocoding-implementation.md)
- **Web Crawling**: [crawling-implementation.md](ai_info/app/docs/crawling-implementation.md)
- **MCP Integration**: [mcp-implementation.md](ai_info/app/docs/mcp-implementation.md)
- **CI/CD Workflows**: [ci-cd-patterns.md](ai_info/app/docs/ci-cd-patterns.md)


### MCP Authentication Patterns
- **RSA Key Management**: FastMCP RSAKeyPair integration with singleton pattern and environment fallbacks
- **Dual Authentication**: FastAPI-Users (HMAC JWT) + Legacy API Key → RSA JWT for MCP access
- **Token Generation**: Service-based pattern with comprehensive error handling and logging
- **Bearer Authentication**: FastMCP BearerAuthProvider with RSA JWT validation
- **Development Fallback**: Auto-generation with production warnings and validation
