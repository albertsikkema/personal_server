# fastapi best practices Documentation
> Source: https://context7.com/zhanymkanov/fastapi-best-practices/llms.txt
> Retrieved: 2025-06-27

TITLE: FastAPI Domain-Driven Project Structure
DESCRIPTION: This snippet illustrates a scalable and evolvable project structure for FastAPI monoliths, inspired by Netflix's Dispatch. It organizes the application by domain within the `src` folder, with each domain containing its own routers, schemas, models, services, and dependencies, promoting modularity and consistency.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_0

LANGUAGE: Directory Structure
CODE:
```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py  # db models
│   │   ├── dependencies.py
│   │   ├── config.py  # local configs
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── aws
│   │   ├── client.py  # client model for external service communication
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── services.py
│   │   └── utils.py
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── database.py  # db connection related stuff
│   └── main.py
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini
```

----------------------------------------

TITLE: FastAPI RESTful Dependency Chaining for Profile Validation
DESCRIPTION: This snippet demonstrates how to chain FastAPI dependencies to enforce RESTful principles and reuse validation logic. `valid_creator_id` reuses `valid_profile_id` by depending on it, ensuring that a profile exists before checking if it's a creator. This approach promotes cleaner, more modular API design.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_9

LANGUAGE: python
CODE:
```
# src.profiles.dependencies
async def valid_profile_id(profile_id: UUID4) -> Mapping:
    profile = await service.get_by_id(profile_id)
    if not profile:
        raise ProfileNotFound()

    return profile

# src.creators.dependencies
async def valid_creator_id(profile: Mapping = Depends(valid_profile_id)) -> Mapping:
    if not profile["is_creator"]:
       raise ProfileNotCreator()

    return profile
```

----------------------------------------

TITLE: FastAPI Dependency Decoupling and Caching Example
DESCRIPTION: This example illustrates how FastAPI caches dependency results within a request's scope, allowing for multiple reuses of smaller, decoupled dependency functions like `parse_jwt_data` without recalculation. It also introduces `valid_active_creator` and `BackgroundTasks` for additional logic.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_8

LANGUAGE: python
CODE:
```
# dependencies.py
from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

async def valid_post_id(post_id: UUID4) -> Mapping:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}


async def valid_owned_post(
    post: Mapping = Depends(valid_post_id), 
    token_data: dict = Depends(parse_jwt_data),
) -> Mapping:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()

    return post


async def valid_active_creator(
    token_data: dict = Depends(parse_jwt_data),
):
    user = await users_service.get_by_id(token_data["user_id"])
    if not user["is_active"]:
        raise UserIsBanned()
    
    if not user["is_creator"]:
       raise UserNotCreator()
    
    return user
        

# router.py
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(
    worker: BackgroundTasks,
    post: Mapping = Depends(valid_owned_post),
    user: Mapping = Depends(valid_active_creator),
):
    """Get post that belong the active user."""
    worker.add_task(notifications_service.send_email, user["id"])
    return post
```

----------------------------------------

TITLE: FastAPI Dependency Validation and JWT Parsing
DESCRIPTION: This snippet demonstrates how to define and use FastAPI dependencies for validating post IDs, parsing JWT tokens for user authentication, and ensuring a user owns a specific post. These dependencies can then be injected into route handlers.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_7

LANGUAGE: python
CODE:
```
# dependencies.py
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}


async def valid_owned_post(
    post: dict[str, Any] = Depends(valid_post_id), 
    token_data: dict[str, Any] = Depends(parse_jwt_data),
) -> dict[str, Any]:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()

    return post

# router.py
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(post: dict[str, Any] = Depends(valid_owned_post)):
    return post
```

----------------------------------------

TITLE: FastAPI Route Examples: Async vs Sync I/O Handling
DESCRIPTION: This Python code demonstrates three FastAPI routes to illustrate the difference between async and sync operations, and how blocking I/O (like `time.sleep`) affects the event loop in async vs. sync contexts. It also shows the correct way to perform non-blocking I/O using `asyncio.sleep`.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_2

LANGUAGE: python
CODE:
```
import asyncio
import time

from fastapi import APIRouter


router = APIRouter()


@router.get("/terrible-ping")
async def terrible_ping():
    time.sleep(10) # I/O blocking operation for 10 seconds, the whole process will be blocked
    
    return {"pong": True}

@router.get("/good-ping")
def good_ping():
    time.sleep(10) # I/O blocking operation for 10 seconds, but in a separate thread for the whole `good_ping` route

    return {"pong": True}

@router.get("/perfect-ping")
async def perfect_ping():
    await asyncio.sleep(10) # non-blocking I/O operation

    return {"pong": True}
```

----------------------------------------

TITLE: Using FastAPI Dependencies for Request Validation
DESCRIPTION: Illustrates how FastAPI dependencies can be effectively used for complex request validation beyond simple endpoint injection, such as checking for the existence of a resource in a database. This approach centralizes validation logic, reducing code duplication across multiple API endpoints that operate on the same resource and simplifying testing.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_6

LANGUAGE: python
CODE:
```
# dependencies.py
async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


# router.py
@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post: dict[str, Any] = Depends(valid_post_id)):
    return post


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    update_data: PostUpdate,  
    post: dict[str, Any] = Depends(valid_post_id), 
):
    updated_post = await service.update(id=post["id"], data=update_data)
    return updated_post


@router.get("/posts/{post_id}/reviews", response_model=list[ReviewsResponse])
async def get_post_reviews(post: dict[str, Any] = Depends(valid_post_id)):
    post_reviews = await reviews_service.get_by_post_id(post["id"])
    return post_reviews
```

----------------------------------------

TITLE: FastAPI: Running Synchronous Libraries in a Thread Pool
DESCRIPTION: Shows how to integrate synchronous external service libraries into an asynchronous FastAPI application using `run_in_threadpool` from Starlette to prevent blocking the event loop.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_13

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from my_sync_library import SyncAPIClient 

app = FastAPI()


@app.get("/")
async def call_my_sync_library():
    my_data = await service.get_my_data()

    client = SyncAPIClient()
    await run_in_threadpool(client.make_request, data=my_data)
```

----------------------------------------

TITLE: Configure Asynchronous Test Client for FastAPI
DESCRIPTION: This pytest fixture sets up an asynchronous test client (`httpx` with `AsyncASGIClient`) for FastAPI applications, enabling robust integration testing against the live application without a running server. It includes an example test case demonstrating how to make an asynchronous POST request and assert the response status code.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_22

LANGUAGE: Python
CODE:
```
import pytest
from async_asgi_testclient import TestClient

from src.main import app  # inited FastAPI app


@pytest.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", "9000"

    async with AsyncClient(transport=ASGITransport(app=app, client=(host, port)), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_post(client: TestClient):
    resp = await client.post("/posts")

    assert resp.status_code == 201
```

----------------------------------------

TITLE: Pydantic Data Validation with Enums and Regex
DESCRIPTION: Demonstrates how to leverage Pydantic's extensive validation features, including defining enums for restricted choices, using regex patterns for string validation, and setting field constraints like minimum length, maximum length, and age limits. It showcases EmailStr and AnyUrl types for built-in validation.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_3

LANGUAGE: python
CODE:
```
from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field


class MusicBand(str, Enum):
   AEROSMITH = "AEROSMITH"
   QUEEN = "QUEEN"
   ACDC = "AC/DC"


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr
    age: int = Field(ge=18, default=None)  # must be greater or equal to 18
    favorite_band: MusicBand | None = None  # only "AEROSMITH", "QUEEN", "AC/DC" values are allowed to be inputted
    website: AnyUrl | None = None
```

----------------------------------------

TITLE: Retrieve Posts for a Creator using SQLAlchemy
DESCRIPTION: This asynchronous function queries the database to fetch a list of posts associated with a specific creator. It uses SQLAlchemy's ORM-like constructs to perform a join with the profiles table, select specific columns, filter by owner ID, and order the results. It also demonstrates building a JSON object for the creator's details within the query.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_19

LANGUAGE: Python
CODE:
```
from typing import Any

from pydantic import UUID4
from sqlalchemy import desc, func, select, text
from sqlalchemy.sql.functions import coalesce

from src.database import database, posts, profiles, post_review, products

async def get_posts(
    creator_id: UUID4, *, limit: int = 10, offset: int = 0
) -> list[dict[str, Any]]: 
    select_query = (
        select(
            (
                posts.c.id,
                posts.c.slug,
                posts.c.title,
                func.json_build_object(
                   text("'id', profiles.id"),
                   text("'first_name', profiles.first_name"),
                   text("'last_name', profiles.last_name"),
                   text("'username', profiles.username"),
                ).label("creator"),
            )
        )
        .select_from(posts.join(profiles, posts.c.owner_id == profiles.c.id))
        .where(posts.c.owner_id == creator_id)
        .limit(limit)
        .offset(offset)
        .group_by(
            posts.c.id,
            posts.c.type,
            posts.c.slug,
            posts.c.title,
            profiles.c.id,
            profiles.c.first_name,
            profiles.c.last_name,
            profiles.c.username,
            profiles.c.avatar,
        )
        .order_by(
            desc(coalesce(posts.c.updated_at, posts.c.published_at, posts.c.created_at))
        )
    )
    
    return await database.fetch_all(select_query)
```

----------------------------------------

TITLE: Define API Schemas for Creator and Post Objects
DESCRIPTION: These Pydantic BaseModel definitions specify the data structures for `Creator` and `Post` objects. They are used for request body validation, response serialization, and generating OpenAPI documentation for the FastAPI application, ensuring consistent data contracts.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_20

LANGUAGE: APIDOC
CODE:
```
Creator (Model):
  id: UUID4
  first_name: str
  last_name: str
  username: str

Post (Model):
  id: UUID4
  slug: str
  title: str
  creator: Creator
```

----------------------------------------

TITLE: Enhance FastAPI Route Documentation with Response Models and Status Codes
DESCRIPTION: This example shows how to provide detailed documentation for a FastAPI route using "response_model", "status_code", "description", "tags", "summary", and especially the "responses" attribute. The "responses" attribute allows defining custom Pydantic models and descriptions for different HTTP status codes, leading to a more comprehensive and user-friendly API documentation.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_16

LANGUAGE: python
CODE:
```
from fastapi import APIRouter, status

router = APIRouter()

@router.post(
    "/endpoints",
    response_model=DefaultResponseModel,  # default response pydantic model 
    status_code=status.HTTP_201_CREATED,  # default status code
    description="Description of the well documented endpoint",
    tags=["Endpoint Category"],
    summary="Summary of the Endpoint",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse, # custom pydantic model for 200 response
            "description": "Ok Response"
        },
        status.HTTP_201_CREATED: {
            "model": CreatedResponse,  # custom pydantic model for 201 response
            "description": "Creates something from user request "
        },
        status.HTTP_202_ACCEPTED: {
            "model": AcceptedResponse,  # custom pydantic model for 202 response
            "description": "Accepts request and handles it later"
        }
    }
)
async def documented_route():
    pass
```

----------------------------------------

TITLE: Creating a Custom Pydantic BaseModel for Global Customizations
DESCRIPTION: Illustrates how to define a custom Pydantic BaseModel to enforce application-wide behaviors, such as standardizing datetime serialization to GMT strings with explicit timezones. It also shows how to add a common method, serializable_dict, to all models inheriting from this custom base, ensuring only serializable fields are returned.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_4

LANGUAGE: python
CODE:
```
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)

```

----------------------------------------

TITLE: Decoupling Pydantic BaseSettings for Modular Configuration
DESCRIPTION: Demonstrates how to split application configuration into multiple, domain-specific BaseSettings classes using pydantic-settings. This approach improves maintainability and organization by separating settings like authentication parameters (AuthConfig) from general application settings (Config), making it easier to manage environment variables for different modules.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_5

LANGUAGE: python
CODE:
```
# src.auth.config
from datetime import timedelta

from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes

    REFRESH_TOKEN_KEY: str
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)

    SECURE_COOKIES: bool = True


auth_settings = AuthConfig()


# src.config
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1.0"


settings = Config()
```

----------------------------------------

TITLE: FastAPI Endpoint to Get Posts by Creator ID
DESCRIPTION: This FastAPI router defines a GET endpoint that retrieves all posts for a given `creator_id`. It uses FastAPI's dependency injection system (`Depends(valid_creator_id)`) to validate the creator ID before fetching posts via the `service.get_posts` function and returning them as a list of `Post` objects.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_21

LANGUAGE: APIDOC
CODE:
```
GET /creators/{creator_id}/posts:
  Description: Retrieves a list of posts for a specific creator.
  Parameters:
    creator_id:
      Type: UUID4
      Description: The unique identifier of the creator.
      Location: Path
  Responses:
    200 OK:
      Description: A list of Post objects.
      Schema: list[Post]
```

----------------------------------------

TITLE: Pydantic: Transforming ValueError into Detailed Validation Error
DESCRIPTION: Demonstrates how raising a `ValueError` within a Pydantic `field_validator` can automatically be converted into a detailed `ValidationError` response by FastAPI, providing clear feedback to clients.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_14

LANGUAGE: python
CODE:
```
# src.profiles.schemas
from pydantic import BaseModel, field_validator

class ProfileCreate(BaseModel):
    username: str
    
    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


# src.profiles.routes
from fastapi import APIRouter

router = APIRouter()


@router.post("/profiles")
async def get_creator_posts(profile_data: ProfileCreate):
   pass
```

----------------------------------------

TITLE: Cross-Module Imports in FastAPI Project
DESCRIPTION: Demonstrates how to import components (constants, services, error codes) from different domain packages within the structured FastAPI project. It emphasizes using explicit module names for clarity and avoiding circular dependencies.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_1

LANGUAGE: Python
CODE:
```
from src.auth import constants as auth_constants
from src.notifications import service as notification_service
from src.posts.constants import ErrorCode as PostsErrorCode  # in case we have Standard ErrorCode in constants module of each package
```

----------------------------------------

TITLE: Hide FastAPI Docs by Default for Specific Environments
DESCRIPTION: This snippet demonstrates how to conditionally hide FastAPI's OpenAPI documentation (Swagger UI/ReDoc) based on the current environment. It reads the environment from a .env file and sets "openapi_url" to "None" if the environment is not in a predefined list of allowed environments (e.g., 'local', 'staging'). This ensures that documentation is only exposed in development or testing environments, improving security for production deployments.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_15

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from starlette.config import Config

config = Config(".env")  # parse .env file for env variables

ENVIRONMENT = config("ENVIRONMENT")  # get current env name
SHOW_DOCS_ENVIRONMENT = ("local", "staging")  # explicit list of allowed envs

app_configs = {"title": "My Cool API"}
if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
   app_configs["openapi_url"] = None  # set url for docs as null

app = FastAPI(**app_configs)
```

----------------------------------------

TITLE: Automate Python Code Linting and Formatting with Ruff
DESCRIPTION: This shell script demonstrates how to use Ruff, a fast Python linter and formatter, to automatically check and fix code style issues and enforce linting rules across the `src` directory. It's designed for use in development workflows, potentially as a pre-commit hook, to maintain consistent code quality.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_23

LANGUAGE: Shell
CODE:
```
#!/bin/sh -e
set -x

ruff check --fix src
ruff format src
```

----------------------------------------

TITLE: FastAPI: Get Creator Profile by ID
DESCRIPTION: Illustrates a FastAPI GET endpoint for fetching a creator's profile by ID, leveraging `Depends` for ID validation and `response_model` for response serialization.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_11

LANGUAGE: python
CODE:
```
@router.get("/creators/{profile_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(
     creator_profile: Mapping = Depends(valid_creator_id)
):
    """Get creator's profile by id."""
    return creator_profile
```

----------------------------------------

TITLE: FastAPI: Get User Profile by ID
DESCRIPTION: Demonstrates a FastAPI GET endpoint to retrieve a user profile by its ID, using `Depends` for validation and `response_model` for serialization.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_10

LANGUAGE: python
CODE:
```
@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(profile: Mapping = Depends(valid_profile_id)):
    """Get profile by id."""
    return profile
```

----------------------------------------

TITLE: Configure Alembic Migration File Template
DESCRIPTION: This configuration snippet for `alembic.ini` sets a custom file template for newly generated Alembic migration scripts. The `%%(year)d-%%(month).2d-%%(day).2d_%%(slug)s` pattern ensures that migration files are named with the date and a descriptive slug, improving organization and readability of the migration history.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_18

LANGUAGE: ini
CODE:
```
# alembic.ini
file_template = %%(year)d-%%(month).2d-%%(day).2d_%%(slug)s
```

----------------------------------------

TITLE: FastAPI: Understanding Pydantic Response Model Serialization
DESCRIPTION: Explains how FastAPI handles Pydantic `response_model` serialization, highlighting that Pydantic objects are created twice. Provides an example using `model_validator` to demonstrate this behavior.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_12

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from pydantic import BaseModel, model_validator

app = FastAPI()


class ProfileResponse(BaseModel):
    @model_validator(mode="after")
    def debug_usage(self):
        print("created pydantic model")

        return self


@app.get("/", response_model=ProfileResponse)
async def root():
    return ProfileResponse()
```

----------------------------------------

TITLE: Set PostgreSQL Index Naming Conventions in SQLAlchemy
DESCRIPTION: This snippet defines a dictionary of naming conventions for PostgreSQL indexes, unique constraints, check constraints, foreign keys, and primary keys. It then applies these conventions to SQLAlchemy's "MetaData" object, ensuring that database schema elements follow a consistent and human-readable naming pattern, which is preferable to SQLAlchemy's default conventions.
SOURCE: https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md#_snippet_17

LANGUAGE: python
CODE:
```
from sqlalchemy import MetaData

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey"
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
```