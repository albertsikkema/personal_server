"""User manager for FastAPI-Users integration."""

import logging
import uuid

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_async_session
from fastapi import Depends, Request
from models.user import User

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """Custom user manager with lifecycle hooks."""

    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

    async def on_after_register(self, user: User, request: Request | None = None):  # noqa: ARG002 - FastAPI-Users interface requirement - FastAPI-Users interface requirement
        """Handle post-registration logic.

        Args:
            user: The newly registered user.
            request: The request object (if available).
        """
        logger.info(f"User {user.id} has registered with email {user.email}")

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,  # noqa: ARG002 - FastAPI-Users interface requirement - FastAPI-Users interface requirement
        response=None,  # noqa: ARG002 - FastAPI-Users interface requirement
    ):
        """Handle post-login logic.

        Args:
            user: The user who logged in.
            request: The request object (if available).
            response: The response object (if available).
        """
        logger.info(f"User {user.id} logged in")

        # Update last_login timestamp
        # Note: This requires a database update, but we don't have
        # access to the session here. In production, you might want
        # to handle this differently or use a background task.

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Request | None = None,  # noqa: ARG002 - FastAPI-Users interface requirement
    ):
        """Handle post-forgot-password logic.

        Args:
            user: The user who requested password reset.
            token: The reset token.
            request: The request object (if available).
        """
        logger.info(
            f"User {user.id} has forgotten their password. Reset token: {token}"
        )

    async def on_after_reset_password(self, user: User, request: Request | None = None):  # noqa: ARG002 - FastAPI-Users interface requirement
        """Handle post-password-reset logic.

        Args:
            user: The user who reset their password.
            request: The request object (if available).
        """
        logger.info(f"User {user.id} has reset their password")

    async def on_after_update(
        self,
        user: User,
        update_dict: dict,
        request: Request | None = None,  # noqa: ARG002 - FastAPI-Users interface requirement
    ):
        """Handle post-update logic.

        Args:
            user: The updated user.
            update_dict: Dictionary of updated fields.
            request: The request object (if available).
        """
        logger.info(f"User {user.id} has been updated: {list(update_dict.keys())}")

    async def on_after_verification_request(
        self,
        user: User,
        token: str,
        request: Request | None = None,  # noqa: ARG002 - FastAPI-Users interface requirement
    ):
        """Handle post-verification-request logic.

        Args:
            user: The user who requested verification.
            token: The verification token.
            request: The request object (if available).
        """
        logger.info(f"Verification requested for user {user.id}. Token: {token}")

    async def on_after_verify(self, user: User, request: Request | None = None):  # noqa: ARG002 - FastAPI-Users interface requirement
        """Handle post-verification logic.

        Args:
            user: The user who was verified.
            request: The request object (if available).
        """
        logger.info(f"User {user.id} has been verified")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get user database dependency.

    Args:
        session: Database session.

    Yields:
        SQLAlchemyUserDatabase: User database instance.
    """
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """Get user manager dependency.

    Args:
        user_db: User database instance.

    Yields:
        UserManager: User manager instance.
    """
    yield UserManager(user_db)
