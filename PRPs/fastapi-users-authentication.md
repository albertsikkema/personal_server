# PRP: FastAPI-Users Authentication with Bearer Token Integration

## Feature: Replace X-API-KEY authentication with FastAPI-Users and JWT Bearer tokens to fix MCP authentication and implement professional-grade security

### Overview
Implement FastAPI-Users authentication system with JWT Bearer tokens to replace the current X-API-KEY system. This addresses critical security issues, fixes broken MCP authentication, and provides a foundation for multi-user support with role-based access control.

### Context & Documentation

#### Current Authentication Issues
1. **Broken MCP Authentication**: FastMCP middleware implementation in `mcp_integration/server.py` is not working properly
2. **Security Limitations**: Single static X-API-KEY with no expiration or rotation
3. **Scalability Issues**: Cannot support multiple users or roles
4. **Non-Standard Approach**: Custom authentication vs industry OAuth2 standards

#### FastAPI-Users Documentation
- **Main Documentation**: https://fastapi-users.github.io/fastapi-users/latest/
- **JWT Authentication**: https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/backend/
- **SQLAlchemy Integration**: https://fastapi-users.github.io/fastapi-users/latest/configuration/databases/sqlalchemy/
- **Router Configuration**: https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/

#### FastMCP Bearer Token Authentication
- **Bearer Token Provider**: https://gofastmcp.com/servers/auth/bearer
- **MCP Authorization Spec**: https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization
- **FastMCP GitHub**: https://github.com/jlowin/fastmcp

#### Existing Codebase Analysis

**Current Authentication System (dependencies.py)**
```python
# Current X-API-KEY implementation
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str) -> str:
    if api_key != settings.API_KEY:
        raise AuthHTTPException(status_code=401, message="Invalid API key")
    return api_key

RequiredAuth = Depends(verify_api_key)
```

**Current Configuration (config.py)**
```python
class Settings(BaseSettings):
    API_KEY: str = Field(..., min_length=8, description="API key for authentication")
    # ... other settings
```

**Current Test Patterns (tests/test_integration.py)**
```python
class TestProtectedEndpoints:
    def test_protected_endpoint_no_auth(self, client: TestClient):
        response = client.get("/protected")
        assert response.status_code == 401
        assert data["detail"] == "API key missing"
```

### Implementation Blueprint

#### 1. Database Setup and Models

**User Model with FastAPI-Users Integration**
```python
# models/user.py
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    
    # Additional fields beyond FastAPI-Users base
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Role-based access (future extension)
    role = Column(String(20), default="user")  # user, admin, premium
```

**Database Configuration**
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./fastapi_users.db"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
```

#### 2. FastAPI-Users Configuration

**User Manager Implementation**
```python
# managers/user_manager.py
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from models.user import User
from database import get_async_session

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_login(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} logged in.")
        # Update last_login timestamp
        user.last_login = datetime.utcnow()

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
```

**Authentication Backend Configuration**
```python
# auth/backend.py
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```

#### 3. FastAPI-Users Integration

**FastAPI-Users Instance**
```python
# auth/users.py
import uuid
from fastapi_users import FastAPIUsers
from models.user import User
from managers.user_manager import get_user_manager
from auth.backend import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Current user dependencies
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_admin_user = fastapi_users.current_user(active=True, verified=True, superuser=True)
```

**User Schemas**
```python
# schemas/user.py
from fastapi_users import schemas
from pydantic import EmailStr
from typing import Optional

class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"

class UserCreate(schemas.BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str

class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
```

#### 4. Router Integration

**Authentication Routes**
```python
# main.py additions
from auth.users import fastapi_users, auth_backend
from schemas.user import UserRead, UserCreate, UserUpdate

# Include authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth/jwt", 
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
```

#### 5. Update Existing Endpoints

**Migration from X-API-KEY to Bearer Token**
```python
# Before (dependencies.py)
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "Access granted"}

# After (using FastAPI-Users)
@app.get("/protected")
async def protected_endpoint(user: User = Depends(current_active_user)):
    return {"message": f"Access granted to {user.email}"}
```

**Geocoding Endpoint Migration**
```python
# routers/geocoding.py - Update to use Bearer token
from auth.users import current_active_user

@router.get("/city", response_model=GeocodingResponse)
@limiter.limit(settings.GEOCODING_USER_RATE_LIMIT)
async def geocode_city(
    request: Request,
    city: str = Query(..., min_length=1, max_length=200),
    user: User = Depends(current_active_user)  # Replace RequiredAuth
):
    # Implementation remains the same
```

#### 6. Fix MCP Authentication

**Remove Broken Middleware**
```python
# Remove from mcp_integration/server.py
# class AuthenticationMiddleware(Middleware):  # DELETE THIS
#     async def on_request(self, context: MiddlewareContext, call_next):
#         # This doesn't work properly
```

**Implement FastMCP BearerAuthProvider**
```python
# mcp_integration/server.py
from fastmcp.server.auth import BearerAuthProvider
from config import settings

def get_mcp_server() -> FastMCP:
    global _mcp_server
    if _mcp_server is None:
        # Configure Bearer token authentication
        auth_provider = BearerAuthProvider(
            public_key=settings.JWT_PUBLIC_KEY,
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            algorithm="RS256"
        )
        
        _mcp_server = FastMCP(
            name="Personal MCP Server",
            auth=auth_provider,
            instructions="""
            This server provides capabilities through the Model Context Protocol.
            Authentication: Requires Bearer token (JWT) in Authorization header.
            """,
        )
        
        _mcp_server.add_tool(geocode_city)
    
    return _mcp_server
```

#### 7. Configuration Updates

**Updated Settings**
```python
# config.py additions
class Settings(BaseSettings):
    # JWT Configuration
    JWT_SECRET: str = Field(..., min_length=32, description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRE_MINUTES: int = Field(default=60, description="JWT expiration in minutes")
    JWT_ISSUER: str = Field(default="fastapi-app", description="JWT issuer")
    JWT_AUDIENCE: str = Field(default="fastapi-users", description="JWT audience")
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./fastapi_users.db",
        description="Database URL"
    )
    
    # For MCP (RSA keys for production)
    JWT_PUBLIC_KEY: Optional[str] = Field(default=None, description="JWT public key for MCP")
    JWT_PRIVATE_KEY: Optional[str] = Field(default=None, description="JWT private key for MCP")
    
    # Backward compatibility (remove after migration)
    API_KEY: Optional[str] = Field(default=None, description="Legacy API key")
```

### Implementation Tasks (In Order)

1. **✅ Database Setup**
   - Install SQLAlchemy and Alembic: `uv add sqlalchemy alembic aiosqlite`
   - Install FastAPI-Users: `uv add "fastapi-users[sqlalchemy]"`
   - Create database models and migration scripts
   - Set up async database session management

2. **✅ User Management System**
   - Create User model extending FastAPI-Users base
   - Implement UserManager with custom logic
   - Create Pydantic schemas for User operations
   - Set up database user repository pattern

3. **✅ Authentication Backend**
   - Configure JWT strategy with proper secret management
   - Set up Bearer token transport
   - Create authentication backend with proper lifetime
   - Implement user dependencies for route protection

4. **✅ FastAPI Integration**
   - Add authentication routes (login, register, users)
   - Update main.py with FastAPI-Users router inclusion
   - Configure lifespan events for database initialization
   - Add proper error handling and validation

5. **✅ Migrate Existing Endpoints**
   - Update all protected endpoints to use Bearer tokens
   - Replace RequiredAuth with current_active_user
   - Maintain backward compatibility during transition
   - Update rate limiting to work with user-based auth

6. **✅ Fix MCP Authentication**
   - Remove broken middleware implementation
   - Implement FastMCP BearerAuthProvider
   - Configure JWT validation for MCP requests
   - Test MCP tool access with Bearer tokens

7. **✅ Testing Update**
   - Update test fixtures to use Bearer tokens
   - Create user registration/login test helpers
   - Update all authentication-related tests
   - Add integration tests for MCP authentication

8. **✅ Documentation and Configuration**
   - Update environment variable documentation
   - Create user registration/login examples
   - Update API documentation with new auth flows
   - Update CLAUDE.md with authentication patterns

### Validation Gates

**Development Environment Setup**
```bash
# Install dependencies
uv add "fastapi-users[sqlalchemy]" alembic aiosqlite

# Database setup
uv run alembic init alembic
uv run alembic revision --autogenerate -m "Add users table"
uv run alembic upgrade head
```

**Code Quality Checks**
```bash
# Syntax and style
uv run ruff check --fix .
uv run ruff format .

# Type checking
uv run mypy .
```

**Testing Validation**
```bash
# Unit tests
uv run pytest tests/test_unit.py -v

# Integration tests
uv run pytest tests/test_integration.py -v

# Authentication-specific tests
uv run pytest tests/test_auth.py -v

# MCP authentication tests
uv run pytest mcp_integration/tests/test_mcp_auth.py -v
```

**Manual Testing Commands**
```bash
# User registration
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# User login
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# Protected endpoint with Bearer token
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# MCP authentication test
python -c "
import asyncio
from fastmcp import Client

async def test_mcp_auth():
    headers = {'Authorization': 'Bearer YOUR_JWT_TOKEN'}
    async with Client('http://localhost:8000/mcp-server/mcp', headers=headers) as client:
        tools = await client.list_tools()
        print(f'Available tools: {tools}')
        result = await client.call_tool('geocode_city', {'city': 'London'})
        print(f'Result: {result}')

asyncio.run(test_mcp_auth())
"
```

### Key Design Decisions

#### 1. **Database Strategy**
- **SQLite for Development**: Easy setup, file-based, perfect for development
- **PostgreSQL Ready**: Easy migration path for production
- **Async Support**: Full async/await compatibility with FastAPI
- **Alembic Migrations**: Professional database schema management

#### 2. **Authentication Architecture**
- **JWT Strategy**: Industry standard, stateless, secure
- **Bearer Token Transport**: OAuth2 compliant, works with MCP
- **Role-Based Access**: Foundation for future multi-user features
- **Token Expiration**: Configurable security with refresh capability

#### 3. **Migration Strategy**
- **Backward Compatibility**: Maintain X-API-KEY during transition
- **Gradual Migration**: Endpoints updated incrementally
- **Comprehensive Testing**: Ensure no functionality breaks
- **Clear Documentation**: Guide users through the transition

#### 4. **MCP Integration**
- **Native FastMCP Support**: Use BearerAuthProvider instead of middleware
- **JWT Validation**: Proper token verification and claims checking
- **Security Compliance**: Follows MCP authorization specification
- **Production Ready**: RSA key support for advanced JWT validation

#### 5. **Security Considerations**
- **Secret Management**: Proper environment variable handling
- **Token Lifetime**: Configurable expiration times
- **Password Hashing**: Bcrypt with proper salt handling
- **Rate Limiting**: User-based instead of IP-based limits

### Expected Outcomes

#### 1. **Fixed Authentication Issues**
- MCP authentication works properly with Bearer tokens
- No more broken middleware implementations
- Proper JWT validation and error handling

#### 2. **Enhanced Security**
- Industry-standard OAuth2 Bearer tokens
- Configurable token expiration times
- Professional password hashing and validation
- Role-based access control foundation

#### 3. **Improved User Experience**
- Standard login/register flows
- Proper error messages and status codes
- OpenAPI documentation with authentication
- JWT token refresh capabilities

#### 4. **Future-Proof Architecture**
- Multi-user support ready
- Role-based permissions extensible
- Social authentication ready (OAuth2)
- Admin interface capabilities

### Success Criteria

- [x] **Database Setup**: SQLAlchemy models and Alembic migrations working
- [x] **User Management**: Registration, login, and user CRUD operations
- [x] **JWT Authentication**: Token generation, validation, and refresh
- [x] **API Migration**: All endpoints use Bearer token authentication
- [x] **MCP Authentication**: FastMCP BearerAuthProvider working properly
- [x] **Testing Coverage**: All authentication flows tested and passing
- [x] **Documentation**: Complete user guides and API documentation
- [x] **Security Validation**: No security vulnerabilities or token leaks
- [x] **Performance**: No significant performance degradation
- [x] **Backward Compatibility**: Smooth transition from X-API-KEY

### Potential Gotchas

1. **Database Migrations**: Ensure proper Alembic setup and table creation
2. **JWT Secret Management**: Use secure, random secrets in production
3. **Token Expiration**: Balance security with user experience
4. **MCP Integration**: Ensure proper JWT validation configuration
5. **Testing Setup**: Mock authentication in tests properly
6. **CORS Configuration**: Ensure Bearer tokens work with CORS
7. **Error Handling**: Proper authentication error responses

### Risk Assessment

**Low Risk:**
- FastAPI-Users is mature and well-documented
- SQLAlchemy and Alembic are battle-tested
- JWT is industry standard
- Existing codebase patterns are well-established

**Medium Risk:**
- MCP authentication integration requires proper configuration
- Database migration needs careful execution
- Test suite updates require comprehensive coverage

**High Risk:**
- None identified - this is a well-established pattern with good documentation

### Dependencies to Add

```toml
# pyproject.toml additions
dependencies = [
    "fastapi[standard]",
    "fastapi-users[sqlalchemy]",
    "sqlalchemy",
    "alembic",
    "aiosqlite",  # For development
    "asyncpg",    # For PostgreSQL (optional)
    "python-multipart",  # For form data
    "pydantic-settings",
    "fastmcp",
]
```

## PRP Confidence Score: 9/10

**High confidence** - This implementation follows well-established patterns with comprehensive documentation and examples. FastAPI-Users is a mature library with excellent SQLAlchemy integration. The FastMCP Bearer token authentication is officially supported and documented. The existing codebase provides clear patterns to follow.

**Risk factors that prevent 10/10:**
- MCP authentication testing requires proper JWT configuration
- Database migration needs careful execution
- Comprehensive test suite updates required

**Likelihood of one-pass success: 90%** - Well-documented patterns, existing codebase compatibility, and clear implementation steps make this highly likely to succeed in a single implementation pass.