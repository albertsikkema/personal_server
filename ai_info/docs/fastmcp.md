TITLE: Creating a Dice Roller FastMCP Server in Python
DESCRIPTION: This Python snippet demonstrates how to create a FastMCP server that exposes a `roll_dice` tool. The `FastMCP` instance is named "Dice Roller", and the `roll_dice` function, decorated with `@mcp.tool()`, simulates rolling 6-sided dice. The server is configured to run using SSE transport on port 8000.
SOURCE: https://gofastmcp.com/integrations/openai

LANGUAGE: python
CODE:
```
import random
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool()
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

----------------------------------------

TITLE: Accessing MCP Context in a FastMCP Tool (Python)
DESCRIPTION: This example illustrates how a FastMCP tool can access MCP features like logging, resource reading, and progress reporting through the `Context` object. By adding a parameter with the `Context` type hint to the tool function, developers can use `ctx.info()`, `ctx.read_resource()`, `ctx.report_progress()`, and `ctx.sample()` to interact with the MCP environment and client LLM. The `process_data` function demonstrates reading data from a URI, reporting processing progress, and summarizing content using the client's LLM.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="ContextDemo")

@mcp.tool()
async def process_data(data_uri: str, ctx: Context) -> dict:
    """Process data from a resource with progress reporting."""
    await ctx.info(f"Processing data from {data_uri}")
    
    # Read a resource
    resource = await ctx.read_resource(data_uri)
    data = resource[0].content if resource else ""
    
    # Report progress
    await ctx.report_progress(progress=50, total=100)
    
    # Example request to the client's LLM for help
    summary = await ctx.sample(f"Summarize this in 10 words: {data[:200]}")
    
    await ctx.report_progress(progress=100, total=100)
    return {
        "length": len(data),
        "summary": summary.text
    }
```

----------------------------------------

TITLE: Adding FastMCP as a Dependency with uv
DESCRIPTION: This command adds FastMCP as a project dependency using the `uv` package manager. It's recommended for integrating FastMCP into an existing project, ensuring proper dependency management and isolation.
SOURCE: https://gofastmcp.com/getting-started/installation

LANGUAGE: bash
CODE:
```
uv add fastmcp
```

----------------------------------------

TITLE: Defining a Tool with FastMCP in Python
DESCRIPTION: This example illustrates how to define a callable tool using the @mcp.tool() decorator. Tools are functions that clients can invoke to perform specific actions or access external systems.
SOURCE: https://gofastmcp.com/servers/fastmcp

LANGUAGE: python
CODE:
```
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b
```

----------------------------------------

TITLE: Defining Tool with Pydantic Field Metadata in Python
DESCRIPTION: This snippet illustrates how to provide rich parameter metadata using Pydantic's `Field` with `Annotated`. The `process_image` tool takes an `image_url` with a description, `resize` boolean, `width` with range constraints (1-2000), and `format` with allowed literal values. This metadata enhances LLM understanding and enables advanced validation.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: python
CODE:
```
from typing import Annotated
from pydantic import Field

@mcp.tool()
def process_image(
    image_url: Annotated[str, Field(description="URL of the image to process")],
    resize: Annotated[bool, Field(description="Whether to resize the image")] = False,
    width: Annotated[int, Field(description="Target width in pixels", ge=1, le=2000)] = 800,
    format: Annotated[
        Literal["jpeg", "png", "webp"],
        Field(description="Output image format")
    ] = "jpeg"
) -> dict:
    """Process an image with optional resizing."""
    # Implementation...
```

----------------------------------------

TITLE: Installing FastMCP Directly with uv pip or pip
DESCRIPTION: These commands demonstrate direct installation of the FastMCP library using either `uv pip` or `pip`. This method is suitable for global or virtual environment installations when not managing FastMCP as a project dependency.
SOURCE: https://gofastmcp.com/getting-started/installation

LANGUAGE: bash uv
CODE:
```
uv pip install fastmcp
```

LANGUAGE: bash pip
CODE:
```
pip install fastmcp
```

----------------------------------------

TITLE: Defining and Running a Basic FastMCP Tool in Python
DESCRIPTION: This snippet demonstrates how to initialize a FastMCP server, define a simple tool using the `@mcp.tool()` decorator, and run the server. The `add` tool takes two integers and returns their sum, showcasing how to expose functionality to LLMs via the Model Context Protocol. It illustrates the minimal boilerplate required to create an MCP server.
SOURCE: https://gofastmcp.com/getting-started/welcome

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

----------------------------------------

TITLE: Generating Python Code Examples with LLM Sampling
DESCRIPTION: This tool demonstrates how to generate a Python code example for a given concept using `ctx.sample`. It utilizes both a user message and a system prompt to guide the LLM, along with `temperature` and `max_tokens` parameters for fine-grained control over the generation process. The output is formatted as a Python code block.
SOURCE: https://gofastmcp.com/servers/context

LANGUAGE: python
CODE:
```
@mcp.tool()
async def generate_example(concept: str, ctx: Context) -> str:
    """Generate a Python code example for a given concept."""
    # Using a system prompt and a user message
    response = await ctx.sample(
        messages=f"Write a simple Python code example demonstrating '{concept}'.",
        system_prompt="You are an expert Python programmer. Provide concise, working code examples without explanations.",
        temperature=0.7,
        max_tokens=300
    )
    
    code_example = response.text
    return f"```python\n{code_example}\n```"
```

----------------------------------------

TITLE: Defining a Resource with FastMCP in Python
DESCRIPTION: This snippet shows how to expose data sources as resources using the @mcp.resource() decorator. Resources allow clients to read specific data, such as application configuration.
SOURCE: https://gofastmcp.com/servers/fastmcp

LANGUAGE: python
CODE:
```
@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}
```

----------------------------------------

TITLE: Mounting Subserver and Calling Tools in FastMCP (Python)
DESCRIPTION: This snippet demonstrates how to create a live link between a main FastMCP server and a subserver using `main_mcp.mount()`. It shows how tools defined on the subserver, even those added after mounting, become accessible through the main server with a prefixed name. It also includes an asynchronous test to verify tool access and execution.
SOURCE: https://gofastmcp.com/servers/composition

LANGUAGE: python
CODE:
```
import asyncio
from fastmcp import FastMCP, Client

# Define subserver
dynamic_mcp = FastMCP(name="DynamicService")

@dynamic_mcp.tool()
def initial_tool():
    """Initial tool demonstration."""
    return "Initial Tool Exists"

# Mount subserver (synchronous operation)
main_mcp = FastMCP(name="MainAppLive")
main_mcp.mount("dynamic", dynamic_mcp)

# Add a tool AFTER mounting - it will be accessible through main_mcp
@dynamic_mcp.tool()
def added_later():
    """Tool added after mounting."""
    return "Tool Added Dynamically!"

# Testing access to mounted tools
async def test_dynamic_mount():
    tools = await main_mcp.get_tools()
    print("Available tools:", list(tools.keys()))
    # Shows: ['dynamic_initial_tool', 'dynamic_added_later']
    
    async with Client(main_mcp) as client:
        result = await client.call_tool("dynamic_added_later")
        print("Result:", result[0].text)
        # Shows: "Tool Added Dynamically!"

if __name__ == "__main__":
    asyncio.run(test_dynamic_mount())
```

----------------------------------------

TITLE: Configuring BearerAuthProvider with a JWKS URI (Python)
DESCRIPTION: This snippet shows how to configure the `BearerAuthProvider` using a JSON Web Key Set (JWKS) URI. This approach is recommended for production environments as it supports automatic key rotation and multiple signing keys, fetching the public keys dynamically from the specified endpoint.
SOURCE: https://gofastmcp.com/servers/auth/bearer

LANGUAGE: python
CODE:
```
provider = BearerAuthProvider(
    jwks_uri="https://idp.example.com/.well-known/jwks.json"
)
```

----------------------------------------

TITLE: Defining Structured Data with Pydantic Models in FastMCP (Python)
DESCRIPTION: This example demonstrates using Pydantic models for complex, structured data inputs in FastMCP tools. It highlights automatic validation, JSON schema generation, and conversion from JSON objects or dictionaries, providing clear and self-documenting input structures.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str
    email: str = Field(description="User's email address")
    age: int | None = None
    is_active: bool = True

@mcp.tool()
def create_user(user: User):
    """Create a new user in the system."""
    # The input is automatically validated against the User model
    # Even if provided as a JSON string or dict
    # Implementation...
```

----------------------------------------

TITLE: Registering a Tool with FastMCP Server in Python
DESCRIPTION: This code shows how to add a callable tool to the FastMCP server. The `greet` function is decorated with `@mcp.tool()` to register it, allowing the server to expose this functionality to clients. It takes a `name` string and returns a greeting.
SOURCE: https://gofastmcp.com/getting-started/quickstart

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

----------------------------------------

TITLE: Composing FastMCP Servers using Mount - Python
DESCRIPTION: This snippet demonstrates how to compose multiple FastMCP servers by mounting a sub-server onto a main server. It shows the creation of two `FastMCP` instances, `main` and `sub`, and registers a simple tool on the `sub` server. The `sub` server is then mounted onto the `main` server using `main.mount("sub", sub)`, allowing the main server to expose the sub-server's functionalities.
SOURCE: https://gofastmcp.com/servers/fastmcp

LANGUAGE: python
CODE:
```
# Example: Importing a subserver
from fastmcp import FastMCP
import asyncio

main = FastMCP(name="Main")
sub = FastMCP(name="Sub")

@sub.tool()
def hello(): 
    return "hi"

# Mount directly
main.mount("sub", sub)
```

----------------------------------------

TITLE: Calling FastMCP Server via OpenAI Responses API in Python
DESCRIPTION: This Python code demonstrates how to interact with a deployed FastMCP server using the OpenAI Python SDK's `responses.create` method. It configures a tool of type "mcp" pointing to the FastMCP server's URL and sends an input prompt to trigger the tool. The response's `output_text` is then printed, showing the result of the tool's execution.
SOURCE: https://gofastmcp.com/integrations/openai

LANGUAGE: python
CODE:
```
from openai import OpenAI

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "dice_server",
            "server_url": f"{url}/sse",
            "require_approval": "never",
        },
    ],
    input="Roll a few dice!",
)

print(resp.output_text)
```

----------------------------------------

TITLE: Initializing a FastMCP Server in Python
DESCRIPTION: This snippet demonstrates how to create a basic FastMCP server instance by importing the `FastMCP` class and instantiating it with a server name. This is the foundational step for building any FastMCP application.
SOURCE: https://gofastmcp.com/getting-started/quickstart

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
```

----------------------------------------

TITLE: Using Streamable HTTP Transport (Inferred) in FastMCP Client - Python
DESCRIPTION: This snippet demonstrates the automatic inference of `StreamableHttpTransport` when a FastMCP `Client` is initialized with an HTTP or HTTPS URL. It shows how to connect to a server and list available tools within an asynchronous context. This is the recommended and default approach for web-based deployments since v2.3.0.
SOURCE: https://gofastmcp.com/clients/transports

LANGUAGE: python
CODE:
```
from fastmcp import Client
import asyncio

# The Client automatically uses StreamableHttpTransport for HTTP URLs
client = Client("https://example.com/mcp")

async def main():
    async with client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

asyncio.run(main())
```

----------------------------------------

TITLE: Defining Tool Parameters with Pydantic Annotated Fields in Python
DESCRIPTION: This snippet demonstrates how to define tool parameters using Pydantic's `Field` in conjunction with `typing.Annotated` for robust validation. It shows examples of applying range constraints to numbers (`ge`, `le`, `gt`, `lt`), pattern and length constraints to strings (`pattern`, `min_length`, `max_length`), and `multiple_of` constraints for integers. This ensures that input values conform to specific business rules before tool execution, improving data integrity and preventing invalid inputs.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: Python
CODE:
```
from typing import Annotated
from pydantic import Field

@mcp.tool()
def analyze_metrics(
    # Numbers with range constraints
    count: Annotated[int, Field(ge=0, le=100)],         # 0 <= count <= 100
    ratio: Annotated[float, Field(gt=0, lt=1.0)],       # 0 < ratio < 1.0
    
    # String with pattern and length constraints
    user_id: Annotated[str, Field(
        pattern=r"^[A-Z]{2}\d{4}$",                     # Must match regex pattern
        description="User ID in format XX0000"
    )],
    
    # String with length constraints
    comment: Annotated[str, Field(min_length=3, max_length=500)] = "",
    
    # Numeric constraints
    factor: Annotated[int, Field(multiple_of=5)] = 10  # Must be multiple of 5
):
    """Analyze metrics with validated parameters."""
    # Implementation...
```

----------------------------------------

TITLE: Using Type Annotations and Pydantic Fields in FastMCP Prompts - Python
DESCRIPTION: This Python snippet demonstrates the importance of type annotations in FastMCP prompts for parameter validation and schema generation. It uses `pydantic.Field` to add descriptions to parameters and `typing.Literal` and `typing.Optional` for stricter type control, allowing for more robust and well-defined prompt interfaces.
SOURCE: https://gofastmcp.com/servers/prompts

LANGUAGE: Python
CODE:
```
from pydantic import Field
from typing import Literal, Optional

@mcp.prompt()
def generate_content_request(
    topic: str = Field(description="The main subject to cover"),
    format: Literal["blog", "email", "social"] = "blog",
    tone: str = "professional",
    word_count: Optional[int] = None
) -> str:
    """Create a request for generating content in a specific format."""
    prompt = f"Please write a {format} post about {topic} in a {tone} tone."
    
    if word_count:
        prompt += f" It should be approximately {word_count} words long."
        
    return prompt
```

----------------------------------------

TITLE: Configuring Bearer Token Authentication in FastMCP (Python)
DESCRIPTION: This snippet demonstrates how to initialize the `BearerAuthProvider` with a JWKS URI, issuer, and audience for JWT validation, and then integrate it into a `FastMCP` server instance. It enables the server to validate incoming JWTs for securing HTTP-based transports.
SOURCE: https://gofastmcp.com/servers/auth/bearer

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider

auth = BearerAuthProvider(
    jwks_uri="https://my-identity-provider.com/.well-known/jwks.json",
    issuer="https://my-identity-provider.com/",
    audience="my-mcp-server"
)

mcp = FastMCP(name="My MCP Server", auth=auth)
```

----------------------------------------

TITLE: Constraining Parameters with Literal Types in FastMCP Python
DESCRIPTION: This example shows how to use `typing.Literal` to constrain tool parameters to a predefined set of exact values. The `sort_data` function demonstrates `order` and `algorithm` parameters accepting only specific string literals, which helps LLMs and clients understand acceptable inputs and provides input validation.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: Python
CODE:
```
from typing import Literal

@mcp.tool()
def sort_data(
    data: list[float],
    order: Literal["ascending", "descending"] = "ascending",
    algorithm: Literal["quicksort", "mergesort", "heapsort"] = "quicksort"
):
    """Sort data using specific options."""
    # Implementation...
```

----------------------------------------

TITLE: Defining Basic Tool with @mcp.tool in Python
DESCRIPTION: This snippet demonstrates how to define a simple FastMCP tool by decorating a Python function with `@mcp.tool()`. The `add` function takes two integers, `a` and `b`, and returns their sum. FastMCP automatically uses the function name as the tool name, the docstring as the description, and generates an input schema based on type annotations.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b
```

----------------------------------------

TITLE: Running FastMCP Server in Python
DESCRIPTION: This snippet shows how to start the FastMCP server using the mcp.run() method, typically within a __main__ block for direct execution. It demonstrates running with the default STDIO transport and provides a commented example for HTTP transport configuration.
SOURCE: https://gofastmcp.com/servers/fastmcp

LANGUAGE: python
CODE:
```
# my_server.py
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run()
    
    # To use a different transport, e.g., HTTP:
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
```

----------------------------------------

TITLE: Running FastMCP Server using CLI Command
DESCRIPTION: This command demonstrates how to start a FastMCP server using the `fastmcp` command-line interface. The `run` subcommand is used, specifying the server file (`my_server.py`) and the server object within it (`mcp`), which starts the server with the default `stdio` transport.
SOURCE: https://gofastmcp.com/getting-started/quickstart

LANGUAGE: Bash
CODE:
```
fastmcp run my_server.py:mcp
```

----------------------------------------

TITLE: Mounting FastMCP Server in Starlette Application (Python)
DESCRIPTION: This snippet demonstrates how to mount a FastMCP server as a sub-application within an existing Starlette application. It shows creating a FastMCP ASGI app, defining a `Mount` route, and passing the FastMCP app's lifespan to the main Starlette application for proper initialization.
SOURCE: https://gofastmcp.com/deployment/asgi

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

# Create your FastMCP server as well as any tools, resources, etc.
mcp = FastMCP("MyServer")

# Create the ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Create a Starlette app and mount the MCP server
app = Starlette(
    routes=[
        Mount("/mcp-server", app=mcp_app),
        # Add other routes as needed
    ],
    lifespan=mcp_app.lifespan,
)
```

----------------------------------------

TITLE: Defining Tool with Type Annotations in Python
DESCRIPTION: This example shows how to define a FastMCP tool using standard Python type annotations for parameters. The `analyze_text` function accepts a `text` string, an optional `max_tokens` integer (defaulting to 100), and an optional `language` string or `None`. Type annotations are crucial for LLM understanding, client validation, and schema generation.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: python
CODE:
```
@mcp.tool()
def analyze_text(
    text: str,
    max_tokens: int = 100,
    language: str | None = None
) -> dict:
    """Analyze the provided text."""
    # Implementation...
```

----------------------------------------

TITLE: Handling fastmcp ClientError and ConnectionError in Python
DESCRIPTION: This example illustrates a robust error handling pattern for `fastmcp` client interactions. It demonstrates catching `ClientError` for server-side tool execution failures, `ConnectionError` for network-related issues, and a general `Exception` for any other unforeseen errors during `call_tool` operations.
SOURCE: https://gofastmcp.com/clients/client

LANGUAGE: Python
CODE:
```
async def safe_call_tool():
    async with client:
        try:
            # Assume 'divide' tool exists and might raise ZeroDivisionError
            result = await client.call_tool("divide", {"a": 10, "b": 0})
            print(f"Result: {result}")
        except ClientError as e:
            print(f"Tool call failed: {e}")
        except ConnectionError as e:
            print(f"Connection failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
```

----------------------------------------

TITLE: Handling Errors with ResourceError and ValueError in FastMCP (Python)
DESCRIPTION: Demonstrates different error handling strategies in FastMCP. `ResourceError` allows explicit control over error messages sent to clients, regardless of the `mask_error_details` setting. Standard `ValueError` exceptions, however, will have their details masked if `mask_error_details` is `True`, providing a generic error message instead.
SOURCE: https://gofastmcp.com/servers/resources

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://safe-error")
def fail_with_details() -> str:
    """This resource provides detailed error information."""
    # ResourceError contents are always sent back to clients,
    # regardless of mask_error_details setting
    raise ResourceError("Unable to retrieve data: file not found")

@mcp.resource("resource://masked-error")
def fail_with_masked_details() -> str:
    """This resource masks internal error details when mask_error_details=True."""
    # This message would be masked if mask_error_details=True
    raise ValueError("Sensitive internal file path: /etc/secrets.conf")

@mcp.resource("data://{id}")
def get_data_by_id(id: str) -> dict:
    """Template resources also support the same error handling pattern."""
    if id == "secure":
        raise ValueError("Cannot access secure data")
    elif id == "missing":
        raise ResourceError("Data ID 'missing' not found in database")
    return {"id": id, "value": "data"}
```

----------------------------------------

TITLE: Calling a FastMCP Server with Gemini SDK - Python
DESCRIPTION: This Python asynchronous code demonstrates how to connect to a local FastMCP server and integrate its tools with the Google Gemini SDK. It initializes a FastMCP client, enters its context, and then passes the client session to the Gemini SDK's `generate_content` method, allowing Gemini to invoke the defined MCP tools (e.g., `roll_dice`) based on the prompt.
SOURCE: https://gofastmcp.com/integrations/gemini

LANGUAGE: Python
CODE:
```
from fastmcp import Client
from google import genai
import asyncio

mcp_client = Client("server.py")
gemini_client = genai.Client()

async def main():    
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Roll 3 dice!",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Importing Subservers in FastMCP (Python)
DESCRIPTION: This snippet demonstrates how to use `FastMCP.import_server()` for static composition. It defines a `WeatherService` subserver with tools and resources, then imports it into a `MainApp` server, showing how components are prefixed to avoid naming conflicts. Changes made to the subserver after importing are not reflected in the main server.
SOURCE: https://gofastmcp.com/servers/composition

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP
import asyncio

# Define subservers
weather_mcp = FastMCP(name="WeatherService")

@weather_mcp.tool()
def get_forecast(city: str) -> dict:
    """Get weather forecast."""
    return {"city": city, "forecast": "Sunny"}

@weather_mcp.resource("data://cities/supported")
def list_supported_cities() -> list[str]:
    """List cities with weather support."""
    return ["London", "Paris", "Tokyo"]

# Define main server
main_mcp = FastMCP(name="MainApp")

# Import subserver
async def setup():
    await main_mcp.import_server("weather", weather_mcp)

# Result: main_mcp now contains prefixed components:
# - Tool: "weather_get_forecast"
# - Resource: "data://weather/cities/supported" 

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run()
```

----------------------------------------

TITLE: HTTP Authorization Header Example
DESCRIPTION: This snippet illustrates the standard format for including a Bearer token in the 'Authorization' header of an HTTP request. The '<token>' placeholder should be replaced with the actual JSON Web Token (JWT).
SOURCE: https://gofastmcp.com/clients/auth/bearer

LANGUAGE: HTTP
CODE:
```
Authorization: Bearer <token>
```

----------------------------------------

TITLE: Defining Optional Arguments in FastMCP Python Tools
DESCRIPTION: This snippet demonstrates how FastMCP interprets Python function parameters. Parameters without default values are considered required, while those with default values (including None for optional types) are treated as optional, allowing the LLM to omit them.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: Python
CODE:
```
@mcp.tool()
def search_products(
    query: str,                   # Required - no default value
    max_results: int = 10,        # Optional - has default value
    sort_by: str = "relevance",   # Optional - has default value
    category: str | None = None   # Optional - can be None
) -> list[dict]:
    """Search the product catalog."""
    # Implementation...

```

----------------------------------------

TITLE: Connecting to Remote Authenticated FastMCP Server - Python
DESCRIPTION: This Python snippet illustrates how to configure a FastMCP client to connect to a remote server using an HTTPS endpoint and authenticate with a Bearer token. This flexibility allows the Gemini SDK to interact with FastMCP servers deployed remotely or those requiring specific authentication methods, without altering the core Gemini API interaction logic.
SOURCE: https://gofastmcp.com/integrations/gemini

LANGUAGE: Python
CODE:
```
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

client = Client(
    "https://my-server.com/sse",
    auth=BearerAuth("<your-token>"),
)
```

----------------------------------------

TITLE: Running a Local FastMCP Server
DESCRIPTION: This command executes a local FastMCP server directly from a specified Python file. It runs the server in your current Python environment, making you responsible for ensuring all necessary dependencies are installed and available.
SOURCE: https://gofastmcp.com/patterns/cli

LANGUAGE: bash
CODE:
```
fastmcp run server.py
```

----------------------------------------

TITLE: Complete FastMCP Server with Bearer Authentication and Tool (Python)
DESCRIPTION: This comprehensive example combines RSA key generation, `BearerAuthProvider` setup, and a `FastMCP` application with a `roll_dice` tool. It demonstrates a fully authenticated server that prints the generated access token (for development only) and runs on SSE transport.
SOURCE: https://gofastmcp.com/integrations/openai

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.bearer import RSAKeyPair
import random

key_pair = RSAKeyPair.generate()
access_token = key_pair.create_token(audience="dice-server")

auth = BearerAuthProvider(
    public_key=key_pair.public_key,
    audience="dice-server",
)

mcp = FastMCP(name="Dice Roller", auth=auth)

@mcp.tool()
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    print(f"\n---\n\n🔑 Dice Roller access token:\n\n{access_token}\n\n---\n")
    mcp.run(transport="sse", port=8000)
```

----------------------------------------

TITLE: Defining Built-in Parameter Types for FastMCP Tools (Python)
DESCRIPTION: This snippet showcases the use of Python's built-in scalar types (`str`, `int`, `float`, `bool`) as parameters for a FastMCP tool. FastMCP leverages Pydantic for type validation and coercion, ensuring that inputs are correctly handled even if they arrive as different types (e.g., a string '42' for an `int` parameter). These type hints provide clear expectations for LLMs and enable proper input validation.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: python
CODE:
```
@mcp.tool()
def process_values(
    name: str,             # Text data
    count: int,            # Integer numbers
    amount: float,         # Floating point numbers
    enabled: bool          # Boolean values (True/False)
):
    """Process various value types."""
    # Implementation...
```

----------------------------------------

TITLE: Configuring FastMCP with Streamable HTTP (Default)
DESCRIPTION: This snippet demonstrates how to initialize and run a FastMCP server using the recommended Streamable HTTP transport with its default host (127.0.0.1), port (8000), and path (/mcp). It also includes a corresponding client example showing how to connect to this default endpoint and perform a basic ping operation.
SOURCE: https://gofastmcp.com/deployment/running-server

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

LANGUAGE: python
CODE:
```
import asyncio
from fastmcp import Client

async def example():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        await client.ping()

if __name__ == "__main__":
    asyncio.run(example())
```

----------------------------------------

TITLE: Calling FastMCP Server via Anthropic Messages API (Python)
DESCRIPTION: This Python code demonstrates how to call a FastMCP server using the Anthropic Messages API. It initializes an Anthropic client, constructs a message with a user prompt, and specifies the FastMCP server URL and name. It's crucial to include the `extra_headers` for beta features and replace the placeholder URL with the actual server endpoint.
SOURCE: https://gofastmcp.com/integrations/anthropic

LANGUAGE: python
CODE:
```
import anthropic
from rich import print

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Roll a few dice!"}],
    mcp_servers=[
        {
            "type": "url",
            "url": f"{url}/sse",
            "name": "dice-server"
        }
    ],
    extra_headers={
        "anthropic-beta": "mcp-client-2025-04-04"
    }
)

print(response.content)
```

----------------------------------------

TITLE: Creating a Dice Roller FastMCP Server in Python
DESCRIPTION: This Python snippet defines a simple FastMCP server named 'Dice Roller'. It includes a `roll_dice` tool that simulates rolling a specified number of 6-sided dice, demonstrating basic FastMCP server setup and tool definition for local execution.
SOURCE: https://gofastmcp.com/integrations/claude-desktop

LANGUAGE: Python
CODE:
```
import random
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool()
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    mcp.run()
```

----------------------------------------

TITLE: Creating a FastMCP Dice Roller Server in Python
DESCRIPTION: This Python snippet defines a FastMCP server named 'Dice Roller' with a single tool, `roll_dice`. The tool takes an integer `n_dice` and returns a list of random 6-sided dice rolls. The server runs on port 8000 using SSE transport.
SOURCE: https://gofastmcp.com/integrations/anthropic

LANGUAGE: python
CODE:
```
import random
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool()
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

----------------------------------------

TITLE: Defining FastMCP Tool with Context Injection - Python
DESCRIPTION: Demonstrates how to define a FastMCP tool (`@mcp.tool()`) that accepts the `Context` object via dependency injection. The `ctx: Context` parameter allows the tool to access MCP capabilities like logging and resource management during file processing.
SOURCE: https://gofastmcp.com/servers/context

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="ContextDemo")

@mcp.tool()
async def process_file(file_uri: str, ctx: Context) -> str:
    """Processes a file, using context for logging and resource access."""
    # Context is available as the ctx parameter
    return "Processed file"
```

----------------------------------------

TITLE: Running FastMCP Server via Python Main Block
DESCRIPTION: This code demonstrates how to make the FastMCP server executable directly from a Python script. By adding `mcp.run()` within the `if __name__ == "__main__":` block, the server can be started using `python my_server.py`, typically using the default `stdio` transport.
SOURCE: https://gofastmcp.com/getting-started/quickstart

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

----------------------------------------

TITLE: Accessing FastMCP Context in Prompts (Python)
DESCRIPTION: This example shows how to access the `Context` object within a FastMCP prompt function. By adding a parameter typed as `Context`, prompts can retrieve additional information like the `request_id`, enabling more dynamic and context-aware prompt generation.
SOURCE: https://gofastmcp.com/servers/prompts

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="PromptServer")

@mcp.prompt()
async def generate_report_request(report_type: str, ctx: Context) -> str:
    """Generates a request for a report."""
    return f"Please create a {report_type} report. Request ID: {ctx.request_id}"
```

----------------------------------------

TITLE: Defining Required and Optional Parameters in FastMCP Prompts (Python)
DESCRIPTION: This snippet demonstrates how to define required and optional parameters in a FastMCP prompt function. Parameters without a default value, like `data_uri`, are required, while those with default values, such as `analysis_type` and `include_charts`, are optional. The `@mcp.prompt()` decorator registers the function as a prompt.
SOURCE: https://gofastmcp.com/servers/prompts

LANGUAGE: python
CODE:
```
@mcp.prompt()
def data_analysis_prompt(
    data_uri: str,                        # Required - no default value
    analysis_type: str = "summary",       # Optional - has default value
    include_charts: bool = False          # Optional - has default value
) -> str:
    """Creates a request to analyze data with specific parameters."""
    prompt = f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
    if include_charts:
        prompt += " Include relevant charts and visualizations."
    return prompt
```

----------------------------------------

TITLE: Running Asynchronous FastMCP Client Operations in Python
DESCRIPTION: This line executes the asynchronous `main` function, which contains the FastMCP client operations. It uses `asyncio.run()` to start the event loop and run the top-level coroutine until it completes.
SOURCE: https://gofastmcp.com/clients/transports

LANGUAGE: Python
CODE:
```
asyncio.run(main())
```

----------------------------------------

TITLE: Configuring Timeouts for fastmcp Client Calls in Python
DESCRIPTION: This snippet demonstrates how to set a default global timeout for all requests made by a `fastmcp` client and how to override this timeout for individual `call_tool` invocations. It also shows how to catch `McpError` specifically for timeout scenarios.
SOURCE: https://gofastmcp.com/clients/client

LANGUAGE: Python
CODE:
```
client = Client(
    my_mcp_server,
    timeout=5.0  # Default timeout in seconds
)

async with client:
    # This uses the global 5-second timeout
    result1 = await client.call_tool("quick_task", {"param": "value"})
    
    # This specifies a 10-second timeout for this specific call
    result2 = await client.call_tool("slow_task", {"param": "value"}, timeout=10.0)
    
    try:
        # This will likely timeout
        result3 = await client.call_tool("medium_task", {"param": "value"}, timeout=0.01)
    except McpError as e:
        # Handle timeout error
        print(f"The task timed out: {e}")
```

----------------------------------------

TITLE: Defining Standard Resource Templates in FastMCP (Python)
DESCRIPTION: This snippet demonstrates how to define resource templates using the `@mcp.resource` decorator in FastMCP. It shows two examples: one for fetching weather information by city and another for retrieving GitHub repository details by owner and repository name. Parameters embedded in the URI (e.g., `{city}`, `{owner}`, `{repo}`) are automatically mapped to function arguments, enabling dynamic resource generation based on client requests.
SOURCE: https://gofastmcp.com/servers/resources

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Template URI includes {city} placeholder
@mcp.resource("weather://{city}/current")
def get_weather(city: str) -> dict:
    """Provides weather information for a specific city."""
    # In a real implementation, this would call a weather API
    # Here we're using simplified logic for example purposes
    return {
        "city": city.capitalize(),
        "temperature": 22,
        "condition": "Sunny",
        "unit": "celsius"
    }

# Template with multiple parameters
@mcp.resource("repos://{owner}/{repo}/info")
def get_repo_info(owner: str, repo: str) -> dict:
    """Retrieves information about a GitHub repository."""
    # In a real implementation, this would call the GitHub API
    return {
        "owner": owner,
        "name": repo,
        "full_name": f"{owner}/{repo}",
        "stars": 120,
        "forks": 48
    }
```

----------------------------------------

TITLE: Handling Errors with FastMCP ToolError
DESCRIPTION: Illustrates the use of `fastmcp.exceptions.ToolError` for explicit error handling within a tool. Messages from `ToolError` are always sent to clients, providing controlled error feedback regardless of the `mask_error_details` setting. It also shows a standard `TypeError` which would be masked if `mask_error_details` is true.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        # Error messages from ToolError are always sent to clients,
        # regardless of mask_error_details setting
        raise ToolError("Division by zero is not allowed.")
    
    # If mask_error_details=True, this message would be masked
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers.")
        
    return a / b
```

----------------------------------------

TITLE: Initializing FastMCP Server in Python
DESCRIPTION: This snippet demonstrates how to create instances of the FastMCP server class. It shows basic instantiation with a name and how to include initial instructions to guide client interaction.
SOURCE: https://gofastmcp.com/servers/fastmcp

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP

# Create a basic server instance
mcp = FastMCP(name="MyAssistantServer")

# You can also add instructions for how to interact with the server
mcp_with_instructions = FastMCP(
    name="HelpfulAssistant",
    instructions="""
        This server provides data analysis tools.
        Call get_average() to analyze numerical data.
    """,
)
```

----------------------------------------

TITLE: Defining an Asynchronous FastMCP Tool for I/O Operations
DESCRIPTION: Illustrates defining an asynchronous tool with `async def` for I/O-bound operations like network requests. This approach prevents the server from blocking while waiting for external operations, improving responsiveness. It uses `aiohttp` for an example API call.
SOURCE: https://gofastmcp.com/servers/tools

LANGUAGE: Python
CODE:
```
@mcp.tool()
async def fetch_weather(city: str) -> dict:
    """Retrieve current weather conditions for a city."""
    # Use 'async def' for operations involving network calls, file I/O, etc.
    # This prevents blocking the server while waiting for external operations.
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/weather/{city}") as response:
            # Check response status before returning
            response.raise_for_status()
            return await response.json()
```

----------------------------------------

TITLE: Adding Custom Web Routes to FastMCP Server in Python
DESCRIPTION: This example illustrates how to add custom web routes to a FastMCP server using the `@mcp.custom_route` decorator. This allows for exposing simple HTTP endpoints, such as a health check, alongside the main MCP endpoint. It utilizes `starlette.requests.Request` and `starlette.responses.PlainTextResponse` for handling the web request and response.
SOURCE: https://gofastmcp.com/deployment/running-server

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    mcp.run()
```

----------------------------------------

TITLE: Complete FastMCP Server with Bearer Authentication - Python
DESCRIPTION: This comprehensive example demonstrates a FastMCP server with bearer token authentication. It generates an RSA key pair, creates an access token, sets up `BearerAuthProvider`, defines a `roll_dice` tool, and runs the server, printing the access token for development purposes. This token printing should be avoided in production.
SOURCE: https://gofastmcp.com/integrations/anthropic

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.bearer import RSAKeyPair
import random

key_pair = RSAKeyPair.generate()
access_token = key_pair.create_token(audience="dice-server")

auth = BearerAuthProvider(
    public_key=key_pair.public_key,
    audience="dice-server",
)

mcp = FastMCP(name="Dice Roller", auth=auth)

@mcp.tool()
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    print(f"\n---\n\n🔑 Dice Roller access token:\n\n{access_token}\n\n---\n")
    mcp.run(transport="sse", port=8000)
```

----------------------------------------

TITLE: Running FastMCP Server with `run()` Method (Python)
DESCRIPTION: This snippet demonstrates how to run a FastMCP server directly from a Python script by calling the `run()` method on a `FastMCP` instance. Placing the `run()` call within an `if __name__ == "__main__":` block ensures the server starts only when the script is executed directly, not when imported as a module. This method is suitable for local execution and basic server setup.
SOURCE: https://gofastmcp.com/deployment/running-server

LANGUAGE: Python
CODE:
```
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

----------------------------------------

TITLE: Adding Custom Starlette Middleware to FastMCP ASGI Apps (Python)
DESCRIPTION: This snippet illustrates how to integrate custom Starlette middleware, such as `CORSMiddleware`, into a FastMCP ASGI application. It demonstrates defining a list of middleware instances and passing them to the `http_app()` method during app creation.
SOURCE: https://gofastmcp.com/deployment/asgi

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Define custom middleware
custom_middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"]),
]

# Create ASGI app with custom middleware
http_app = mcp.http_app(middleware=custom_middleware)
```

----------------------------------------

TITLE: Configuring FastMCP Server Settings - Python
DESCRIPTION: This snippet demonstrates how to configure a FastMCP server during its initialization using various parameters that map to `ServerSettings`. It shows setting the server's `name`, `port`, and behavior for `on_duplicate_tools`. The example also illustrates how to access these configured settings via the `mcp.settings` attribute after the server has been initialized.
SOURCE: https://gofastmcp.com/servers/fastmcp

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP

# Configure during initialization
mcp = FastMCP(
    name="ConfiguredServer",
    port=8080, # Directly maps to ServerSettings
    on_duplicate_tools="error" # Set duplicate handling
)

# Settings are accessible via mcp.settings
print(mcp.settings.port) # Output: 8080
print(mcp.settings.on_duplicate_tools) # Output: "error"
```

----------------------------------------

TITLE: Authenticating OpenAI Client with FastMCP Server using Bearer Token (Python)
DESCRIPTION: This snippet demonstrates how to authenticate an OpenAI client when interacting with a FastMCP server. It shows how to include the bearer token in the `Authorization` header within the `mcp` tool configuration, enabling successful communication with the secured server.
SOURCE: https://gofastmcp.com/integrations/openai

LANGUAGE: python
CODE:
```
from openai import OpenAI

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

# Your access token (replace with your actual token)
access_token = 'your-access-token'

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "dice_server",
            "server_url": f"{url}/sse",
            "require_approval": "never",
            "headers": {
                "Authorization": f"Bearer {access_token}"
            }
        },
    ],
    input="Roll a few dice!",
)

print(resp.output_text)
```

----------------------------------------

TITLE: Running FastMCP Asynchronously with run_async() in Python
DESCRIPTION: This snippet demonstrates how to run a FastMCP server asynchronously using `mcp.run_async()`. This method is essential when integrating FastMCP into an application that is already operating within an asynchronous event loop, preventing conflicts that arise from `mcp.run()` attempting to create a new loop. It shows the setup of a tool and the main async function to start the server.
SOURCE: https://gofastmcp.com/deployment/running-server

LANGUAGE: python
CODE:
```
from fastmcp import FastMCP
import asyncio

mcp = FastMCP(name="MyServer")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

async def main():
    # Use run_async() in async contexts
    await mcp.run_async(transport="streamable-http")

if __name__ == "__main__":
    asyncio.run(main())
```