"""
MCP RSA Key Management Service.

This module provides RSA key pair management for MCP JWT Bearer authentication
using FastMCP's built-in RSAKeyPair functionality.
"""

from fastmcp.server.auth.providers.bearer import RSAKeyPair

from config import settings
from utils.logging import get_logger

logger = get_logger(__name__)


class MCPRSAKeyManager:
    """
    MCP RSA key pair manager using FastMCP built-in RSAKeyPair.

    Leverages FastMCP's built-in key generation and management
    for seamless integration with BearerAuthProvider.
    """

    def __init__(self):
        """Initialize the RSA key manager."""
        self._key_pair: RSAKeyPair | None = None

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
                        public_key_pem=settings.MCP_JWT_PUBLIC_KEY,
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
            additional_claims={"email": email, "scope": "mcp-access"},
            expires_in_seconds=settings.MCP_JWT_EXPIRE_MINUTES * 60,
        )


# Singleton instance
_mcp_rsa_manager: MCPRSAKeyManager | None = None


def get_mcp_rsa_manager() -> MCPRSAKeyManager:
    """
    Get or create the MCP RSA key manager instance.

    Returns:
        MCPRSAKeyManager: The singleton RSA key manager instance
    """
    global _mcp_rsa_manager
    if _mcp_rsa_manager is None:
        _mcp_rsa_manager = MCPRSAKeyManager()
    return _mcp_rsa_manager


def reset_mcp_rsa_manager() -> None:
    """
    Reset the MCP RSA key manager instance.

    This is primarily useful for testing purposes.
    """
    global _mcp_rsa_manager
    _mcp_rsa_manager = None
