"""User schemas for FastAPI-Users integration."""

import uuid
from datetime import datetime

from fastapi_users import schemas

from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User read schema - returned when fetching user data.

    Includes all user fields that should be visible to the client.
    Excludes sensitive fields like hashed_password.
    """

    first_name: str | None = Field(None, description="User's first name")
    last_name: str | None = Field(None, description="User's last name")
    role: str = Field("user", description="User role: user, admin, premium")
    created_at: datetime = Field(..., description="Account creation timestamp")
    last_login: datetime | None = Field(None, description="Last login timestamp")

    @property
    def full_name(self) -> str | None:
        """Get user's full name if available."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return None


class UserCreate(schemas.BaseUserCreate):
    """User creation schema - used for registration.

    Includes all fields required/optional for creating a new user.
    """

    first_name: str | None = Field(
        None, max_length=50, description="User's first name (optional)"
    )
    last_name: str | None = Field(
        None, max_length=50, description="User's last name (optional)"
    )
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=8, description="User's password (minimum 8 characters)"
    )


class UserUpdate(schemas.BaseUserUpdate):
    """User update schema - used for updating user information.

    All fields are optional since this is for partial updates.
    """

    first_name: str | None = Field(None, max_length=50, description="User's first name")
    last_name: str | None = Field(None, max_length=50, description="User's last name")
    password: str | None = Field(
        None, min_length=8, description="New password (minimum 8 characters)"
    )
