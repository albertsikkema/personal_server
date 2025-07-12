"""FastAPI-Users instance and user dependencies."""

import uuid

from fastapi_users import FastAPIUsers

from auth.backend import auth_backend
from auth.user_manager import get_user_manager
from models.user import User

# Create FastAPI-Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# User dependencies for protecting routes
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)

# Optional user dependency (returns None if not authenticated)
optional_user = fastapi_users.current_user(optional=True)
