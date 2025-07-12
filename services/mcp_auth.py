"""
MCP Authentication Service.

This module provides MCP-specific JWT authentication service integrated with FastAPI-Users.
Generates RSA-signed JWT tokens for MCP access from authenticated FastAPI-Users.
"""

import hashlib

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
                    "auth_type": "legacy-api-key",
                },
                expires_in_seconds=self.expire_minutes * 60,
            )

            logger.info(f"Generated MCP token for legacy API key: {api_key[:8]}...")
            return token

        except Exception as e:
            logger.error(f"Failed to generate MCP token for API key: {e}")
            raise

    def _hash_api_key(self, api_key: str) -> str:
        """
        Create a hash of the API key for token identification.

        Args:
            api_key: The API key to hash

        Returns:
            str: Hashed API key (first 16 characters of SHA256 hash)
        """
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:16]


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
