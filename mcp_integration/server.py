"""
FastMCP Server Configuration.

This module provides the main FastMCP server instance that exposes geocoding
functionality through the Model Context Protocol with JWT Bearer authentication.
"""

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
                logger.warning(
                    "Falling back to unauthenticated MCP server for development"
                )
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
