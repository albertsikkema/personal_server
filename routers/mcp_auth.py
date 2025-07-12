"""
MCP Authentication Router.

This module provides API endpoints for MCP token generation with dual authentication support.
Supports both FastAPI-Users authentication and legacy API key authentication.
"""

from datetime import UTC, datetime
from typing import Any

from auth.users import current_active_user
from dependencies import RequiredAuth
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from pydantic import BaseModel, Field
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
    user_info: dict[str, Any] = Field(..., description="User information")


@router.post("/mcp-token", response_model=MCPTokenResponse)
async def generate_mcp_token(
    _request: MCPTokenRequest,
    current_user: User = Depends(current_active_user),
    mcp_auth_service=Depends(get_mcp_auth_service),
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
            detail=f"Failed to generate MCP token: {e!s}",
        ) from e


@router.post("/mcp-token/legacy", response_model=MCPTokenResponse)
async def generate_mcp_token_legacy(
    _request: MCPTokenRequest,
    api_key: str = RequiredAuth,
    mcp_auth_service=Depends(get_mcp_auth_service),
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
            detail=f"Failed to generate MCP token: {e!s}",
        ) from e
