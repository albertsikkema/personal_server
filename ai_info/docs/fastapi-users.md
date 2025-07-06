# fastapi users Documentation
> Source: https://context7.com/fastapi-users/fastapi-users/llms.txt
> Retrieved: 2025-06-27

TITLE: Main Entry Point for FastAPI Application with SQLAlchemy
DESCRIPTION: The main entry point for a FastAPI application using FastAPI Users with SQLAlchemy. This file initializes and runs the application.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
--8<-- "examples/sqlalchemy/main.py"
```

----------------------------------------

TITLE: FastAPI Application Setup with Beanie
DESCRIPTION: Configuration of the FastAPI application with user routes and authentication using Beanie backend. Defines the API endpoints and middleware.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_8

LANGUAGE: python
CODE:
```
--8<-- "examples/beanie/app/app.py"
```

----------------------------------------

TITLE: Implementing JWT Authentication Backend in FastAPI-Users with Python
DESCRIPTION: This code snippet demonstrates how to create a JWT-based authentication backend using FastAPI-Users. It sets up a BearerTransport, defines a JWTStrategy with a secret key and token lifetime, and combines them into an AuthenticationBackend.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/backend.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```

----------------------------------------

TITLE: FastAPI Application Setup with SQLAlchemy
DESCRIPTION: Configuration of the FastAPI application with user routes and authentication using SQLAlchemy backend. Defines the API endpoints and middleware.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
--8<-- "examples/sqlalchemy/app/app.py"
```

----------------------------------------

TITLE: Setting up Register Routes with FastAPI Users in Python
DESCRIPTION: This code snippet demonstrates how to set up register routes using FastAPI Users. It imports necessary modules, creates a FastAPIUsers instance, and includes the register router in a FastAPI application. The router is configured with specific user schemas and is added under the '/auth' prefix with the 'auth' tag.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/register.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from .db import User
from .schemas import UserCreate, UserRead

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
```

----------------------------------------

TITLE: User Management Logic for SQLAlchemy Implementation
DESCRIPTION: User management implementation with FastAPI Users using SQLAlchemy, including authentication, user creation, and user operations.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_5

LANGUAGE: python
CODE:
```
--8<-- "examples/sqlalchemy/app/users.py"
```

----------------------------------------

TITLE: User Management Logic for Beanie Implementation
DESCRIPTION: User management implementation with FastAPI Users using Beanie, including authentication, user creation, and user operations.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_11

LANGUAGE: python
CODE:
```
--8<-- "examples/beanie/app/users.py"
```

----------------------------------------

TITLE: Basic Current User Authentication in FastAPI
DESCRIPTION: Demonstrates how to get the current authenticated user without any additional checks. Returns the user object that can be used in the route.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/current-user.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"
```

----------------------------------------

TITLE: Configuring User Verification Requirement for Authentication
DESCRIPTION: This code shows how to require user verification before allowing login. It adds the requires_verification parameter to the router instantiation, ensuring that only users with is_verified=True can log in.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/auth.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Configuring FastAPIUsers Object in Python
DESCRIPTION: This snippet demonstrates how to configure the FastAPIUsers object with a user manager and authentication backend. It uses generic types for User and UUID to ensure proper type-checking and auto-completion.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/index.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi_users import FastAPIUsers

from .db import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
```

----------------------------------------

TITLE: JWT Login Authentication
DESCRIPTION: Authentication requests using JWT backend with form data submission. Returns an access token used for subsequent authenticated requests.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/flow.md#2025-04-23_snippet_1

LANGUAGE: bash
CODE:
```
curl \
-H "Content-Type: multipart/form-data" \
-X POST \
-F "username=king.arthur@camelot.bt" \
-F "password=guinevere" \
http://localhost:8000/auth/jwt/login
```

LANGUAGE: typescript
CODE:
```
const formData = new FormData();
formData.set('username', 'king.arthur@camelot.bt');
formData.set('password', 'guinevere');
axios.post(
    'http://localhost:8000/auth/jwt/login',
    formData,
    {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    },
)
.then((response) => console.log(response))
.catch((error) => console.log(error));
```

----------------------------------------

TITLE: Defining SQLAlchemy User Model with UUID Primary Key
DESCRIPTION: Creates a SQLAlchemy User model by inheriting from SQLAlchemyBaseUserTableUUID and Base classes. This model includes default user fields and allows for custom field additions.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/databases/sqlalchemy.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
```

----------------------------------------

TITLE: Implementing Database Authentication Strategy
DESCRIPTION: Defines a function to create and configure the DatabaseStrategy for authentication. This strategy uses the AccessTokenDatabase adapter and sets a token lifetime. It demonstrates how to set up the database-backed authentication strategy in FastAPI Users.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/strategies/database.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)
```

----------------------------------------

TITLE: Setting up FastAPI Users Verify Router in Python
DESCRIPTION: This snippet demonstrates how to initialize and include the verify router in a FastAPI application. It creates a FastAPIUsers instance with a user model and UUID type, then adds the verify router to the FastAPI app with a specified prefix and tags.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/verify.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from .db import User
from .schemas import UserRead

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Active User Authentication in FastAPI
DESCRIPTION: Shows how to get only active authenticated users. Will throw 401 Unauthorized if the user is inactive.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/current-user.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
current_active_user = fastapi_users.current_user(active=True)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"
```

----------------------------------------

TITLE: Implementing Database Adapter Dependencies
DESCRIPTION: Sets up FastAPI dependencies for database session management and user database adapter creation. Includes session factory and user database configuration.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/databases/sqlalchemy.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
```

----------------------------------------

TITLE: Superuser Authentication in FastAPI
DESCRIPTION: Implements authentication for active superusers. Will throw 401 Unauthorized if inactive or 403 Forbidden if not a superuser.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/current-user.md#2025-04-23_snippet_3

LANGUAGE: python
CODE:
```
current_superuser = fastapi_users.current_user(active=True, superuser=True)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_superuser)):
    return f"Hello, {user.email}"
```

----------------------------------------

TITLE: Initializing FastAPIUsers - Before and After Comparison
DESCRIPTION: Shows how the initialization of FastAPIUsers has changed to use generics and no longer requires passing Pydantic schemas directly. The new approach uses type parameters instead of explicit schema parameters.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/9x_to_10x.md#2025-04-23_snippet_8

LANGUAGE: python
CODE:
```
fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
```

LANGUAGE: python
CODE:
```
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
```

----------------------------------------

TITLE: Initializing FastAPI Users Router
DESCRIPTION: Sets up basic user management routes in a FastAPI application using FastAPIUsers. Includes configuration of user manager, authentication backend, and route prefix with tags.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/users.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from .db import User
from .schemas import UserRead, UserUpdate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
```

----------------------------------------

TITLE: Deleting a User with cURL in FastAPI-Users
DESCRIPTION: HTTP DELETE request to remove a user from the system using cURL. Requires a valid JWT token in the Authorization header and the user's UUID as part of the URL path.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/flow.md#2025-04-23_snippet_4

LANGUAGE: bash
CODE:
```
curl \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X DELETE \
http://localhost:8000/users/4fd3477b-eccf-4ee3-8f7d-68ad72261476
```

----------------------------------------

TITLE: Configuring Bearer Transport in FastAPI-Users
DESCRIPTION: This code shows how to initialize a BearerTransport instance for FastAPI-Users authentication. The tokenUrl parameter specifies the endpoint that will handle JWT login requests, enabling the interactive documentation to discover it and provide a working Authorize button.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/transports/bearer.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
```

----------------------------------------

TITLE: Configuring Basic JWT Strategy in FastAPI Users
DESCRIPTION: Basic JWT strategy implementation using a secret key and lifetime configuration. Demonstrates how to set up JWT authentication with a simple secret and token expiration time.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/strategies/jwt.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_users.authentication import JWTStrategy

SECRET = "SECRET"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
```

----------------------------------------

TITLE: Setting up Beanie Models for OAuth
DESCRIPTION: Configures OAuth account support for MongoDB using Beanie by embedding OAuth account objects within the User document using a Pydantic model.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/oauth.md#2025-04-23_snippet_4

LANGUAGE: py
CODE:
```
--8<-- "docs/src/db_beanie_oauth.py"
```

----------------------------------------

TITLE: Configuring User Verification Router
DESCRIPTION: Demonstrates how to set up user routes with mandatory verification requirement. Adds requires_verification parameter to ensure users must be verified to access these routes.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/users.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)
```

----------------------------------------

TITLE: Setting up Authentication Router in FastAPI Users
DESCRIPTION: This code demonstrates how to create and include an authentication router in a FastAPI application. It configures login and logout routes for a specific authentication backend with a prefix and tag.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/auth.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from .db import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Using the Create User Function
DESCRIPTION: Example script showing how to use the create_user function in an async context with asyncio.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/cookbook/create-user-programmatically.md#2025-04-23_snippet_3

LANGUAGE: python
CODE:
```
import asyncio

if __name__ == "__main__":
    asyncio.run(create_user("king.arthur@camelot.bt", "guinevere"))
```

----------------------------------------

TITLE: Enabling Automatic Account Association by Email
DESCRIPTION: Configures the OAuth router to automatically associate OAuth logins with existing user accounts that have the same email address, with a warning about potential security implications.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/oauth.md#2025-04-23_snippet_6

LANGUAGE: py
CODE:
```
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        "SECRET",
        associate_by_email=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Configuring Reset Password Router in FastAPI
DESCRIPTION: Sets up reset password functionality by configuring FastAPIUsers instance and including the reset password router in a FastAPI application. Creates two endpoints: /forgot-password for requesting reset tokens and /reset-password for changing passwords using those tokens.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/routers/reset.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from .db import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Configuring Redis Authentication Strategy for FastAPI Users
DESCRIPTION: Example configuration for setting up a Redis authentication strategy. It creates a Redis connection and defines a function that returns a RedisStrategy instance with a specified token lifetime.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/strategies/redis.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
import redis.asyncio
from fastapi_users.authentication import RedisStrategy

redis = redis.asyncio.from_url("redis://localhost:6379", decode_responses=True)

def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)
```

----------------------------------------

TITLE: Configuring FastAPI-Users with SQLAlchemy
DESCRIPTION: Example code demonstrating how to set up FastAPI-Users with SQLAlchemy as the database backend. It includes user model definition, database configuration, and user manager setup.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/index.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from user_manager import get_user_manager
from db import User

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret="SECRET", lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[
User, int
](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(fastapi_users.current_user())):
    return {"message": f"Hello {user.email}!"}
```

----------------------------------------

TITLE: Extending User Schemas with Custom Fields in Python
DESCRIPTION: Enhanced implementation of user schemas with additional custom fields. Adds first_name and birthdate fields to all schema variations with appropriate optionality.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/schemas.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
import datetime
import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    birthdate: Optional[datetime.date]


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    birthdate: Optional[datetime.date]


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    birthdate: Optional[datetime.date]
```

----------------------------------------

TITLE: Database Configuration for SQLAlchemy Implementation
DESCRIPTION: Database setup for the SQLAlchemy implementation of FastAPI Users, including model definitions and database connection configuration.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_3

LANGUAGE: python
CODE:
```
--8<-- "examples/sqlalchemy/app/db.py"
```

----------------------------------------

TITLE: Configuring Cookie Authentication in FastAPI-Users
DESCRIPTION: Code to set up a cookie authentication transport with customizable expiration time. The CookieTransport class supports configuration for cookie name, lifetime, path, domain, security, and same-site policy.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/transports/cookie.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_users.authentication import CookieTransport

cookie_transport = CookieTransport(cookie_max_age=3600)
```

----------------------------------------

TITLE: Configuring Custom PasswordHash with Argon2 in FastAPI Users
DESCRIPTION: Demonstrates how to create a custom PasswordHash instance that only uses the Argon2 algorithm, and initialize a PasswordHelper with it.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/password-hash.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash = PasswordHash((
    Argon2Hasher(),
))
password_helper = PasswordHelper(password_hash)
```

----------------------------------------

TITLE: Listing Python Dependencies for FastAPI Users Project
DESCRIPTION: This snippet lists the required Python packages for a FastAPI Users project with SQLAlchemy integration. It includes FastAPI, FastAPI Users with SQLAlchemy support, Uvicorn for running the ASGI server, and aiosqlite for asynchronous SQLite database operations.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/examples/sqlalchemy/requirements.txt#2025-04-23_snippet_0

LANGUAGE: plaintext
CODE:
```
fastapi
fastapi-users[sqlalchemy]
uvicorn[standard]
aiosqlite
```

----------------------------------------

TITLE: Generating OAuth Router for FastAPI
DESCRIPTION: Adds an OAuth-specific router to a FastAPI application, configuring it with an OAuth client, authentication backend, and security secret.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/oauth.md#2025-04-23_snippet_5

LANGUAGE: py
CODE:
```
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/google",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Implementing RS256 JWT Strategy in FastAPI Users
DESCRIPTION: Advanced JWT strategy implementation using RSA256 algorithm with public/private key pair. Shows how to configure JWT authentication using asymmetric encryption with RSA keys.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/strategies/jwt.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
from fastapi_users.authentication import JWTStrategy

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
# Your RSA public key in PEM format goes here
-----END PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
# Your RSA private key in PEM format goes here
-----END RSA PRIVATE KEY-----"""

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=PRIVATE_KEY, 
        lifetime_seconds=3600,
        algorithm="RS256",
        public_key=PUBLIC_KEY,
    )
```

----------------------------------------

TITLE: Defining Dependencies for FastAPI Users with SQLAlchemy and OAuth
DESCRIPTION: This requirements file specifies the necessary Python packages for a FastAPI application using fastapi-users with SQLAlchemy ORM and OAuth authentication. It includes the ASGI server uvicorn with standard extensions and aiosqlite for asynchronous SQLite database operations.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/examples/sqlalchemy-oauth/requirements.txt#2025-04-23_snippet_0

LANGUAGE: plaintext
CODE:
```
fastapi
fastapi-users[sqlalchemy,oauth]
uvicorn[standard]
aiosqlite
```

----------------------------------------

TITLE: Defining User Manager Dependency with Generator
DESCRIPTION: Example showing how FastAPI dependencies are typically defined using generators with the yield keyword in the dependency injection system.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/cookbook/create-user-programmatically.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
```

----------------------------------------

TITLE: Configuring Beanie Access Token Model and Database Adapter
DESCRIPTION: Defines an AccessToken ODM model inheriting from BeanieBaseAccessToken and sets up a dependency for instantiating the BeanieAccessTokenDatabase. This snippet shows how to integrate the access token functionality with Beanie ODM in FastAPI Users.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/strategies/database.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
class AccessToken(BeanieBaseAccessToken[PydanticObjectId]):
    pass

async def get_access_token_db():
    yield BeanieAccessTokenDatabase(AccessToken)
```

----------------------------------------

TITLE: Dynamic Authentication Backends in FastAPI
DESCRIPTION: Advanced implementation showing how to dynamically enable different authentication backends based on request path. Demonstrates configuration of JWT and Cookie authentication.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/current-user.md#2025-04-23_snippet_4

LANGUAGE: python
CODE:
```
from fastapi import Request
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, CookieTransport, JWTStrategy

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
cookie_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

async def get_enabled_backends(request: Request):
    """Return the enabled dependencies following custom logic."""
    if request.url.path == "/protected-route-only-jwt":
        return [jwt_backend]
    else:
        return [cookie_backend, jwt_backend]


current_active_user = fastapi_users.current_user(active=True, get_enabled_backends=get_enabled_backends)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}. You are authenticated with a cookie or a JWT."


@app.get("/protected-route-only-jwt")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}. You are authenticated with a JWT."
```

----------------------------------------

TITLE: Defining Basic User Schemas in Python with FastAPI Users
DESCRIPTION: Basic implementation of user schemas extending FastAPI Users base classes. Demonstrates setup of UserRead with UUID type, and basic UserCreate and UserUpdate schemas.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/schemas.md#2025-04-23_snippet_0

LANGUAGE: python
CODE:
```
import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
```

----------------------------------------

TITLE: Creating OAuth Association Router for Authenticated Users
DESCRIPTION: Sets up a router that allows already authenticated users to associate their account with an OAuth provider for future authentication.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/oauth.md#2025-04-23_snippet_7

LANGUAGE: py
CODE:
```
app.include_router(
    fastapi_users.get_oauth_associate_router(google_oauth_client, UserRead, "SECRET"),
    prefix="/auth/associate/google",
    tags=["auth"],
)
```

----------------------------------------

TITLE: Writing User Creation Function
DESCRIPTION: Implementation of a function to create users programmatically, showing proper handling of context managers and required arguments outside the dependency injection system.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/cookbook/create-user-programmatically.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
--8<-- "docs/src/cookbook_create_user_programmatically.py"
```

----------------------------------------

TITLE: Migrating UserManager Class in FastAPI Users
DESCRIPTION: Changes to the UserManager implementation for FastAPI Users v10. The class now requires a parse_id method through mixins and uses generic typing for the native User model class and ID type.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/9x_to_10x.md#2025-04-23_snippet_6

LANGUAGE: python
CODE:
```
class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
```

LANGUAGE: python
CODE:
```
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
```

----------------------------------------

TITLE: Setting OAuth Users as Verified by Default
DESCRIPTION: Configures the OAuth router to automatically mark users registering through OAuth as verified, avoiding the need for email verification when using trusted OAuth providers.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/oauth.md#2025-04-23_snippet_8

LANGUAGE: py
CODE:
```
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        "SECRET",
        is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)
```

----------------------------------------

TITLE: User Schema Definitions for SQLAlchemy Implementation
DESCRIPTION: Pydantic schema definitions for user models in the SQLAlchemy implementation, defining the structure of user data for API requests and responses.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/full-example.md#2025-04-23_snippet_4

LANGUAGE: python
CODE:
```
--8<-- "examples/sqlalchemy/app/schemas.py"
```

----------------------------------------

TITLE: Successful Login Response Format with Bearer Authentication
DESCRIPTION: This JSON snippet shows the format of a successful login response when using Bearer authentication in FastAPI-Users. It includes the access_token (JWT) and token_type fields in the response body.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/authentication/transports/bearer.md#2025-04-23_snippet_1

LANGUAGE: json
CODE:
```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
    "token_type": "bearer"
}
```

----------------------------------------

TITLE: Implementing UserManager with Custom PasswordHelper in FastAPI
DESCRIPTION: Shows how to integrate a custom password helper into the UserManager initialization.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/password-hash.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db, password_helper)
```

----------------------------------------

TITLE: Migrating MongoDB User Database Integration in FastAPI Users
DESCRIPTION: Complete rewrite of MongoDB integration for FastAPI Users v10, transitioning from direct MongoDB adapter to Beanie ODM. This includes defining a proper User model using Beanie.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/9x_to_10x.md#2025-04-23_snippet_4

LANGUAGE: python
CODE:
```
import os

import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase

from app.models import UserDB

DATABASE_URL = os.environ["DATABASE_URL"]
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["database_name"]
collection = db["users"]


async def get_user_db():
    yield MongoDBUserDatabase(UserDB, collection)
```

LANGUAGE: python
CODE:
```
import motor.motor_asyncio
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["database_name"]


class User(BeanieBaseUser[PydanticObjectId]):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
```

----------------------------------------

TITLE: Visualizing FastAPI Users Library Structure with Mermaid Flowchart
DESCRIPTION: This Mermaid flowchart illustrates the structure of the FastAPI Users library, showing the relationships between various components such as FastAPIUsers, UserManager, database adapters, authentication backends, and routers.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/overview.md#2025-04-23_snippet_0

LANGUAGE: mermaid
CODE:
```
flowchart TB
    FASTAPI_USERS{FastAPIUsers}
    USER_MANAGER{UserManager}
    USER_MODEL{User model}
    DATABASE_DEPENDENCY[[get_user_db]]
    USER_MANAGER_DEPENDENCY[[get_user_manager]]
    CURRENT_USER[[current_user]]
    subgraph SCHEMAS[Schemas]
        USER[User]
        USER_CREATE[UserCreate]
        USER_UPDATE[UserUpdate]
    end
    subgraph DATABASE[Database adapters]
        SQLALCHEMY[SQLAlchemy]
        BEANIE[Beanie]
    end
    subgraph ROUTERS[Routers]
        AUTH[[get_auth_router]]
        OAUTH[[get_oauth_router]]
        OAUTH_ASSOCIATE[[get_oauth_associate_router]]
        REGISTER[[get_register_router]]
        VERIFY[[get_verify_router]]
        RESET[[get_reset_password_router]]
        USERS[[get_users_router]]
    end
    subgraph AUTH_BACKENDS[Authentication]
        subgraph TRANSPORTS[Transports]
            COOKIE[CookieTransport]
            BEARER[BearerTransport]
        end
        subgraph STRATEGIES[Strategies]
            DB[DatabaseStrategy]
            JWT[JWTStrategy]
            REDIS[RedisStrategy]
        end
        AUTH_BACKEND{AuthenticationBackend}
    end
    DATABASE --> DATABASE_DEPENDENCY
    USER_MODEL --> DATABASE_DEPENDENCY
    DATABASE_DEPENDENCY --> USER_MANAGER

    USER_MANAGER --> USER_MANAGER_DEPENDENCY
    USER_MANAGER_DEPENDENCY --> FASTAPI_USERS

    FASTAPI_USERS --> ROUTERS

    TRANSPORTS --> AUTH_BACKEND
    STRATEGIES --> AUTH_BACKEND

    AUTH_BACKEND --> ROUTERS
    AUTH_BACKEND --> FASTAPI_USERS

    FASTAPI_USERS --> CURRENT_USER

    SCHEMAS --> ROUTERS
```

----------------------------------------

TITLE: Setting up SQLAlchemy Models for OAuth
DESCRIPTION: Defines the SQLAlchemy models needed for OAuth account storage, including the OAuthAccount model and relationship with the User model. Highlights the important components in the implementation.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/oauth.md#2025-04-23_snippet_2

LANGUAGE: py
CODE:
```
--8<-- "docs/src/db_sqlalchemy_oauth.py"
```

----------------------------------------

TITLE: Database Adapter Creation for FastAPI Users
DESCRIPTION: Sets up the database adapter that connects the database configuration with users logic through a FastAPI dependency.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/databases/beanie.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
--8<-- "docs/src/db_beanie.py"
```

----------------------------------------

TITLE: Active and Verified User Authentication in FastAPI
DESCRIPTION: Implements authentication for active and verified users. Will throw 401 Unauthorized if inactive or 403 Forbidden if not verified.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/current-user.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_verified_user)):
    return f"Hello, {user.email}"
```

----------------------------------------

TITLE: Initializing Beanie ODM for FastAPI Users
DESCRIPTION: Code to initialize Beanie ODM during application startup when using FastAPI Users v10 with MongoDB. This needs to be added to the FastAPI application startup event.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/9x_to_10x.md#2025-04-23_snippet_5

LANGUAGE: python
CODE:
```
from beanie import init_beanie


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
```

----------------------------------------

TITLE: User Model Definition with Beanie ODM
DESCRIPTION: Creates a User model class that inherits from FastAPI Users base class, providing standard user fields with the ability to add custom fields.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/databases/beanie.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
--8<-- "docs/src/db_beanie.py"
```

----------------------------------------

TITLE: Implementing Custom PasswordHelper Protocol in FastAPI Users
DESCRIPTION: Demonstrates the implementation of a custom PasswordHelper class that follows the PasswordHelperProtocol, showing required methods for password verification, hashing, and generation.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/configuration/password-hash.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
from typing import Tuple

from fastapi_users.password import PasswordHelperProtocol

class PasswordHelper(PasswordHelperProtocol):
    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, str]:
        ...

    def hash(self, password: str) -> str:
        ...

    def generate(self) -> str:
        ...
```

----------------------------------------

TITLE: Updating SQLAlchemy User Database Adapter in FastAPI Users
DESCRIPTION: Changes to the SQLAlchemy database adapter initialization in FastAPI Users v10. The adapter now only expects the User model instead of both UserDB and UserTable.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/9x_to_10x.md#2025-04-23_snippet_2

LANGUAGE: python
CODE:
```
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)
```

LANGUAGE: python
CODE:
```
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
```

----------------------------------------

TITLE: Configuring FastAPI Routers - Before and After Comparison
DESCRIPTION: Demonstrates how to configure FastAPI authentication routers before and after the design change. In the new approach, Pydantic schemas need to be passed explicitly when initializing each router that requires them, rather than during FastAPIUsers initialization.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/9x_to_10x.md#2025-04-23_snippet_9

LANGUAGE: python
CODE:
```
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
```

LANGUAGE: python
CODE:
```
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
```

----------------------------------------

TITLE: Logging Out a User with cURL in FastAPI-Users
DESCRIPTION: HTTP POST request to end a user session using cURL. Uses cookie-based authentication, requiring the session token to be passed in the Cookie header.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/flow.md#2025-04-23_snippet_6

LANGUAGE: bash
CODE:
```
curl \
-H "Content-Type: application/json" \
-H "Cookie: fastapiusersauth=$TOKEN" \
-X POST \
http://localhost:8000/auth/cookie/logout
```

----------------------------------------

TITLE: Dependency-Only Authentication in FastAPI
DESCRIPTION: Shows how to protect a route with authentication without needing the user object in the route logic using dependencies parameter.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/usage/current-user.md#2025-04-23_snippet_5

LANGUAGE: python
CODE:
```
@app.get("/protected-route", dependencies=[Depends(current_superuser)])
def protected_route():
    return "Hello, some user."
```

----------------------------------------

TITLE: Configuring JWT Authentication in FastAPI Users v9
DESCRIPTION: Updated configuration for JWT authentication in FastAPI Users version 9. It separates the transport (BearerTransport) and strategy (JWTStrategy) components, and combines them using AuthenticationBackend.
SOURCE: https://github.com/fastapi-users/fastapi-users/blob/master/docs/migration/8x_to_9x.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```