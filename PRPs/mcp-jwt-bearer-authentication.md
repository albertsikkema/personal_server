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
FastMCP framework requires RSA-based JWT tokens for the `BearerAuthProvider`, while the main FastAPI application uses HMAC-based JWT with simple API keys. The existing TODO comments in mcp_integration/server.py indicate this is a planned feature.

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
- **API Key System**: dependencies.py:35-69 - X-API-KEY header authentication
- **Configuration**: config.py:14-19 - Single API_KEY setting
- **Error Handling**: dependencies.py:21-33 - Custom AuthHTTPException with request tracking
- **Dependencies**: RequiredAuth = Depends(verify_api_key) (line 107)

#### Related Dependencies
- **cryptography>=43.0.1**: Already available (pyproject.toml:21) - Required for RSA key generation
- **fastmcp**: Already integrated (pyproject.toml:18) - Supports BearerAuthProvider
- **pydantic-settings**: Available for configuration management

### Implementation Blueprint

#### 1. RSA Key Management System

**RSA Key Generation Utility**
```python
# utils/rsa_keys.py
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class RSAKeyManager:
    """
    RSA key pair manager for JWT signing and verification.
    
    Handles generation, storage, and retrieval of RSA key pairs
    required for MCP JWT authentication.
    """
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def generate_key_pair(self) -> Tuple[str, str]:
        """
        Generate RSA key pair for JWT signing.
        
        Returns:
            Tuple[str, str]: (private_key_pem, public_key_pem)
        
        Raises:
            Exception: If key generation fails
        """
        try:
            # Generate private key (2048-bit RSA)
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # Serialize private key to PEM format
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Serialize public key to PEM format
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            logger.info("RSA key pair generated successfully")
            return private_pem.decode(), public_pem.decode()
            
        except Exception as e:
            logger.error(f"Failed to generate RSA key pair: {e}")
            raise

    def load_keys_from_env(self, private_key_pem: str, public_key_pem: str) -> None:
        """
        Load RSA keys from environment variables.
        
        Args:
            private_key_pem: Private key in PEM format
            public_key_pem: Public key in PEM format
        
        Raises:
            ValueError: If keys are invalid or malformed
        """
        try:
            # Validate private key format
            serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None,
            )
            
            # Validate public key format  
            serialization.load_pem_public_key(
                public_key_pem.encode()
            )
            
            self.private_key = private_key_pem
            self.public_key = public_key_pem
            logger.info("RSA keys loaded from environment")
            
        except Exception as e:
            logger.error(f"Invalid RSA keys: {e}")
            raise ValueError(f"Invalid RSA key format: {e}")

# Singleton instance
_rsa_key_manager: RSAKeyManager | None = None

def get_rsa_key_manager() -> RSAKeyManager:
    """Get or create the RSA key manager instance."""
    global _rsa_key_manager
    if _rsa_key_manager is None:
        _rsa_key_manager = RSAKeyManager()
    return _rsa_key_manager
```

#### 2. Configuration Updates

**Updated Settings with RSA Key Support**
```python
# config.py additions
from typing import Optional
from pydantic import Field, model_validator

class Settings(BaseSettings):
    # Existing settings...
    API_KEY: str = Field(..., min_length=8, description="API key for authentication")
    
    # New MCP JWT Configuration  
    MCP_JWT_PRIVATE_KEY: Optional[str] = Field(
        default=None,
        description="RSA private key for MCP JWT signing (PEM format)"
    )
    MCP_JWT_PUBLIC_KEY: Optional[str] = Field(
        default=None,
        description="RSA public key for MCP JWT verification (PEM format)"
    )
    MCP_JWT_ALGORITHM: str = Field(
        default="RS256",
        description="RSA algorithm for MCP JWT tokens"
    )
    MCP_JWT_EXPIRE_MINUTES: int = Field(
        default=60,
        description="MCP JWT token expiration in minutes"
    )
    MCP_JWT_ISSUER: str = Field(
        default="personal-server",
        description="JWT token issuer"
    )
    MCP_JWT_AUDIENCE: str = Field(
        default="mcp-server",
        description="JWT token audience"
    )
    
    # Development settings
    MCP_JWT_AUTO_GENERATE_KEYS: bool = Field(
        default=True,
        description="Auto-generate RSA keys in development mode"
    )
    
    @model_validator(mode="after")
    def validate_mcp_jwt_config(self):
        """Validate MCP JWT configuration."""
        # In production, require explicit keys
        if self.ENV == "production":
            if not self.MCP_JWT_PRIVATE_KEY or not self.MCP_JWT_PUBLIC_KEY:
                if not self.MCP_JWT_AUTO_GENERATE_KEYS:
                    raise ValueError(
                        "MCP_JWT_PRIVATE_KEY and MCP_JWT_PUBLIC_KEY are required in production"
                    )
        
        # Validate key format if provided
        if self.MCP_JWT_PRIVATE_KEY and self.MCP_JWT_PUBLIC_KEY:
            try:
                from utils.rsa_keys import get_rsa_key_manager
                key_manager = get_rsa_key_manager()
                key_manager.load_keys_from_env(
                    self.MCP_JWT_PRIVATE_KEY,
                    self.MCP_JWT_PUBLIC_KEY
                )
            except Exception as e:
                raise ValueError(f"Invalid MCP JWT keys: {e}")
        
        return self
```

#### 3. MCP Authentication Service

**JWT Token Generation and Validation Service**
```python
# services/mcp_auth.py
import jwt
from datetime import datetime, timedelta, UTC
from typing import Dict, Any, Optional
from config import settings
from utils.rsa_keys import get_rsa_key_manager
from utils.logging import get_logger

logger = get_logger(__name__)

class MCPAuthService:
    """
    MCP-specific JWT authentication service.
    
    Handles JWT token generation and validation for MCP endpoints
    using RSA key pairs, separate from the main application's API key authentication.
    """
    
    def __init__(self):
        self.key_manager = get_rsa_key_manager()
        self.algorithm = settings.MCP_JWT_ALGORITHM
        self.issuer = settings.MCP_JWT_ISSUER
        self.audience = settings.MCP_JWT_AUDIENCE
        self.expire_minutes = settings.MCP_JWT_EXPIRE_MINUTES
        
        # Initialize keys
        self._ensure_keys_available()
    
    def _ensure_keys_available(self) -> None:
        """Ensure RSA keys are available for JWT operations."""
        try:
            # Load from environment if provided
            if settings.MCP_JWT_PRIVATE_KEY and settings.MCP_JWT_PUBLIC_KEY:
                self.key_manager.load_keys_from_env(
                    settings.MCP_JWT_PRIVATE_KEY,
                    settings.MCP_JWT_PUBLIC_KEY
                )
                logger.info("MCP JWT keys loaded from environment")
                return
            
            # Auto-generate in development
            if settings.MCP_JWT_AUTO_GENERATE_KEYS:
                private_key, public_key = self.key_manager.generate_key_pair()
                self.key_manager.private_key = private_key
                self.key_manager.public_key = public_key
                logger.warning(
                    "Auto-generated MCP JWT keys for development. "
                    "Use explicit keys in production!"
                )
                return
            
            raise ValueError("No MCP JWT keys available and auto-generation disabled")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP JWT keys: {e}")
            raise
    
    def generate_mcp_token(self, api_key: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate RSA-signed JWT token for MCP access.
        
        Args:
            api_key: The validated API key from main application
            user_context: Optional user context information
        
        Returns:
            str: JWT token for MCP authentication
        
        Raises:
            Exception: If token generation fails
        """
        try:
            now = datetime.now(UTC)
            
            # Create JWT payload
            payload = {
                "sub": f"api-key:{api_key[:8]}...",  # Subject (masked API key)
                "iat": now,  # Issued at
                "exp": now + timedelta(minutes=self.expire_minutes),  # Expiration
                "aud": self.audience,  # Audience
                "iss": self.issuer,  # Issuer
                "scope": "mcp-access",  # Token scope
                "api_key_hash": self._hash_api_key(api_key),  # API key verification
            }
            
            # Add user context if provided
            if user_context:
                payload["user_context"] = user_context
            
            # Sign with RSA private key
            token = jwt.encode(
                payload,
                self.key_manager.private_key,
                algorithm=self.algorithm
            )
            
            logger.info(f"Generated MCP token for API key {api_key[:8]}...")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate MCP token: {e}")
            raise
    
    def verify_mcp_token(self, token: str) -> Dict[str, Any]:
        """
        Verify RSA-signed JWT token for MCP access.
        
        Args:
            token: JWT token to verify
        
        Returns:
            Dict[str, Any]: Decoded token payload
        
        Raises:
            jwt.InvalidTokenError: If token is invalid
            jwt.ExpiredSignatureError: If token is expired
        """
        try:
            # Decode and verify JWT token
            payload = jwt.decode(
                token,
                self.key_manager.public_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                    "verify_iss": True,
                }
            )
            
            logger.info(f"Verified MCP token for subject: {payload.get('sub')}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("MCP token expired")
            raise
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid MCP token: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to verify MCP token: {e}")
            raise
    
    def _hash_api_key(self, api_key: str) -> str:
        """Create a hash of the API key for token validation."""
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

#### 4. MCP Token Generation Endpoint

**API Endpoint for MCP Token Issuance**
```python
# routers/mcp_auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, UTC

from dependencies import RequiredAuth
from services.mcp_auth import get_mcp_auth_service
from utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["mcp-authentication"])

class MCPTokenRequest(BaseModel):
    """Request model for MCP token generation."""
    user_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional user context information"
    )

class MCPTokenResponse(BaseModel):
    """Response model for MCP token generation."""
    mcp_token: str = Field(..., description="JWT token for MCP access")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    scope: str = Field(default="mcp-access", description="Token scope")
    issued_at: str = Field(..., description="Token issuance timestamp")

@router.post("/mcp-token", response_model=MCPTokenResponse)
async def generate_mcp_token(
    request: MCPTokenRequest,
    api_key: str = RequiredAuth,
    mcp_auth_service = Depends(get_mcp_auth_service),
) -> MCPTokenResponse:
    """
    Generate MCP-specific JWT token for authenticated API key holders.
    
    This endpoint allows users with valid API keys to obtain JWT tokens
    specifically for accessing MCP endpoints. The token is signed with
    RSA keys and includes proper audience and issuer claims.
    
    Args:
        request: Token generation request with optional user context
        api_key: Validated API key from RequiredAuth dependency
        mcp_auth_service: MCP authentication service
    
    Returns:
        MCPTokenResponse: JWT token and metadata
    
    Raises:
        HTTPException: If token generation fails
    """
    try:
        # Generate MCP token using validated API key
        mcp_token = mcp_auth_service.generate_mcp_token(
            api_key=api_key,
            user_context=request.user_context
        )
        
        return MCPTokenResponse(
            mcp_token=mcp_token,
            token_type="bearer",
            expires_in=mcp_auth_service.expire_minutes * 60,
            scope="mcp-access",
            issued_at=datetime.now(UTC).isoformat(),
        )
        
    except Exception as e:
        logger.error(f"Failed to generate MCP token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate MCP token: {str(e)}"
        )

@router.get("/mcp-token/verify")
async def verify_mcp_token(
    token: str,
    mcp_auth_service = Depends(get_mcp_auth_service),
) -> Dict[str, Any]:
    """
    Verify MCP JWT token and return payload information.
    
    This endpoint is primarily for debugging and testing purposes.
    
    Args:
        token: JWT token to verify
        mcp_auth_service: MCP authentication service
    
    Returns:
        Dict[str, Any]: Token payload if valid
    
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = mcp_auth_service.verify_mcp_token(token)
        return {
            "valid": True,
            "payload": payload,
            "message": "Token is valid"
        }
        
    except Exception as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
```

#### 5. Updated MCP Server with Authentication

**FastMCP Server with BearerAuthProvider Integration**
```python
# mcp_integration/server.py
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider
from config import settings
from services.mcp_auth import get_mcp_auth_service
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
            # Initialize authentication service to ensure keys are ready
            auth_service = get_mcp_auth_service()
            
            # Create Bearer authentication provider with RSA public key
            auth_provider = BearerAuthProvider(
                public_key=auth_service.key_manager.public_key,
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
                1. Authenticate with the main API using X-API-KEY header
                2. Request MCP token from /auth/mcp-token endpoint
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
                logger.warning("Falling back to unauthenticated MCP server")
                _mcp_server = FastMCP(
                    name="Personal MCP Server (Unauthenticated)",
                    instructions="""
                    This server is running without authentication (development mode).
                    
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

### Implementation Tasks (Execution Order)

1. **RSA Key Infrastructure** ⏱️ 2 days
   - Create `utils/rsa_keys.py` with RSAKeyManager class
   - Implement key generation, loading, and validation 
   - Add comprehensive error handling and logging
   - Test key generation and PEM format validation

2. **Configuration Updates** ⏱️ 1 day
   - Update `config.py` with MCP JWT settings
   - Add model validator for production key requirements
   - Update `.env.example` with RSA key placeholders
   - Test configuration loading and validation

3. **MCP Authentication Service** ⏱️ 3 days
   - Create `services/mcp_auth.py` with MCPAuthService class
   - Implement JWT token generation with RSA signing
   - Implement JWT token verification with audience/issuer validation
   - Add singleton pattern and dependency injection support
   - Test token generation, verification, and error handling

4. **MCP Token API Endpoint** ⏱️ 2 days
   - Create `routers/mcp_auth.py` with token generation endpoint
   - Implement Pydantic models for request/response
   - Add proper error handling and logging
   - Integrate with existing RequiredAuth dependency
   - Test endpoint functionality and error scenarios

5. **MCP Server Authentication Integration** ⏱️ 2 days
   - Update `mcp_integration/server.py` to use BearerAuthProvider
   - Configure FastMCP with RSA public key validation
   - Add fallback mechanism for development environment
   - Update server instructions with authentication guidance
   - Test MCP server initialization and tool access

6. **Main Application Integration** ⏱️ 1 day
   - Add MCP auth router to main.py
   - Update CORS configuration if necessary
   - Verify no conflicts with existing routes
   - Test complete authentication flow

7. **Testing Implementation** ⏱️ 3 days
   - Create unit tests for RSA key management
   - Create unit tests for MCP authentication service
   - Create integration tests for token generation endpoint
   - Create integration tests for MCP server authentication
   - Update existing MCP tests to use Bearer tokens
   - Test error scenarios and edge cases

8. **Documentation and Deployment** ⏱️ 2 days
   - Update CLAUDE.md with new authentication patterns
   - Create user guide for MCP authentication flow
   - Update API documentation with new endpoints
   - Create deployment guide for production key management
   - Update README.md with MCP authentication instructions

### User Experience Flow

#### 1. Token Generation Flow
```bash
# 1. Authenticate with main application (existing flow)
curl -X GET "http://localhost:8000/protected" \
  -H "X-API-KEY: your-api-key-here"

# 2. Request MCP-specific token
curl -X POST "http://localhost:8000/auth/mcp-token" \
  -H "X-API-KEY: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{}'

# Response:
{
  "mcp_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "mcp-access",
  "issued_at": "2024-01-01T12:00:00+00:00"
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

### Validation Gates

#### Code Quality and Standards
```bash
# Syntax and formatting
uv run ruff check --fix .
uv run ruff format .

# Type checking (if mypy is configured)
uv run mypy services/mcp_auth.py utils/rsa_keys.py
```

#### Unit Testing
```bash
# RSA key management tests
uv run pytest utils/tests/test_rsa_keys.py -v

# MCP authentication service tests  
uv run pytest services/tests/test_mcp_auth.py -v

# MCP authentication endpoint tests
uv run pytest routers/tests/test_mcp_auth.py -v
```

#### Integration Testing
```bash
# MCP server authentication integration
uv run pytest mcp_integration/tests/test_mcp_auth_integration.py -v

# Complete authentication flow testing
uv run pytest tests/test_mcp_authentication_flow.py -v

# All tests
uv run pytest --cov=. -v
```

#### Manual Testing Commands
```bash
# 1. Test key generation
python utils/generate_dev_keys.py

# 2. Test MCP token generation
curl -X POST "http://localhost:8000/auth/mcp-token" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{}'

# 3. Test MCP tool access with Bearer token
python -c "
import asyncio
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

async def test_mcp_auth():
    client = Client(
        'http://localhost:8000/mcp-server/mcp',
        auth=BearerAuth('YOUR_JWT_TOKEN_HERE')
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

# 4. Test token verification
curl -X GET "http://localhost:8000/auth/mcp-token/verify?token=YOUR_JWT_TOKEN"
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

## PRP Confidence Score: 9/10

**High confidence** - This implementation follows well-established JWT and FastMCP patterns with comprehensive documentation. The existing codebase provides clear patterns, and all required dependencies are already available. The dual authentication approach maintains backward compatibility while adding proper MCP security.

**Risk factors preventing 10/10:**
- RSA key management requires careful production setup
- FastMCP integration testing needs validation
- JWT token lifecycle management across dual authentication systems

**Likelihood of one-pass implementation success: 85%** - Well-documented patterns, existing codebase compatibility, detailed implementation steps, and comprehensive validation gates make this highly likely to succeed with minimal rework.