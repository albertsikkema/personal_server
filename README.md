# FastAPI Application with Security by Design

An enterprise-grade FastAPI application implementing API key authentication using FastAPI's official security system with dependency injection. Features automatic OpenAPI security documentation, production-ready operational capabilities, comprehensive security testing, and enhanced observability.

**Repository**: [https://github.com/epblc/fastapi_template](https://github.com/epblc/fastapi_template)

## Features

### 🔒 Security
- **FastAPI Security Integration**: Official FastAPI security implementation using `fastapi.security.APIKeyHeader`
- **Dependency Injection Authentication**: Clean, testable authentication using FastAPI dependencies
- **API Key Authentication**: Secure authentication using X-API-KEY header with validation
- **OpenAPI Security Documentation**: Automatic security scheme documentation in Swagger/ReDoc
- **Comprehensive Security Testing**: Protection against injection attacks, XSS, and malformed input
- **Case-Insensitive Headers**: HTTP standard-compliant header handling

### 🚀 Production Ready
- **Enhanced Error Responses**: Request IDs and timestamps for debugging
- **Structured Logging**: Authentication events and security audit trails
- **Configuration Validation**: Comprehensive environment variable validation
- **Operational Observability**: Request tracking and incident correlation

### 🧪 Development Excellence
- **Comprehensive Testing**: 40 tests including security attack simulations
- **Code Quality**: Ruff linting and formatting with zero issues
- **CORS Support**: Configured for cross-origin requests
- **Auto-generated Documentation**: Interactive API documentation at `/docs`
- **Makefile Workflow**: Streamlined development commands

## FastAPI Security Benefits

This application leverages **FastAPI's official security implementation** for maximum compatibility and maintainability:

### 🎯 **Standards Compliance**
- Uses `fastapi.security.APIKeyHeader` for standard security patterns
- Follows FastAPI best practices and conventions
- Compatible with all FastAPI tooling and ecosystem

### 📚 **Automatic Documentation**
- **OpenAPI Integration**: Security schemes automatically documented
- **Swagger UI**: Built-in authentication interface with "Authorize" button
- **ReDoc**: Complete security documentation with examples
- **Type Safety**: Full type hints and IDE support

### 🧪 **Better Testing**
- **Dependency Injection**: Easy to mock and test authentication
- **Explicit Dependencies**: Clear security requirements in code
- **Unit Testable**: Authentication logic isolated and testable

### 🔧 **Maintainability**
- **Explicit Security**: Each endpoint declares its auth requirements
- **No Hidden Behavior**: No middleware magic, everything is visible
- **Flexible**: Easy to add new auth types or modify existing ones
- **Error Handling**: Consistent error responses with request tracking

### 📖 **Developer Experience**
```python
# Clear, explicit, and discoverable
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "Authenticated"}
```

## Security Model

This application uses **FastAPI's official security implementation** with dependency injection:
- Authentication is handled through FastAPI dependencies using `Security()` and `Depends()`
- Protected endpoints explicitly declare authentication requirements
- Public endpoints require no authentication dependencies
- Currently public endpoints:
  - `/` - Root endpoint
  - `/health` - Health check
  - `/docs` - Swagger UI documentation (includes authentication UI)
  - `/redoc` - ReDoc documentation (includes security information)
  - `/openapi.json` - OpenAPI schema (includes security definitions)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/epblc/fastapi_template.git
cd fastapi_template
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set your API_KEY
```

## Configuration

Create a `.env` file in the project root with the following:

```env
# Required: API key for authentication (minimum 8 characters)
API_KEY=your-secret-api-key-here

# Optional: Application configuration
APP_NAME=FastAPI Application
DEBUG=true
ENV=development

# Logging configuration
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_FILE_PATH=logs
LOG_FILE_NAME=fastapi.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
LOG_JSON_FORMAT=true
```

### Configuration Validation

The application includes comprehensive configuration validation:

#### Core Settings
- **API_KEY**: Required, minimum 8 characters for security
- **APP_NAME**: Application name for logging and identification
- **DEBUG**: Boolean flag for debug mode
- **ENV**: Environment (development, staging, production) - controls API documentation visibility

#### Logging Settings
- **LOG_LEVEL**: Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
- **LOG_TO_FILE**: Enable/disable file logging (default: true)
- **LOG_FILE_PATH**: Directory for log files (default: "logs")
- **LOG_FILE_NAME**: Log file name (default: "fastapi.log")
- **LOG_MAX_BYTES**: Max file size before rotation (default: 10MB)
- **LOG_BACKUP_COUNT**: Number of backup files to keep (default: 5)
- **LOG_JSON_FORMAT**: Use JSON format for file logs (default: true)

Invalid configurations will cause the application to fail fast with clear error messages.

## Usage

### Quick Start with Makefile

This project includes a Makefile for common development tasks:

```bash
# Start development server
make run

# Run complete code quality workflow
make quality

# Run tests
make test

# See all available commands
make help
```

### Running the Application

Development mode with auto-reload:
```bash
# Using Makefile (recommended)
make run

# Or directly
fastapi dev main.py
```

Production mode:
```bash
fastapi run main.py --port 8000
```

### API Endpoints

#### Public Endpoints (No Authentication Required)

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

#### Protected Endpoints (API Key Required)

- `GET /protected` - Example protected endpoint
- `GET /protected/data` - Example protected data endpoint

### Authentication

This application uses FastAPI's official security system with automatic OpenAPI integration.

#### Using the API

Include the API key in the request header. Headers are case-insensitive per HTTP standards:
```bash
# All of these work (case-insensitive)
curl -H "X-API-KEY: your-secret-api-key-here" http://localhost:8000/protected
curl -H "x-api-key: your-secret-api-key-here" http://localhost:8000/protected
curl -H "X-Api-Key: your-secret-api-key-here" http://localhost:8000/protected
```

#### Using Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click the "Authorize" button in the top right
3. Enter your API key in the "APIKeyHeader (X-API-KEY)" field
4. Click "Authorize" to authenticate
5. Now you can test protected endpoints directly in the UI

#### OpenAPI Security Schema

The application automatically generates OpenAPI security documentation:
```json
{
  "components": {
    "securitySchemes": {
      "APIKeyHeader": {
        "type": "apiKey",
        "description": "API key for authentication",
        "in": "header", 
        "name": "X-API-KEY"
      }
    }
  }
}
```

### Error Responses

Authentication failures return enhanced error responses with request tracking:
```json
{
  "detail": "API key missing",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-06T10:30:00.123456Z"
}
```

## Code Quality & Testing

### Comprehensive Test Suite

The application includes 40 comprehensive tests covering:
- **Unit Tests**: Authentication dependency and security function validation
- **Integration Tests**: Full API endpoint testing with FastAPI security
- **Security Tests**: Injection attacks, XSS, and malformed input protection
- **Header Tests**: Case-insensitive header handling verification
- **Environment Tests**: Documentation visibility across development, staging, and production
- **Edge Cases**: Empty values, unicode attacks, and extreme input sizes
- **OpenAPI Tests**: Security scheme documentation and Swagger UI integration

### Linting and Formatting with Ruff

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and code formatting.

Check code quality:
```bash
ruff check .
```

Auto-fix linting issues:
```bash
ruff check --fix .
```

Format code:
```bash
ruff format .
```

### Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=.
```

Run specific test file:
```bash
pytest tests/test_integration.py -v
```

### Development Workflow

Before committing code, run:
```bash
# Using Makefile (recommended)
make quality

# Or manually
ruff format .
ruff check --fix .
pytest
```

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make run` | Start FastAPI development server |
| `make test` | Run all tests |
| `make test-cov` | Run tests with coverage report |
| `make lint` | Run linter (ruff check) |
| `make format` | Format code with ruff |
| `make fix` | Auto-fix linting issues and format code |
| `make quality` | Run complete code quality workflow |
| `make clean` | Clean up cache and temporary files |
| `make setup` | Complete project setup from scratch |
| `make help` | Show all available commands |

## Project Structure

```
fastapi_template/
├── main.py              # FastAPI application with dependency injection
├── config.py            # Pydantic settings configuration
├── dependencies.py      # FastAPI security dependencies (APIKeyHeader, etc.)
├── middleware.py        # Utility functions for error responses
├── tests/               # Test suite
│   ├── __init__.py
│   ├── conftest.py      # Test fixtures
│   ├── test_unit.py     # Unit tests for authentication dependencies
│   └── test_integration.py  # Integration tests with FastAPI security
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Ruff configuration and project metadata
├── pytest.ini           # Pytest configuration
├── Makefile            # Common development commands
├── reviews/            # Code review documentation
│   ├── 20250106221930_review.md      # Original code review
│   ├── 20250106_response.md          # Implementation response
│   └── 20250106_final_response.md    # Final implementation summary
├── utils/              # Utility modules
│   ├── __init__.py
│   └── logging.py      # Advanced logging utilities with JSON formatting
├── logs/               # Log files (excluded from git)
│   └── .gitkeep        # Keep directory in git
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Development

### Adding New Endpoints

With FastAPI dependency injection, endpoints are explicit about their security requirements:

#### Protected Endpoints (Require Authentication)
```python
from dependencies import RequiredAuth

@app.get("/my-protected-endpoint")
async def my_protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "This endpoint requires authentication"}
```

#### Public Endpoints (No Authentication)
```python
@app.get("/my-public-endpoint")
async def my_public_endpoint():
    return {"message": "This endpoint is public"}
```

#### Optional Authentication
```python
from dependencies import OptionalAuth

@app.get("/my-optional-auth-endpoint")
async def my_optional_auth_endpoint(api_key: Optional[str] = OptionalAuth):
    if api_key:
        return {"message": "Authenticated user", "authenticated": True}
    return {"message": "Public access", "authenticated": False}
```

This approach makes security requirements explicit and visible in the code, improving maintainability and reducing security mistakes.

### CORS Configuration

CORS is currently configured to allow all origins (`*`). For production, update the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],              # Specific methods
    allow_headers=["*"],
)
```

## Operational Features

### Advanced Logging System

The application features a comprehensive logging system with multiple output formats and rotation:

#### Console Logging
- Human-readable format for development
- Real-time log output with timestamps
- Configurable log levels

#### File Logging with Rotation
- Automatic log rotation when files exceed 10MB (configurable)
- Keeps 5 backup files by default (configurable)
- JSON format for structured data analysis
- Azure Blob Storage compatible format

#### Structured Logging Examples

**Console Output:**
```
2025-01-06 10:30:00 - middleware - INFO - Authentication attempt
```

**JSON File Output:**
```json
{
  "timestamp": "2025-01-06T10:30:00.123456Z",
  "level": "INFO",
  "logger": "middleware",
  "message": "Authentication attempt",
  "module": "middleware",
  "function": "dispatch",
  "line": 64,
  "path": "/protected",
  "method": "GET",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "has_api_key": true,
  "client_ip": "192.168.1.100"
}
```

#### Security Features
- Automatic sanitization of sensitive data (API keys, passwords, tokens)
- Request correlation with unique IDs
- Authentication event tracking

#### Future Azure Blob Integration

The logging system is designed for future Azure Blob Storage integration:
- JSON format compatible with Azure Log Analytics
- Batch upload capabilities (planned)
- Managed Identity authentication support (planned)
- Automatic log archival to cloud storage (planned)

### Request Tracking

All authentication failures include unique request IDs for debugging and incident correlation. Use these IDs to trace issues across logs and error responses.

### Configuration Management

Environment variables are validated at startup with clear error messages:
- API key length requirements
- Valid log level formats
- Type validation for all settings

## API Documentation

### Environment-Based Documentation Visibility

The API documentation endpoints are automatically controlled by the `ENV` environment variable:

#### Development & Staging (ENV=development or ENV=staging)
When running in development or staging environments, full documentation is available:
- **Interactive API documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API documentation (ReDoc)**: http://localhost:8000/redoc  
- **OpenAPI schema**: http://localhost:8000/openapi.json

#### Production (ENV=production)
In production environments, documentation endpoints are automatically hidden for security:
- All documentation URLs return **404 Not Found**
- No API schema information is exposed
- Reduces attack surface and prevents information disclosure

#### Configuration Examples
```bash
# Development/Testing - docs available
ENV=development

# Staging - docs available  
ENV=staging

# Production - docs hidden
ENV=production
```

**Default Behavior**: If `ENV` is not set, it defaults to `development` with docs enabled.

## Security Features

### Built-in Security Testing

The application includes comprehensive security testing against:
- **SQL Injection**: Malicious SQL in API keys
- **XSS Attacks**: Script injection attempts
- **Header Injection**: CRLF injection in headers
- **Unicode Attacks**: Normalization bypass attempts
- **Null Byte Injection**: String termination attacks
- **Extreme Input**: 10KB+ API key handling
- **Malformed Data**: Empty and whitespace-only inputs

### Security by Design

- **Default Deny**: All endpoints protected unless explicitly whitelisted
- **Case-Insensitive Headers**: HTTP standard compliant
- **Input Validation**: Comprehensive API key validation
- **Audit Logging**: All authentication attempts logged
- **Error Handling**: No information leakage in responses

## Production Deployment

### Security Checklist

1. **API Key Management**:
   - Use strong API keys (minimum 8 characters, recommend 32+)
   - Never commit `.env` files to version control
   - Implement key rotation procedures

2. **Network Security**:
   - Always use HTTPS in production
   - Implement rate limiting at gateway/proxy level
   - Restrict CORS origins to specific domains

3. **Monitoring**:
   - Monitor authentication failure patterns
   - Set up alerts for unusual request patterns
   - Use request IDs for incident correlation

4. **Configuration**:
   - Set `DEBUG=false` in production
   - Configure appropriate `LOG_LEVEL` (INFO or WARNING)
   - Validate all environment variables at startup

## Development & Contributing

### Development Workflow

1. Create a feature branch
2. Make your changes
3. Run the complete quality workflow:
   ```bash
   make quality  # Runs: ruff format, ruff check --fix, pytest
   ```
4. Ensure all 37 tests pass and zero linting issues
5. Submit a pull request

### Code Quality Standards

- **Test Coverage**: All new features must include tests
- **Security Testing**: Add security tests for new attack vectors
- **Linting**: Zero Ruff violations required
- **Type Safety**: Full type hint coverage
- **Documentation**: Update README for new features

### Adding Security Tests

When adding new security tests, follow the pattern in `TestSecurityTesting`:
```python
def test_new_attack_vector(self, client: TestClient):
    """Test protection against new attack type."""
    malicious_headers = {"X-API-KEY": "malicious-payload"}
    response = client.get("/protected", headers=malicious_headers)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid API key"
    assert "request_id" in data
```

## License

This project is proprietary software developed for internal company use only. All rights reserved. Distribution, modification, or sharing outside the company is strictly prohibited.