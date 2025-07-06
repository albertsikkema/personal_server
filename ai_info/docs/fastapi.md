# fastapi Documentation
> Source: https://context7.com/fastapi/fastapi/llms.txt
> Retrieved: 2025-06-27

TITLE: Installing FastAPI with Standard Dependencies
DESCRIPTION: This command installs FastAPI along with a set of commonly used standard optional dependencies, such as Uvicorn for the server and Pydantic for data validation. It is recommended to execute this command within an activated Python virtual environment to manage project dependencies effectively.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/index.md#_snippet_1

LANGUAGE: console
CODE:
```
$ pip install "fastapi[standard]"

---> 100%
```

----------------------------------------

TITLE: Defining GET Path Operation Decorator - FastAPI Python
DESCRIPTION: This snippet illustrates the `@app.get()` decorator used in FastAPI to define a path operation for handling HTTP GET requests. It maps the root path '/' to a Python function, indicating that the decorated function will be executed when a GET request is made to this URL.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_8

LANGUAGE: Python
CODE:
```
@app.get("/\")
```

----------------------------------------

TITLE: Creating a Basic FastAPI Application in Python
DESCRIPTION: This snippet initializes a FastAPI application and defines a root endpoint (`/`) that returns a JSON response. It demonstrates the minimal code required to create a functional web API with FastAPI, serving a simple 'Hello World' message.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_0

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

----------------------------------------

TITLE: Installing Uvicorn for Serving FastAPI Applications
DESCRIPTION: This command installs Uvicorn, an ASGI server, with its standard dependencies. Uvicorn is a lightweight and fast server that is commonly used to run FastAPI applications in production environments.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_1

LANGUAGE: console
CODE:
```
pip install "uvicorn[standard]"
```

----------------------------------------

TITLE: Returning JSON Content from FastAPI Path Operation
DESCRIPTION: This snippet shows how to return a Python dictionary from a FastAPI path operation function. FastAPI automatically converts dictionaries, lists, and other supported types into JSON responses, simplifying API development.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_11

LANGUAGE: Python
CODE:
```
return {"message": "Hello World"}
```

----------------------------------------

TITLE: Running FastAPI Development Server
DESCRIPTION: This command starts the FastAPI development server using `fastapi dev`. It automatically reloads the application on code changes and provides URLs for the application and its interactive documentation. The server runs on `http://127.0.0.1:8000` by default.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_1

LANGUAGE: console
CODE:
```
$ fastapi dev main.py
```

----------------------------------------

TITLE: Upgrading pip for Python Projects
DESCRIPTION: Upgrades the `pip` package installer to its latest version within the active Python virtual environment. This is a crucial first step to prevent common installation errors and should typically be performed once after creating a virtual environment.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_8

LANGUAGE: console
CODE:
```
$ python -m pip install --upgrade pip

---> 100%
```

----------------------------------------

TITLE: Adding Basic Type Hints to Function Parameters (Python)
DESCRIPTION: This snippet demonstrates adding basic type hints (`str`) to the `first_name` and `last_name` parameters of a function. This allows editors and tools to provide better autocompletion and error checking, improving developer experience without changing runtime behavior.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_1

LANGUAGE: Python
CODE:
```
def get_full_name(first_name: str, last_name: str):
    return f"{first_name.title()} {last_name.title()}"
```

----------------------------------------

TITLE: Running a Python Program within a Virtual Environment
DESCRIPTION: Executes a Python script named `main.py` using the Python interpreter from the active virtual environment. This ensures that the program runs with the specific packages installed in that environment, demonstrating basic program execution.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_16

LANGUAGE: console
CODE:
```
$ python main.py

Hello World
```

----------------------------------------

TITLE: Declaring Integer Type Hint in FastAPI
DESCRIPTION: This snippet shows how to declare a type hint for an integer parameter, `item_id`, in FastAPI. FastAPI uses this standard Python type hint for automatic data validation and documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_7

LANGUAGE: Python
CODE:
```
item_id: int
```

----------------------------------------

TITLE: Reading Environment Variables in Python with `os.getenv`
DESCRIPTION: This Python snippet demonstrates how to retrieve the value of an environment variable named `MY_NAME` using `os.getenv()`. It includes a default value ('World') to be used if the environment variable is not set, ensuring the program can run without it.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_2

LANGUAGE: python
CODE:
```
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

----------------------------------------

TITLE: Creating a Basic FastAPI Application
DESCRIPTION: This Python code defines a simple FastAPI application with two HTTP GET endpoints. The root endpoint ('/') returns a basic 'Hello: World' JSON response, while the '/items/{item_id}' endpoint demonstrates how to define path parameters (item_id) and optional query parameters (q), returning them in the response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_2

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

----------------------------------------

TITLE: Installing FastAPI with Standard Dependencies
DESCRIPTION: This command installs the FastAPI framework along with its standard recommended dependencies, such as Uvicorn for serving applications and Pydantic for data validation. The `[standard]` extra ensures a complete setup for typical FastAPI development, making it ready for immediate use.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_2

LANGUAGE: Shell
CODE:
```
$ pip install "fastapi[standard]"
```

----------------------------------------

TITLE: Creating FastAPI Application Instance
DESCRIPTION: This snippet shows the instantiation of the `FastAPI` class, creating an `app` object. This `app` instance serves as the main point of interaction for defining all API routes, operations, and configurations within the FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_5

LANGUAGE: Python
CODE:
```
app = FastAPI()
```

----------------------------------------

TITLE: Importing FastAPI Class
DESCRIPTION: This snippet demonstrates how to import the `FastAPI` class from the `fastapi` library. This class is the core component for building a FastAPI application, providing all the necessary functionality to define API routes and handle requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_4

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI
```

----------------------------------------

TITLE: Installing FastAPI with Standard Dependencies
DESCRIPTION: This command installs the FastAPI framework along with its recommended standard dependencies. These dependencies include essential libraries like Uvicorn for serving the application and Pydantic for data validation and serialization, which are crucial for developing FastAPI applications.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_0

LANGUAGE: console
CODE:
```
pip install "fastapi[standard]"
```

----------------------------------------

TITLE: Instantiating FastAPI Application
DESCRIPTION: This line creates an instance of the `FastAPI` class, typically named `app`. This `app` object is the main entry point for defining all your API's routes and operations, and it's the object referenced by ASGI servers like Uvicorn to run your application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_4

LANGUAGE: Python
CODE:
```
app = FastAPI()
```

----------------------------------------

TITLE: Defining a Pydantic Data Model in Python
DESCRIPTION: This code defines a Pydantic `Item` model inheriting from `BaseModel`. It specifies data types for `name`, `price`, and optional `description` and `tax` fields, which FastAPI uses for automatic data validation and serialization of request bodies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_1

LANGUAGE: Python
CODE:
```
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

----------------------------------------

TITLE: Defining a Class-Based Dependency with __init__
DESCRIPTION: This snippet defines `CommonQueryParams`, a Python class designed to serve as a FastAPI dependency. Its `__init__` method declares parameters (`q`, `skip`, `limit`) that FastAPI will automatically resolve from incoming request query parameters. This class-based approach provides superior type hinting and editor support compared to returning a raw dictionary.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_2

LANGUAGE: Python
CODE:
```
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
```

----------------------------------------

TITLE: Defining POST Path Operation Decorator - FastAPI Python
DESCRIPTION: This snippet shows the `@app.post()` decorator, used in FastAPI to define a path operation that handles HTTP POST requests. It's typically used for creating new resources or submitting data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_9

LANGUAGE: Python
CODE:
```
@app.post()
```

----------------------------------------

TITLE: FastAPI: Path Operation with `async def` and `await`
DESCRIPTION: Demonstrates declaring a FastAPI path operation function using `async def` when the function needs to `await` an asynchronous library call. This pattern is suitable for I/O-bound operations, allowing the application to perform other tasks while waiting for external resources.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_0

LANGUAGE: Python
CODE:
```
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

----------------------------------------

TITLE: Running FastAPI with Gunicorn and Uvicorn Workers
DESCRIPTION: This command starts the Gunicorn server, which acts as a master process, and spawns multiple Uvicorn worker processes to handle incoming requests. It specifies the application entry point (`main:app`), the number of workers (`--workers 4`), the worker class (`--worker-class uvicorn.workers.UvicornWorker`), and the binding address and port (`--bind 0.0.0.0:80`).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/server-workers.md#_snippet_1

LANGUAGE: Shell
CODE:
```
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

----------------------------------------

TITLE: Defining Separate Input and Output User Models
DESCRIPTION: This snippet defines two Pydantic models: `UserIn` for input, which includes a `password` field, and `UserOut` for output, which explicitly excludes the `password` field. This separation is a best practice for security, ensuring that sensitive data like passwords are not inadvertently exposed in API responses.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_3

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

----------------------------------------

TITLE: Declaring List of Strings (Python 3.9+)
DESCRIPTION: This snippet demonstrates the modern Python 3.9+ syntax for type-hinting a variable as a list containing string elements. It uses the built-in `list` type directly with square brackets for generic type parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body-nested-models.md#_snippet_0

LANGUAGE: Python
CODE:
```
my_list: list[str]
```

----------------------------------------

TITLE: Defining a GET Endpoint in FastAPI
DESCRIPTION: This FastAPI snippet illustrates how to define a server-side GET endpoint. The `@app.get("/some/url")` decorator maps the `read_url` function to handle GET requests for the `/some/url` path, returning a JSON object as the response. This showcases FastAPI's declarative routing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/alternatives.md#_snippet_1

LANGUAGE: Python
CODE:
```
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

----------------------------------------

TITLE: FastAPI Parameter Type Declaration: Pydantic Model
DESCRIPTION: Illustrates how to declare a complex Pydantic model type hint for a function parameter in FastAPI, enabling automatic validation of complex JSON bodies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_2

LANGUAGE: Python
CODE:
```
item: Item
```

----------------------------------------

TITLE: Declaring Annotated Dependency Parameter in FastAPI
DESCRIPTION: This snippet illustrates the declaration of a dependency parameter using Python's `Annotated` type hint combined with FastAPI's `Depends` function. It demonstrates how to specify a dependency, `common_parameters`, and its expected type, `dict`, directly within a function signature for type checking and dependency injection.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/index.md#_snippet_3

LANGUAGE: Python
CODE:
```
commons: Annotated[dict, Depends(common_parameters)]
```

----------------------------------------

TITLE: Protecting Against Host Header Attacks with TrustedHostMiddleware - Python
DESCRIPTION: Shows how to integrate `TrustedHostMiddleware` to validate the `Host` header of incoming requests, preventing HTTP Host Header attacks. It requires a list of `allowed_hosts`, which can include wildcard domains, and returns a `400` response for invalid hosts.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/middleware.md#_snippet_3

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

----------------------------------------

TITLE: Running FastAPI Application with Uvicorn
DESCRIPTION: This console command initiates the FastAPI application using fastapi dev, which internally uses Uvicorn. It starts a development server, making the application accessible at http://127.0.0.1:8000. This command is essential for testing and running FastAPI applications locally.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md#_snippet_3

LANGUAGE: Console
CODE:
```
fastapi dev main.py
```

----------------------------------------

TITLE: Extracting Set Values with Pydantic's exclude_unset (Python)
DESCRIPTION: This line of code demonstrates how to use Pydantic's `model_dump(exclude_unset=True)` (or `.dict()` in Pydantic v1) to create a dictionary containing only the fields that were explicitly set in the incoming request model. This is crucial for partial updates, as it prevents default values from overwriting existing data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-updates.md#_snippet_2

LANGUAGE: Python
CODE:
```
update_data = item.model_dump(exclude_unset=True)
```

----------------------------------------

TITLE: Defining a GET Path Operation
DESCRIPTION: This snippet demonstrates how to define a GET path operation using the `@app.get()` decorator in FastAPI. The decorator associates the following asynchronous Python function with the specified URL path (`/`) and the HTTP GET method, making it responsible for handling incoming GET requests to that route.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_7

LANGUAGE: Python
CODE:
```
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

----------------------------------------

TITLE: Creating a Basic FastAPI Application with Async Endpoints
DESCRIPTION: This Python code illustrates a FastAPI application where endpoint functions are defined using `async def`. This approach is beneficial for I/O-bound operations, allowing the server to handle multiple requests concurrently without blocking, thereby improving performance and responsiveness. It includes a root endpoint and an item endpoint, both asynchronous.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_3

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

----------------------------------------

TITLE: Combining Body, Path, and Query Parameters in FastAPI
DESCRIPTION: This snippet demonstrates a FastAPI path operation that simultaneously handles a request body (`item`), a path parameter (`item_id`), and an optional query parameter (`q`). FastAPI automatically parses and validates each parameter from its respective source (body, URL path, or query string).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_7

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    results = {"item_id": item_id, **item.dict()}
    if q:
        results.update({"q": q})
    return results
```

----------------------------------------

TITLE: Declaring Response Model in FastAPI Post Endpoint
DESCRIPTION: This snippet demonstrates how to declare a `response_model` for a FastAPI POST endpoint. The `response_model` parameter in the `@app.post()` decorator ensures that the output data is transformed, validated, and documented according to the `Item` Pydantic model, even if the function returns the input item directly.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

----------------------------------------

TITLE: Create Virtual Environment using venv
DESCRIPTION: This snippet demonstrates how to create a virtual environment using Python's built-in `venv` module. The command creates a new isolated environment in a `.venv` directory within your project, ensuring project-specific package isolation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/ja/docs/virtual-environments.md#_snippet_1

LANGUAGE: console
CODE:
```
$ python -m venv .venv
```

----------------------------------------

TITLE: Adding Max Length Validation with Annotated and Query
DESCRIPTION: This snippet demonstrates how to apply a maximum length validation to an optional query parameter `q` using `Annotated` and `Query`. By including `Query(max_length=50)` within `Annotated`, FastAPI enforces that the provided string for `q` does not exceed 50 characters, while still keeping the parameter optional.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_6

LANGUAGE: Python
CODE:
```
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    if q:
        return {"q": q}
    return {"message": "No q parameter"}
```

----------------------------------------

TITLE: Overriding FastAPI Dependencies for Testing - Python
DESCRIPTION: This snippet illustrates how to override a FastAPI dependency (`get_settings`) for testing purposes using `app.dependency_overrides`. A mock `get_settings_override` function is defined to return a `Settings` object with a specific `admin_email`, allowing tests to run with controlled configurations without affecting the actual application settings.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_13

LANGUAGE: Python
CODE:
```
from fastapi.testclient import TestClient
from main import app, get_settings
from config import Settings

def get_settings_override():
    return Settings(admin_email="testing@example.com")

client = TestClient(app)

app.dependency_overrides[get_settings] = get_settings_override

def test_info_override():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "testing@example.com"
    }
```

----------------------------------------

TITLE: FastAPI OAuth2 Password Flow Initial Setup
DESCRIPTION: This complete example demonstrates the foundational setup for implementing OAuth2 password flow in FastAPI. It defines the OAuth2PasswordBearer scheme with a tokenUrl and protects a path operation, automatically generating OpenAPI documentation for authentication. Requires python-multipart for form data parsing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/first-steps.md#_snippet_0

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

----------------------------------------

TITLE: Importing APIRouter Class in Python
DESCRIPTION: This snippet demonstrates how to import the `APIRouter` class directly from the `fastapi` library. The `APIRouter` class is essential for organizing routes and handlers in larger FastAPI applications, allowing for modular API design.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/apirouter.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi import APIRouter
```

----------------------------------------

TITLE: Protecting Endpoint with OAuth2 Dependency
DESCRIPTION: This snippet shows how to secure a path operation by injecting oauth2_scheme as a dependency. FastAPI automatically validates the Authorization header, extracts the bearer token, and passes it to the token parameter, or returns a 401 Unauthorized error if invalid.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/first-steps.md#_snippet_3

LANGUAGE: Python
CODE:
```
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
```

----------------------------------------

TITLE: Defining DELETE Path Operation Decorator - FastAPI Python
DESCRIPTION: This snippet illustrates the `@app.delete()` decorator, used in FastAPI to define a path operation for handling HTTP DELETE requests. It's typically used for removing resources.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_11

LANGUAGE: Python
CODE:
```
@app.delete()
```

----------------------------------------

TITLE: Database Dependency Setup with Yield (Python)
DESCRIPTION: This snippet demonstrates the initial part of a database dependency using `yield`. The code before and including `yield` is executed before the path operation, setting up the database session. The yielded value (`db`) is then injected into the dependent function.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_0

LANGUAGE: Python
CODE:
```
def get_db():
    db = DBSession()
    try:
        yield db
```

----------------------------------------

TITLE: Importing BaseModel for Request Body Definition - Python
DESCRIPTION: This snippet demonstrates how to import `BaseModel` from the Pydantic library, which is the foundational class for defining data models used in FastAPI request bodies. It's a prerequisite for creating structured data schemas.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_0

LANGUAGE: Python
CODE:
```
from pydantic import BaseModel
```

----------------------------------------

TITLE: Declaring Typed Path Parameters in FastAPI
DESCRIPTION: This example shows how to add a type annotation (`int`) to a path parameter in FastAPI. This enables automatic data conversion from the URL string to a Python integer, providing type safety and better editor support.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_2

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

----------------------------------------

TITLE: Declaring Dependencies in FastAPI Path Operations (Python)
DESCRIPTION: These snippets illustrate how to integrate a dependency into FastAPI path operation functions using `Annotated` and `Depends`. The `common_parameters` function is automatically called, and its return value is injected into the `commons` parameter, streamlining the use of shared logic across different endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/index.md#_snippet_2

LANGUAGE: Python
CODE:
```
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

----------------------------------------

TITLE: Reading a Single Hero by ID in FastAPI
DESCRIPTION: This FastAPI endpoint retrieves a single `Hero` object from the database using its `hero_id`. It queries the session for the hero and raises an `HTTPException` with a 404 status if the hero is not found, ensuring proper error handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_8

LANGUAGE: Python
CODE:
```
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(*, session: SessionDep, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

----------------------------------------

TITLE: Install FastAPI with Standard Dependencies
DESCRIPTION: This command installs FastAPI along with its standard dependencies, including a Uvicorn server and Pydantic. It is recommended to use a virtual environment for installation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_0

LANGUAGE: console
CODE:
```
$ pip install "fastapi[standard]"
```

----------------------------------------

TITLE: Loading Settings from .env with Pydantic - Python
DESCRIPTION: This Python snippet demonstrates how to configure Pydantic's `Settings` class to automatically load environment variables from a `.env` file. By setting `model_config = SettingsConfigDict(env_file=".env")` within the `Settings` class, Pydantic will look for and parse the specified `.env` file during instantiation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_15

LANGUAGE: Python
CODE:
```
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str

    model_config = SettingsConfigDict(env_file=".env")
```

----------------------------------------

TITLE: Declaring Complex Model Body Parameters in FastAPI (Python)
DESCRIPTION: This snippet shows how to declare a complex `Item` model as a parameter in FastAPI. Using a Pydantic model (implied by `Item`), FastAPI automatically handles JSON body parsing, validation, and serialization, providing comprehensive editor support.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_9

LANGUAGE: Python
CODE:
```
item: Item
```

----------------------------------------

TITLE: Defining a Pydantic Data Model for Request Body - Python
DESCRIPTION: This code defines a Pydantic model named `Item` by inheriting from `BaseModel`. It specifies the expected data structure for a request body, including required fields (`name`, `price`) and optional fields (`description`, `tax`) with default `None` values, enabling automatic data validation and serialization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_1

LANGUAGE: Python
CODE:
```
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

----------------------------------------

TITLE: Defining Data Models with Pydantic
DESCRIPTION: Introduces Pydantic, a library for data validation and settings management using Python type hints. It shows how to define a data model by inheriting from `BaseModel` and declaring typed attributes. Pydantic automatically validates data against these types, providing robust data handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_16

LANGUAGE: Python
CODE:
```
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

LANGUAGE: Python
CODE:
```
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

LANGUAGE: Python
CODE:
```
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

----------------------------------------

TITLE: Overriding Settings for Testing
DESCRIPTION: This snippet illustrates how to easily override the `get_settings` dependency during testing. By assigning a custom function to `app.dependency_overrides[get_settings]`, you can provide specific settings (e.g., a test `admin_email`) for isolated and predictable test scenarios. Remember to clear overrides after tests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/settings.md#_snippet_3

LANGUAGE: Python
CODE:
```
from fastapi.testclient import TestClient
from main import app, get_settings, Settings

def test_info_with_override():
    def override_get_settings():
        return Settings(admin_email="test@example.com")

    app.dependency_overrides[get_settings] = override_get_settings
    client = TestClient(app)
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "test@example.com",
    }
    app.dependency_overrides.clear() # Clean up
```

----------------------------------------

TITLE: Creating a Hero Entry in FastAPI with SQLModel
DESCRIPTION: This FastAPI endpoint handles the creation of a new `Hero` entry. It accepts a `Hero` object from the request body, adds it to the database session, commits the transaction, refreshes the object to include database-generated fields (like `id`), and returns the created hero.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_6

LANGUAGE: Python
CODE:
```
@app.post("/heroes/", response_model=Hero)
def create_hero(*, session: SessionDep, hero: Hero):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

----------------------------------------

TITLE: Defining Python Types and Pydantic Models in FastAPI
DESCRIPTION: This snippet demonstrates the use of standard Python type declarations for function parameters and the definition of a Pydantic BaseModel for data validation and serialization. It highlights how FastAPI leverages these types for automatic data handling and enhanced editor support.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/features.md#_snippet_0

LANGUAGE: Python
CODE:
```
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

----------------------------------------

TITLE: Declaring an Async FastAPI Path Operation Function
DESCRIPTION: This FastAPI path operation function is declared with `async def` because it performs an I/O-bound operation by awaiting `some_library()`. Using `async def` allows FastAPI to run other tasks concurrently while this function is waiting for the library call to complete, improving overall application responsiveness.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_1

LANGUAGE: Python
CODE:
```
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

----------------------------------------

TITLE: Running FastAPI Application with Uvicorn (Console)
DESCRIPTION: This command starts the FastAPI application using Uvicorn. It specifies `main:app` where `main` refers to the `main.py` file and `app` is the FastAPI instance within it. The `--reload` flag enables automatic server restart on code changes, which is useful during development.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_4

LANGUAGE: Console
CODE:
```
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

----------------------------------------

TITLE: Running FastAPI Application with Uvicorn
DESCRIPTION: This command starts the FastAPI application using Uvicorn, a fast ASGI server. `main:app` specifies the `app` instance from `main.py`. The `--reload` flag enables automatic server restart on code changes, which is highly useful for development.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_0

LANGUAGE: console
CODE:
```
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

----------------------------------------

TITLE: Declaring Request Body Parameter in FastAPI Path Operation - Python
DESCRIPTION: This snippet shows how to declare a request body parameter in a FastAPI path operation function. By type-hinting the parameter `item` with the `Item` Pydantic model, FastAPI automatically handles JSON parsing, validation, and provides the structured data to the function.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_4

LANGUAGE: Python
CODE:
```
@app.post("/items/")
async def create_item(item: Item):
```

----------------------------------------

TITLE: Defining Multiple Pydantic Models for User Data in Python
DESCRIPTION: This snippet defines distinct Pydantic models (`UserIn`, `UserInDB`, `UserOut`) for handling user data at different stages: input (with plaintext password), database storage (with hashed password), and output (without password). It also includes a `create_user` function demonstrating the data flow and transformation between these models, using `**user_in.dict()` for unpacking.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Optional
from pydantic import BaseModel

# Simulate a password hasher and user saver
def fake_password_hasher(password: str):
    return "hashed" + password

def fake_save_user(user_in_db: "UserInDB"):
    # Simulate saving to a database
    print(f"Saving user: {user_in_db.username} to DB")
    return user_in_db

# Input model: User provides password
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None

# Database model: Stores hashed password
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: Optional[str] = None

# Output model: Does not expose password
class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# Example usage
def create_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    saved_user = fake_save_user(user_in_db)
    user_out = UserOut(**saved_user.dict())
    return user_out

# Test the function
user_input = UserIn(username="john", password="secret", email="john.doe@example.com")
created_user = create_user(user_input)
print(f"Created user (output): {created_user.username}, {created_user.email}")
```

----------------------------------------

TITLE: Configure CORS Middleware in FastAPI
DESCRIPTION: Demonstrates how to import and apply `CORSMiddleware` to a FastAPI application. It shows how to define a list of allowed origins and configure various CORS settings such as credentials, allowed methods, and headers, enabling cross-origin requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/cors.md#_snippet_0

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost",
    "https://example.org",
    "https://www.example.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

----------------------------------------

TITLE: Updating FastAPI Application with Pydantic Model and PUT Endpoint (Python)
DESCRIPTION: This Python code updates the `main.py` file to introduce a Pydantic `Item` model for data validation and a new `PUT` endpoint. The `Item` model defines the structure for incoming request bodies, ensuring type safety and enabling automatic documentation. The `update_item` function handles `PUT` requests to `/items/{item_id}`, accepting an `item_id` and an `Item` object as the request body.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_6

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```