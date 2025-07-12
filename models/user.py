"""User model for FastAPI-Users integration."""

from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model with FastAPI-Users integration.

    Extends SQLAlchemyBaseUserTableUUID which provides:
    - id: UUID (primary key)
    - email: str (unique)
    - hashed_password: str
    - is_active: bool
    - is_superuser: bool
    - is_verified: bool
    """

    __tablename__ = "users"

    # Additional fields beyond FastAPI-Users base
    first_name = Column(String(50), nullable=True, doc="User's first name")
    last_name = Column(String(50), nullable=True, doc="User's last name")
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Account creation timestamp",
    )
    last_login = Column(DateTime, nullable=True, doc="Last login timestamp")

    # Role-based access (future extension)
    role = Column(
        String(20),
        default="user",
        nullable=False,
        doc="User role: user, admin, premium",
    )

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

    def __repr__(self) -> str:
        """String representation of user."""
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
