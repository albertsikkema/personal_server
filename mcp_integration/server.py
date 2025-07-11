"""
FastMCP Server Configuration.

This module provides the main FastMCP server instance that exposes geocoding
functionality through the Model Context Protocol.
"""

from fastmcp import FastMCP

from .tools.geocoding import geocode_city

# Global MCP server instance
_mcp_server = None


def get_mcp_server() -> FastMCP:
    """
    Get or create the MCP server instance.

    Returns:
        FastMCP: The configured MCP server instance
    """
    global _mcp_server
    if _mcp_server is None:
        _mcp_server = FastMCP(
            name="Personal MCP Server",
            instructions="""
            This server provides capabilities through the Model Context Protocol.
            Use the geocode_city tool to convert city names to geographic coordinates.
            
            Available tools:
            - geocode_city: Convert city names to latitude/longitude coordinates
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
