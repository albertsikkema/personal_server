"""
FastMCP Server Configuration.

This module provides the main FastMCP server instance that exposes geocoding
functionality through the Model Context Protocol with JWT Bearer authentication.
"""

from fastmcp import FastMCP

from .tools.geocoding import geocode_city

# Global MCP server instance
_mcp_server = None


def get_mcp_server() -> FastMCP:
    """
    Get or create the MCP server instance.

    Note: JWT Bearer authentication for MCP is temporarily disabled due to
    BearerAuthProvider requiring RSA keys instead of HMAC secrets. This will
    be implemented in a follow-up with proper RSA key generation.

    Returns:
        FastMCP: The configured MCP server instance
    """
    global _mcp_server
    if _mcp_server is None:
        # TODO: Implement JWT Bearer authentication with RSA keys
        # The BearerAuthProvider requires public_key (RSA) not secret (HMAC)
        # For now, MCP server runs without authentication

        _mcp_server = FastMCP(
            name="Personal MCP Server",
            # auth=auth_provider,  # Disabled until RSA keys are implemented
            instructions="""
            This server provides capabilities through the Model Context Protocol.
            
            Available tools:
            - geocode_city: Convert city names to latitude/longitude coordinates
            
            Note: Authentication is temporarily disabled. In production, this server
            should be protected with JWT Bearer token authentication using RSA keys.
            """,
        )

        # Register the geocoding tool
        _mcp_server.add_tool(geocode_city)

    return _mcp_server


def reset_mcp_server() -> None:
    """
    Reset the MCP server instance.

    This is primarily useful for testing purposes.
    """
    global _mcp_server
    _mcp_server = None
