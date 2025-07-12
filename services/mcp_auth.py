"""
MCP Authentication Service.

This module provides MCP-specific JWT authentication service integrated with FastAPI-Users.
Generates RSA-signed JWT tokens for MCP access from authenticated FastAPI-Users.
"""

from config import settings
from models.user import User
from services.mcp_rsa_keys import get_mcp_rsa_manager
from utils.logging import get_logger

logger = get_logger(__name__)


class MCPAuthService:
    """
    MCP-specific JWT authentication service integrated with FastAPI-Users.

    Generates RSA-signed JWT tokens for MCP access from authenticated FastAPI-Users.
    Bridges the HMAC-based FastAPI-Users authentication with RSA-based MCP requirements.
    """

    def __init__(self):
        """Initialize the MCP authentication service."""
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
                user_id=str(user.id), email=user.email
            )

            logger.info(f"Generated MCP token for user: {user.email} (ID: {user.id})")
            return token

        except Exception as e:
            logger.error(f"Failed to generate MCP token for user {user.email}: {e}")
            raise


# Singleton instance
_mcp_auth_service: MCPAuthService | None = None


def get_mcp_auth_service() -> MCPAuthService:
    """
    Get or create the MCP authentication service instance.

    Returns:
        MCPAuthService: The singleton MCP authentication service instance
    """
    global _mcp_auth_service
    if _mcp_auth_service is None:
        _mcp_auth_service = MCPAuthService()
    return _mcp_auth_service


def reset_mcp_auth_service() -> None:
    """
    Reset the MCP authentication service instance.

    This is primarily useful for testing purposes.
    """
    global _mcp_auth_service
    _mcp_auth_service = None
