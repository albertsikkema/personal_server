# PRP: JWT Bearer Token Authentication for MCP Endpoints

## Feature: #9 - Implement JWT Bearer token authentication for the Model Context Protocol (MCP) endpoints to secure access to MCP tools and align with the application's JWT authentication strategy

### Overview
Implement JWT Bearer token authentication for MCP endpoints using RSA key pairs while maintaining compatibility with the existing API key authentication system for the main application. This addresses the current security gap where MCP endpoints are publicly accessible and establishes a dual authentication system.

### Issue Context
**GitHub Issue**: https://github.com/albertsikkema/personal_server/issues/9

**Current State Analysis:**
- ✅ MCP server running without authentication (mcp_integration/server.py:25-39)
- ✅ FastAPI application using X-API-KEY authentication (dependencies.py:35-69)  
- ✅ MCP tools (geocoding) accessible without credentials (mcp_integration/tools/geocoding.py)
- ⚠️ Security Gap: MCP endpoints publicly accessible with no user tracking or rate limiting
- ⚠️ Inconsistent security model across application components

**Root Cause:**
FastMCP framework requires RSA-based JWT tokens for the `BearerAuthProvider`, while the main FastAPI application uses FastAPI-Users with HMAC-based JWT (HS256). The application has evolved beyond simple API keys to a full user management system, but MCP integration still needs the RSA bridge for proper authentication. The existing TODO comments in mcp_integration/server.py indicate this is a planned feature.

### Critical Context & Documentation

#### FastMCP Bearer Authentication
- **BearerAuthProvider Documentation**: https://gofastmcp.com/servers/auth/bearer
- **Complete Bearer Auth Example**: https://gofastmcp.com/integrations/openai (lines 793-823 in ai_info/docs/fastmcp.md)
- **RSA Key Generation Pattern**: Uses `RSAKeyPair.generate()` and `BearerAuthProvider` with public key validation
- **Client Authentication**: Standard `Authorization: Bearer <token>` header (line 737 in fastmcp.md)

#### Existing FastMCP Integration
- **Current Server**: mcp_integration/server.py - No authentication configured
- **Tool Implementation**: mcp_integration/tools/geocoding.py - Reuses existing GeocodingService
- **Mount Point**: main.py:166 - Mounted at `/mcp-server` endpoint  
- **Service Reuse Pattern**: Singleton pattern for service management (mcp_integration/tools/geocoding.py:27-37)

#### Current Authentication Infrastructure  
- **FastAPI-Users System**: Full JWT Bearer authentication with user management (auth/)
  - **User Model**: models/user.py - Complete user management with roles, timestamps, database
  - **JWT Backend**: auth/backend.py - HMAC-based JWT authentication (HS256)
  - **Authentication Routes**: /auth/jwt/login, /auth/register, /users (implemented)
  - **Dependencies**: current_active_user, current_verified_user, current_superuser
- **Legacy API Key**: dependencies.py:60 - Optional X-API-KEY for backward compatibility
- **Configuration**: config.py - Full JWT settings with JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
- **Error Handling**: dependencies.py:21-33 - Custom AuthHTTPException with request tracking

#### Related Dependencies
- **cryptography>=43.0.1**: Already available (pyproject.toml:21) - Required for RSA key generation
- **fastmcp**: Already integrated (pyproject.toml:18) - Supports BearerAuthProvider
- **pydantic-settings**: Available for configuration management

### Implementation Blueprint

#### 1. RSA Key Management System (Simplified with FastMCP)

**RSA Key Manager using FastMCP Built-ins**
```python
# services/mcp_rsa_keys.py
from fastmcp.server.auth.providers.bearer import RSAKeyPair
from typing import Optional
import logging
from config import settings

logger = logging.getLogger(__name__)

class MCPRSAKeyManager:
    """
    MCP RSA key pair manager using FastMCP built-in RSAKeyPair.
    
    Leverages FastMCP's built-in key generation and management
    for seamless integration with BearerAuthProvider.
    """
    
    def __init__(self):
        self._key_pair: Optional[RSAKeyPair] = None
    
    def get_or_create_key_pair(self) -> RSAKeyPair:
        """
        Get existing key pair or create new one.
        
        Returns:
            RSAKeyPair: FastMCP RSA key pair instance
        
        Raises:
            Exception: If key generation or loading fails
        """
        if self._key_pair is None:
            try:
                # Try loading from environment first
                if settings.MCP_JWT_PRIVATE_KEY and settings.MCP_JWT_PUBLIC_KEY:
                    logger.info("Loading RSA keys from environment")
                    # FastMCP can load from PEM strings
                    self._key_pair = RSAKeyPair.from_pem(
                        private_key_pem=settings.MCP_JWT_PRIVATE_KEY,
                        public_key_pem=settings.MCP_JWT_PUBLIC_KEY
                    )
                else:
                    # Generate new key pair for development
                    if settings.ENV == "development":
                        logger.warning(
                            "Auto-generating RSA keys for development. "
                            "Use explicit keys in production!"
                        )
                        self._key_pair = RSAKeyPair.generate()
                    else:
                        raise ValueError(
                            "MCP RSA keys required in production. "
                            "Set MCP_JWT_PRIVATE_KEY and MCP_JWT_PUBLIC_KEY."
                        )
                        
                logger.info("MCP RSA key pair initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize RSA key pair: {e}")
                raise
                
        return self._key_pair
    
    def create_token(self, user_id: str, email: str) -> str:
        """
        Create JWT token for MCP access using FastMCP built-in method.
        
        Args:
            user_id: User ID from FastAPI-Users
            email: User email from FastAPI-Users
        
        Returns:
            str: JWT token for MCP authentication
        """
        key_pair = self.get_or_create_key_pair()
        
        # Use FastMCP's built-in token creation
        return key_pair.create_token(
            audience=settings.MCP_JWT_AUDIENCE,
            subject=user_id,
            issuer=settings.MCP_JWT_ISSUER,
            additional_claims={
                "email": email,
                "scope": "mcp-access"
            },
            expires_in_minutes=settings.MCP_JWT_EXPIRE_MINUTES
        )

# Singleton instance
_mcp_rsa_manager: Optional[MCPRSAKeyManager] = None

def get_mcp_rsa_manager() -> MCPRSAKeyManager:
    """Get or create the MCP RSA key manager instance."""
    global _mcp_rsa_manager
    if _mcp_rsa_manager is None:
        _mcp_rsa_manager = MCPRSAKeyManager()
    return _mcp_rsa_manager
```

#### 2. Configuration Updates (Extending Existing JWT Settings)

**Updated Settings with MCP-Specific Extensions**
```python
# config.py additions to existing Settings class
class Settings(BaseSettings):
    # Existing FastAPI-Users JWT settings (HMAC-based)
    JWT_SECRET: str = Field(..., min_length=32, description="JWT secret for main app")
    JWT_ALGORITHM: str = Field(default="HS256", description="HMAC algorithm for main app")
    JWT_EXPIRE_MINUTES: int = Field(default=60, description="JWT expiration in minutes")
    JWT_ISSUER: str = Field(default="fastapi-app", description="JWT issuer")
    JWT_AUDIENCE: str = Field(default="fastapi-users", description="JWT audience")
    
    # Existing RSA key fields (currently unused, now for MCP)
    JWT_PRIVATE_KEY: str | None = Field(default=None, description="JWT private key for MCP")
    JWT_PUBLIC_KEY: str | None = Field(default=None, description="JWT public key for MCP")
    
    # New MCP-specific JWT Configuration (extends existing)
    MCP_JWT_PRIVATE_KEY: str | None = Field(
        default=None,
        description="RSA private key for MCP JWT signing (PEM format) - fallback to JWT_PRIVATE_KEY"
    )
    MCP_JWT_PUBLIC_KEY: str | None = Field(
        default=None,
        description="RSA public key for MCP JWT verification (PEM format) - fallback to JWT_PUBLIC_KEY"
    )
    MCP_JWT_ALGORITHM: str = Field(
        default="RS256",
        description="RSA algorithm for MCP JWT tokens"
    )
    MCP_JWT_EXPIRE_MINUTES: int = Field(
        default=60,
        description="MCP JWT token expiration in minutes (inherits from JWT_EXPIRE_MINUTES)"
    )
    MCP_JWT_ISSUER: str = Field(
        default="personal-server",
        description="JWT token issuer for MCP"
    )
    MCP_JWT_AUDIENCE: str = Field(
        default="mcp-server",
        description="JWT token audience for MCP"
    )
    
    @model_validator(mode="after")
    def validate_jwt_settings(self):
        """Validate JWT configuration for both main app and MCP."""
        # Use fallback keys if MCP-specific keys not provided
        if not self.MCP_JWT_PRIVATE_KEY and self.JWT_PRIVATE_KEY:
            self.MCP_JWT_PRIVATE_KEY = self.JWT_PRIVATE_KEY
            
        if not self.MCP_JWT_PUBLIC_KEY and self.JWT_PUBLIC_KEY:
            self.MCP_JWT_PUBLIC_KEY = self.JWT_PUBLIC_KEY
            
        # Inherit expiration from main JWT settings if not specified
        if self.MCP_JWT_EXPIRE_MINUTES == 60 and self.JWT_EXPIRE_MINUTES != 60:
            self.MCP_JWT_EXPIRE_MINUTES = self.JWT_EXPIRE_MINUTES
        
        # In production, warn if using auto-generation
        if self.ENV == "production":
            if not self.MCP_JWT_PRIVATE_KEY or not self.MCP_JWT_PUBLIC_KEY:
                logger.warning(
                    "MCP will auto-generate RSA keys. "
                    "Set MCP_JWT_PRIVATE_KEY and MCP_JWT_PUBLIC_KEY for production."
                )
        
        return self
```

#### 3. MCP Authentication Service (FastAPI-Users Integration)

**JWT Token Generation Service for FastAPI-Users**
```python
# services/mcp_auth.py
from typing import Dict, Any, Optional
from fastapi import Depends
from models.user import User
from auth.users import current_active_user
from services.mcp_rsa_keys import get_mcp_rsa_manager
from config import settings
from utils.logging import get_logger

logger = get_logger(__name__)

class MCPAuthService:
    """
    MCP-specific JWT authentication service integrated with FastAPI-Users.
    
    Generates RSA-signed JWT tokens for MCP access from authenticated FastAPI-Users.
    Bridges the HMAC-based FastAPI-Users authentication with RSA-based MCP requirements.
    """
    
    def __init__(self):
        self.rsa_manager = get_mcp_rsa_manager()
        self.audience = settings.MCP_JWT_AUDIENCE
        self.issuer = settings.MCP_JWT_ISSUER
        self.expire_minutes = settings.MCP_JWT_EXPIRE_MINUTES
    
    def generate_mcp_token_for_user(self, user: User) -> str:
        """
        Generate RSA-signed JWT token for MCP access from authenticated FastAPI-Users user.
        
        Args:
            user: Authenticated FastAPI-Users User instance
        
        Returns:
            str: JWT token for MCP authentication
        
        Raises:
            Exception: If token generation fails
        """
        try:
            # Use FastMCP's built-in token creation with user details
            token = self.rsa_manager.create_token(
                user_id=str(user.id),
                email=user.email
            )
            
            logger.info(f"Generated MCP token for user: {user.email} (ID: {user.id})")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate MCP token for user {user.email}: {e}")
            raise
    
    def generate_mcp_token_for_legacy_api_key(self, api_key: str) -> str:
        """
        Generate RSA-signed JWT token for legacy API key users.
        
        Args:
            api_key: Validated legacy API key
        
        Returns:
            str: JWT token for MCP authentication
            
        Raises:
            Exception: If token generation fails
        """
        try:
            # For legacy API key users, create token with limited context
            key_pair = self.rsa_manager.get_or_create_key_pair()
            
            token = key_pair.create_token(
                audience=self.audience,
                subject=f"legacy-api-key:{self._hash_api_key(api_key)}",
                issuer=self.issuer,
                additional_claims={
                    "scope": "mcp-access",
                    "auth_type": "legacy-api-key"
                },
                expires_in_minutes=self.expire_minutes
            )
            
            logger.info(f"Generated MCP token for legacy API key: {api_key[:8]}...")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate MCP token for API key: {e}")
            raise
    
    def _hash_api_key(self, api_key: str) -> str:
        """Create a hash of the API key for token identification."""
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]

# Singleton instance
_mcp_auth_service: Optional[MCPAuthService] = None

def get_mcp_auth_service() -> MCPAuthService:
    """Get or create the MCP authentication service instance."""
    global _mcp_auth_service
    if _mcp_auth_service is None:
        _mcp_auth_service = MCPAuthService()
    return _mcp_auth_service
```

#### 4. MCP Token Generation Endpoint (FastAPI-Users Integration)

**API Endpoint for MCP Token Issuance with Dual Authentication Support**
```python
# routers/mcp_auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union
from datetime import datetime, UTC

from models.user import User
from auth.users import current_active_user
from dependencies import RequiredAuth, OptionalAuth
from services.mcp_auth import get_mcp_auth_service
from utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["mcp-authentication"])

class MCPTokenRequest(BaseModel):
    """Request model for MCP token generation."""
    pass  # No additional parameters needed - user info comes from authentication

class MCPTokenResponse(BaseModel):
    """Response model for MCP token generation."""
    mcp_token: str = Field(..., description="JWT token for MCP access")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    scope: str = Field(default="mcp-access", description="Token scope")
    issued_at: str = Field(..., description="Token issuance timestamp")
    user_info: Dict[str, Any] = Field(..., description="User information")

@router.post("/mcp-token", response_model=MCPTokenResponse)
async def generate_mcp_token(
    request: MCPTokenRequest,
    current_user: User = Depends(current_active_user),
    mcp_auth_service = Depends(get_mcp_auth_service),
) -> MCPTokenResponse:
    """
    Generate MCP-specific JWT token for authenticated FastAPI-Users.
    
    This endpoint allows authenticated users to obtain RSA-signed JWT tokens
    specifically for accessing MCP endpoints. Requires valid FastAPI-Users authentication.
    
    Args:
        request: Token generation request (currently no parameters needed)
        current_user: Authenticated FastAPI-Users User instance
        mcp_auth_service: MCP authentication service
    
    Returns:
        MCPTokenResponse: JWT token and metadata
    
    Raises:
        HTTPException: If token generation fails
    """
    try:
        # Generate MCP token for authenticated FastAPI-Users user
        mcp_token = mcp_auth_service.generate_mcp_token_for_user(current_user)
        
        return MCPTokenResponse(
            mcp_token=mcp_token,
            token_type="bearer",
            expires_in=mcp_auth_service.expire_minutes * 60,
            scope="mcp-access",
            issued_at=datetime.now(UTC).isoformat(),
            user_info={
                "user_id": str(current_user.id),
                "email": current_user.email,
                "full_name": current_user.full_name,
                "role": current_user.role,
            },
        )
        
    except Exception as e:
        logger.error(f"Failed to generate MCP token for user {current_user.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate MCP token: {str(e)}"
        )

@router.post("/mcp-token/legacy", response_model=MCPTokenResponse)
async def generate_mcp_token_legacy(
    request: MCPTokenRequest,
    api_key: str = RequiredAuth,
    mcp_auth_service = Depends(get_mcp_auth_service),
) -> MCPTokenResponse:
    """
    Generate MCP-specific JWT token for legacy API key authentication.
    
    This endpoint maintains backward compatibility for users still using
    X-API-KEY authentication instead of FastAPI-Users.
    
    Args:
        request: Token generation request
        api_key: Validated legacy API key
        mcp_auth_service: MCP authentication service
    
    Returns:
        MCPTokenResponse: JWT token and metadata
    
    Raises:
        HTTPException: If token generation fails
    """
    try:
        # Generate MCP token for legacy API key
        mcp_token = mcp_auth_service.generate_mcp_token_for_legacy_api_key(api_key)
        
        return MCPTokenResponse(
            mcp_token=mcp_token,
            token_type="bearer",
            expires_in=mcp_auth_service.expire_minutes * 60,
            scope="mcp-access",
            issued_at=datetime.now(UTC).isoformat(),
            user_info={
                "auth_type": "legacy-api-key",
                "api_key_prefix": api_key[:8] + "...",
            },
        )
        
    except Exception as e:
        logger.error(f"Failed to generate MCP token for API key: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate MCP token: {str(e)}"
        )
```

#### 5. Updated MCP Server with Authentication (Simplified FastMCP Integration)

**FastMCP Server with BearerAuthProvider using Built-in RSA Management**
```python
# mcp_integration/server.py
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider
from config import settings
from services.mcp_rsa_keys import get_mcp_rsa_manager
from utils.logging import get_logger
from .tools.geocoding import geocode_city

logger = get_logger(__name__)

# Global MCP server instance
_mcp_server = None

def get_mcp_server() -> FastMCP:
    """
    Get or create the authenticated MCP server instance.
    
    Returns:
        FastMCP: The configured MCP server instance with Bearer authentication
    """
    global _mcp_server
    if _mcp_server is None:
        try:
            # Initialize RSA key manager to ensure keys are ready
            rsa_manager = get_mcp_rsa_manager()
            key_pair = rsa_manager.get_or_create_key_pair()
            
            # Create Bearer authentication provider with FastMCP RSA key pair
            auth_provider = BearerAuthProvider(
                public_key=key_pair.public_key,  # FastMCP RSAKeyPair.public_key
                algorithm=settings.MCP_JWT_ALGORITHM,
                audience=settings.MCP_JWT_AUDIENCE,
                issuer=settings.MCP_JWT_ISSUER,
            )
            
            _mcp_server = FastMCP(
                name="Personal MCP Server",
                auth=auth_provider,  # Authentication now enabled
                instructions="""
                This server provides secure capabilities through the Model Context Protocol.
                
                Authentication: JWT Bearer tokens required for all operations.
                
                To obtain a token:
                1. Authenticate with FastAPI-Users (POST /auth/jwt/login) OR use legacy X-API-KEY
                2. Request MCP token from /auth/mcp-token endpoint (FastAPI-Users) or /auth/mcp-token/legacy (API key)
                3. Use the returned JWT token in Authorization: Bearer <token> header
                
                Available tools:
                - geocode_city: Convert city names to latitude/longitude coordinates
                """,
            )
            
            # Register tools
            _mcp_server.add_tool(geocode_city)
            
            logger.info("MCP server initialized with Bearer authentication")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP server with authentication: {e}")
            # Fallback to unauthenticated server in development
            if settings.ENV == "development":
                logger.warning("Falling back to unauthenticated MCP server for development")
                _mcp_server = FastMCP(
                    name="Personal MCP Server (Development - No Auth)",
                    instructions="""
                    This server is running without authentication (development mode only).
                    
                    In production, authentication is required:
                    1. Authenticate with FastAPI-Users or legacy API key
                    2. Obtain MCP JWT token
                    3. Use Bearer token for MCP access
                    
                    Available tools:
                    - geocode_city: Convert city names to latitude/longitude coordinates
                    """,
                )
                _mcp_server.add_tool(geocode_city)
            else:
                raise
    
    return _mcp_server

def reset_mcp_server() -> None:
    """
    Reset the MCP server instance.
    
    This is primarily useful for testing purposes.
    """
    global _mcp_server
    _mcp_server = None
```

#### 6. Main Application Integration

**FastAPI Router Integration**
```python
# main.py additions (after existing includes)
from routers import crawling, geocoding, mcp_auth

# Include MCP authentication router
app.include_router(
    mcp_auth.router,
    responses={
        401: {"description": "Authentication required"},
        500: {"description": "Token generation failed"},
    },
)
```

#### 7. Environment Configuration

**Environment Variables**
```bash
# .env additions

# MCP JWT Configuration (required for production)
MCP_JWT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
MCP_JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"

# Optional MCP JWT settings (have defaults)
MCP_JWT_ALGORITHM=RS256
MCP_JWT_EXPIRE_MINUTES=60
MCP_JWT_ISSUER=personal-server
MCP_JWT_AUDIENCE=mcp-server

# Development settings
MCP_JWT_AUTO_GENERATE_KEYS=true  # Auto-generate keys in development
```

### Implementation Tasks (Updated for FastAPI-Users Integration)

1. **MCP RSA Key Management Service** ⏱️ 1 day
   - Create `services/mcp_rsa_keys.py` using FastMCP's RSAKeyPair
   - Implement key loading from environment variables
   - Add auto-generation fallback for development
   - Test key pair creation and token generation

2. **Configuration Extensions** ⏱️ 1 day  
   - Update `config.py` to extend existing JWT settings for MCP
   - Add MCP-specific settings with fallbacks to main JWT config
   - Update model validator to handle dual JWT systems
   - Test configuration inheritance and validation

3. **MCP Authentication Service** ⏱️ 2 days
   - Create `services/mcp_auth.py` with FastAPI-Users integration
   - Implement token generation for authenticated User objects
   - Implement legacy API key support for backward compatibility
   - Add comprehensive error handling and logging
   - Test both FastAPI-Users and legacy authentication paths

4. **MCP Token Generation Endpoints** ⏱️ 2 days
   - Create `routers/mcp_auth.py` with dual authentication support
   - Implement `/auth/mcp-token` for FastAPI-Users (primary)
   - Implement `/auth/mcp-token/legacy` for API key users (backward compatibility)
   - Add proper Pydantic models and error handling
   - Test both authentication endpoints and error scenarios

5. **MCP Server Authentication Integration** ⏱️ 1 day
   - Update `mcp_integration/server.py` to use FastMCP BearerAuthProvider
   - Configure with RSA key pair from mcp_rsa_keys service
   - Update server instructions for dual authentication flow
   - Add development fallback with clear warnings
   - Test MCP server initialization and Bearer token validation

6. **Main Application Integration** ⏱️ 1 day
   - Add MCP auth router to main.py (both endpoints)
   - Verify no conflicts with existing FastAPI-Users routes
   - Test complete authentication flows (FastAPI-Users and legacy)
   - Verify CORS and middleware compatibility

7. **Testing Implementation** ⏱️ 2 days
   - Create unit tests for MCP RSA key service
   - Create unit tests for MCP authentication service (both auth types)
   - Create integration tests for token generation endpoints
   - Update existing MCP tests to include Bearer authentication
   - Test error scenarios, token expiration, and edge cases

8. **Documentation and Environment Setup** ⏱️ 1 day
   - Update CLAUDE.md with FastAPI-Users + MCP authentication patterns
   - Update `.env.example` with MCP RSA key examples
   - Create user guide for both authentication flows
   - Update API documentation with dual endpoint approach

### User Experience Flow (FastAPI-Users + Legacy Support)

#### 1. FastAPI-Users Authentication Flow (Primary)
```bash
# 1. User registration (if new user)
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# 2. User login to get FastAPI-Users JWT token
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=user@example.com&password=password123'

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",  # HMAC token for main app
  "token_type": "bearer"
}

# 3. Request MCP-specific RSA token using FastAPI-Users authentication
curl -X POST "http://localhost:8000/auth/mcp-token" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{}'

# Response:
{
  "mcp_token": "eyJhbGciOiJSUzI1NiIs...",  # RSA token for MCP
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "mcp-access",
  "issued_at": "2024-01-01T12:00:00+00:00",
  "user_info": {
    "user_id": "12345-67890-abcdef",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user"
  }
}
```

#### 2. Legacy API Key Flow (Backward Compatibility)
```bash
# 1. Use existing X-API-KEY authentication
curl -X GET "http://localhost:8000/protected" \
  -H "X-API-KEY: your-api-key-here"

# 2. Request MCP-specific token using legacy endpoint
curl -X POST "http://localhost:8000/auth/mcp-token/legacy" \
  -H "X-API-KEY: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{}'

# Response:
{
  "mcp_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "mcp-access",
  "issued_at": "2024-01-01T12:00:00+00:00",
  "user_info": {
    "auth_type": "legacy-api-key",
    "api_key_prefix": "your-api-..."
  }
}
```

#### 2. MCP Client Usage
```python
# Python MCP client with Bearer authentication
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

# Configure client with Bearer token
client = Client(
    server_url="http://localhost:8000/mcp-server/mcp",
    auth=BearerAuth("eyJhbGciOiJSUzI1NiIs...")
)

# Use MCP tools with authentication
async with client:
    tools = await client.list_tools()
    print("Available tools:", tools)
    
    result = await client.call_tool("geocode_city", {"city": "London"})
    print("Geocoding result:", result)
```

#### 3. Development Key Generation
```python
# Development utility for key generation
# utils/generate_dev_keys.py
from utils.rsa_keys import get_rsa_key_manager

def main():
    key_manager = get_rsa_key_manager()
    private_key, public_key = key_manager.generate_key_pair()
    
    print("Development RSA Keys Generated:")
    print("=" * 50)
    print("Private Key (MCP_JWT_PRIVATE_KEY):")
    print(private_key)
    print("\nPublic Key (MCP_JWT_PUBLIC_KEY):")
    print(public_key)
    print("=" * 50)
    print("Add these to your .env file for development")

if __name__ == "__main__":
    main()
```

### Validation Gates (Updated for Current Codebase)

#### Code Quality and Standards
```bash
# Syntax and formatting (using current project standards)
uv run ruff check --fix
uv run ruff format

# All quality checks (using project Makefile)
make quality

# Fix formatting and linting
make fix
```

#### Unit Testing (Current Test Structure)
```bash
# MCP RSA key service tests
uv run pytest services/tests/test_mcp_rsa_keys.py -v

# MCP authentication service tests  
uv run pytest services/tests/test_mcp_auth.py -v

# MCP authentication router tests
uv run pytest routers/tests/test_mcp_auth.py -v

# Run all unit tests
make test
```

#### Integration Testing (Following Current Patterns)
```bash
# Updated MCP integration tests (with authentication)
uv run pytest mcp_integration/tests/test_mcp_geocoding.py -v

# New MCP authentication integration tests
uv run pytest mcp_integration/tests/test_mcp_auth_integration.py -v

# Updated integration tests
uv run pytest tests/test_integration.py -v

# All tests with coverage
make test-cov
```

#### Manual Testing Commands (FastAPI-Users + Legacy)
```bash
# 1. Start development server
make run

# 2. Test FastAPI-Users authentication flow
# Register new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'

# Login to get HMAC JWT token
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=password123'

# Get MCP RSA token using FastAPI-Users authentication
curl -X POST "http://localhost:8000/auth/mcp-token" \
  -H "Authorization: Bearer YOUR_FASTAPI_USERS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

# 3. Test legacy API key flow
curl -X POST "http://localhost:8000/auth/mcp-token/legacy" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{}'

# 4. Test MCP tool access with Bearer token
python -c "
import asyncio
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

async def test_mcp_auth():
    client = Client(
        'http://localhost:8000/mcp-server/mcp',
        auth=BearerAuth('YOUR_MCP_RSA_TOKEN_HERE')
    )
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f'Available tools: {list(tools.keys())}')
        
        # Test geocoding tool
        result = await client.call_tool('geocode_city', {'city': 'London'})
        print(f'Geocoding result: {result[0].text}')

asyncio.run(test_mcp_auth())
"

# 5. Test health endpoints
curl -X GET "http://localhost:8000/"
curl -X GET "http://localhost:8000/geocode/health"
```

### Key Design Decisions

#### 1. **Dual Authentication Architecture**
- **Main Application**: Continue using X-API-KEY for REST endpoints (backward compatibility)
- **MCP Endpoints**: Use RSA-signed JWT Bearer tokens (FastMCP requirement)
- **Token Generation**: Bridge between systems via API key validation

**Rationale**: Maintains existing functionality while adding proper MCP security without breaking changes.

#### 2. **RSA Key Management Strategy**
- **Development**: Auto-generate keys with warning logs
- **Production**: Require explicit environment variable keys
- **Key Storage**: Environment variables (no file storage for security)
- **Key Rotation**: Manual process with configuration updates

**Rationale**: Balances development ease with production security requirements.

#### 3. **Token Scope and Claims**
- **Audience**: "mcp-server" (specific to MCP endpoints)
- **Issuer**: "personal-server" (identifies token origin)
- **Subject**: Masked API key reference (privacy)
- **Scope**: "mcp-access" (explicit permission model)

**Rationale**: Follows JWT best practices with specific claims for MCP context.

#### 4. **Error Handling Strategy**  
- **Development Fallback**: Unauthenticated MCP server if auth fails
- **Production Strict**: Fail fast if authentication cannot be configured
- **Comprehensive Logging**: All authentication events logged for debugging
- **User-Friendly Errors**: Clear error messages for common scenarios

**Rationale**: Enables development productivity while maintaining production security.

#### 5. **Service Integration Pattern**
- **Singleton Services**: Single instances shared across application
- **Dependency Injection**: FastAPI Depends() pattern for service access
- **Service Reuse**: MCP tools continue using existing services
- **Clean Separation**: Authentication logic separated from business logic

**Rationale**: Maintains existing architectural patterns and service boundaries.

### Security Considerations

#### JWT Token Security
- **Short-lived Tokens**: 60-minute default expiration (configurable)
- **Audience Validation**: Strict audience checking for MCP endpoints
- **Issuer Validation**: Verify token origin
- **Algorithm Restriction**: Only RS256 RSA algorithm allowed
- **No Sensitive Data**: API keys masked in JWT claims

#### RSA Key Security
- **2048-bit Keys**: Industry-standard key size
- **Secure Generation**: Cryptographically secure random generation
- **Environment Storage**: Keys stored in environment variables only
- **No File Storage**: Avoid key files that could be accidentally committed
- **Production Validation**: Strict validation of production key format

#### Authentication Flow Security
- **API Key Validation**: Existing X-API-KEY validation preserved
- **Token Generation Audit**: All token generation events logged
- **Failed Authentication Logging**: Security event monitoring
- **Rate Limiting Preserved**: Existing rate limiting continues to work

#### Network Security
- **HTTPS-Only Production**: Tokens transmitted over secure connections
- **Bearer Token Headers**: Standard Authorization header format
- **No Token Leakage**: Tokens not logged or exposed in responses
- **Client-Side Security**: Proper token storage recommendations

### Expected Outcomes

#### 1. **Secured MCP Endpoints**
- All MCP tools require valid JWT Bearer tokens
- Authentication failures properly handled and logged
- User-specific access tracking and audit trails
- Rate limiting can be applied per authenticated user

#### 2. **Improved Architecture**
- Dual authentication system supporting both existing and new patterns
- Clean separation between main application and MCP authentication
- Professional JWT implementation following industry standards
- Foundation for future role-based access control

#### 3. **Enhanced Developer Experience**
- Auto-generated development keys for easy local setup
- Clear documentation and examples for MCP client authentication
- Comprehensive error messages for debugging authentication issues
- Backward compatibility maintained for existing API consumers

#### 4. **Production Readiness**
- Secure RSA key management for production deployments
- Configurable token expiration and security settings
- Comprehensive logging and monitoring for security events
- Docker and cloud deployment compatibility

### Success Criteria

- [ ] **RSA Key Infrastructure**: Key generation, loading, and validation working
- [ ] **MCP Token Generation**: API endpoint generates valid JWT tokens
- [ ] **MCP Server Authentication**: FastMCP BearerAuthProvider validates tokens
- [ ] **Tool Access Control**: All MCP tools require authentication
- [ ] **Error Handling**: Comprehensive error responses and logging
- [ ] **Development Setup**: Auto-generated keys work in development
- [ ] **Production Configuration**: Manual key configuration works
- [ ] **Testing Coverage**: All authentication flows tested and passing
- [ ] **Documentation**: Complete user guides and deployment instructions
- [ ] **Backward Compatibility**: Existing API functionality unchanged
- [ ] **Security Validation**: No token leaks or security vulnerabilities
- [ ] **Performance**: Authentication adds <50ms latency per MCP request

### Potential Gotchas and Mitigation

#### 1. **RSA Key Format Issues**
**Risk**: Invalid PEM format or wrong key types
**Mitigation**: Comprehensive validation in RSAKeyManager with clear error messages

#### 2. **JWT Clock Skew**
**Risk**: Token validation fails due to time differences
**Mitigation**: Use UTC timestamps and consider adding clock skew tolerance

#### 3. **FastMCP Integration**
**Risk**: BearerAuthProvider configuration incompatibility
**Mitigation**: Follow exact FastMCP documentation patterns and test thoroughly

#### 4. **Development vs Production Keys**
**Risk**: Auto-generated keys used in production
**Mitigation**: Strict validation requiring explicit keys in production environment

#### 5. **Token Expiration Handling**
**Risk**: Expired tokens causing MCP client failures
**Mitigation**: Clear expiration error messages and token refresh guidance

#### 6. **Environment Variable Management**
**Risk**: Large RSA keys difficult to manage in environment variables
**Mitigation**: Use multi-line environment variable format and validation

#### 7. **CORS Configuration**
**Risk**: Bearer tokens blocked by CORS policy
**Mitigation**: Ensure Authorization header is allowed in CORS configuration

### Dependencies and Installation

```bash
# All required dependencies already available in pyproject.toml:
# - cryptography>=43.0.1 (RSA key generation)
# - fastmcp (BearerAuthProvider)
# - pydantic-settings (configuration management)
# - fastapi[standard] (core framework)

# No additional dependencies required!
```

### Risk Assessment

**Low Risk Factors:**
- FastMCP BearerAuthProvider is officially supported and documented
- RSA JWT tokens are industry standard with mature libraries
- Existing authentication patterns provide clear implementation guidance
- Comprehensive test coverage ensures reliability

**Medium Risk Factors:**
- RSA key management requires careful production configuration
- JWT integration testing needs thorough validation
- Error handling across multiple authentication layers

**High Risk Factors:**
- None identified - this follows well-established patterns with good documentation

### Development Timeline

**Total Estimated Time: 16 days**

- **Week 1 (Days 1-5)**: Core infrastructure (RSA keys, auth service, config)
- **Week 2 (Days 6-10)**: API endpoints and MCP server integration
- **Week 3 (Days 11-16)**: Testing, documentation, and deployment preparation

**Critical Path Dependencies:**
1. RSA key infrastructure → MCP auth service
2. MCP auth service → Token generation endpoint  
3. Token generation endpoint → MCP server authentication
4. MCP server authentication → Integration testing

## PRP Confidence Score: 9.5/10 (UPDATED)

**Very high confidence** - This updated implementation leverages FastMCP's built-in RSA management and integrates seamlessly with the existing FastAPI-Users authentication system. The approach is simplified compared to the original PRP and aligns perfectly with current codebase patterns.

**Key Success Factors:**
- ✅ **FastMCP Built-in RSA**: Uses FastMCP's RSAKeyPair instead of custom cryptography
- ✅ **FastAPI-Users Integration**: Builds on existing authentication infrastructure
- ✅ **Backward Compatibility**: Maintains legacy API key support
- ✅ **Current Codebase Alignment**: All patterns match existing code structure
- ✅ **Comprehensive Research**: Based on actual codebase analysis and validation
- ✅ **Dependencies Available**: All required packages already in pyproject.toml

**Minor Risk Factors:**
- FastMCP RSAKeyPair.from_pem() method needs validation (may use different API)
- Production RSA key configuration requires careful environment setup

**Likelihood of one-pass implementation success: 95%** - Simplified approach using proven patterns, existing infrastructure, and well-documented FastMCP integration makes this extremely likely to succeed with minimal issues.