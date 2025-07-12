name: "Authentication Migration Strategy: Remove API Key Authentication"
description: |

## Purpose

Simple cleanup to remove legacy API key authentication code since it's no longer used in development.

## Core Principles

1. **Move Fast**: Development environment, data loss acceptable
2. **Clean Codebase**: Remove unused authentication patterns
3. **JWT Only**: Simplify to single authentication method

---

## Goal

Remove all API key authentication code from the FastAPI application, keeping only JWT Bearer token authentication with FastAPI-Users.

## Why

- **Code Cleanup**: Remove unused legacy authentication code
- **Simplified Architecture**: Single authentication method is easier to maintain
- **No Users**: API keys are not being used anymore

## What

Remove all API key authentication code and dependencies, keeping only JWT authentication.

### Success Criteria

- [ ] API key authentication code removed from codebase
- [ ] All endpoints use JWT authentication only
- [ ] No references to API_KEY in configuration
- [ ] Tests updated to reflect JWT-only authentication

## Key Files to Modify

- **dependencies.py**: Remove API key authentication functions
- **config.py**: Remove API_KEY configuration 
- **routers/mcp_auth.py**: Remove legacy API key endpoints
- **services/mcp_auth.py**: Remove API key bridge functions

## Current API Key Code to Remove

```python
# dependencies.py - Remove these functions:
- verify_api_key()
- optional_api_key() 
- RequiredAuth dependency
- OptionalAuth dependency

# config.py - Remove:
- API_KEY setting

# services/mcp_auth.py - Remove:
- generate_mcp_token_for_legacy_api_key()

# routers/mcp_auth.py - Remove:
- POST /auth/mcp-token/legacy endpoint
```

## Simple Task List

```yaml
Task 1 - Remove API Key Dependencies:
MODIFY dependencies.py:
  - DELETE verify_api_key() function
  - DELETE optional_api_key() function
  - DELETE RequiredAuth and OptionalAuth dependencies
  - DELETE AuthHTTPException class if only used for API keys

Task 2 - Clean Configuration:
MODIFY config.py:
  - DELETE API_KEY field from Settings class

Task 3 - Remove Legacy MCP Auth:
MODIFY services/mcp_auth.py:
  - DELETE generate_mcp_token_for_legacy_api_key() method
  - DELETE _hash_api_key() method if only used for legacy

MODIFY routers/mcp_auth.py:
  - DELETE POST /auth/mcp-token/legacy endpoint
  - DELETE MCPTokenRequest model if only used for legacy

Task 4 - Update Tests:
MODIFY tests/:
  - REMOVE API key test cases
  - UPDATE any tests that reference API_KEY or RequiredAuth
```

## Validation

```bash
# After removing API key code, ensure everything still works:
uv run pytest tests/ -v
uv run ruff check .
uv run mypy .

# Test JWT authentication still works:
curl -X POST http://localhost:8000/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your-email@example.com&password=your-password"

# Test endpoints work with JWT:
curl -H "Authorization: Bearer <jwt-token>" http://localhost:8000/geocoding/city/London
```

## Final Checklist

- [ ] API key code removed from dependencies.py
- [ ] API_KEY removed from config.py  
- [ ] Legacy MCP endpoints removed
- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check .`
- [ ] JWT authentication still works

**Confidence Score: 9/10** - Simple cleanup task with clear file targets.