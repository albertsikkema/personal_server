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

This project implements **FastAPI's official security system** using dependency injection:

#### Core Security Components
```python
# dependencies.py
from fastapi.security import APIKeyHeader
from fastapi import Security, Depends

api_key_header = APIKeyHeader(
    name="X-API-KEY", 
    auto_error=False,
    description="API key for authentication"
)

async def verify_api_key(api_key: Annotated[str, Security(api_key_header)]) -> str:
    # Authentication logic with custom error responses
    
RequiredAuth = Depends(verify_api_key)  # Helper alias
OptionalAuth = Depends(optional_api_key)  # Optional auth
```

#### Usage in Endpoints
```python
# Protected endpoint - requires authentication
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "Authenticated"}

# Public endpoint - no authentication
@app.get("/public")
async def public_endpoint():
    return {"message": "Public"}

# Optional authentication
@app.get("/optional")
async def optional_endpoint(api_key: Optional[str] = OptionalAuth):
    return {"authenticated": bool(api_key)}
```

#### Error Response Format
```python
# Custom exception for consistent error responses
class AuthHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str):
        self.response_content = {
            "detail": message,
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        super().__init__(status_code=status_code, detail=self.response_content)
```

#### OpenAPI Integration
- Automatic security scheme documentation
- Swagger UI "Authorize" button 
- Security requirements per endpoint
- Type-safe authentication

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