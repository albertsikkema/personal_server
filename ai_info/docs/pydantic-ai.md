# pydantic ai Documentation
> Source: https://context7.com/pydantic/pydantic-ai/llms.txt
> Retrieved: 2025-06-27

TITLE: PydanticAI ModelProfile and OpenAIModelProfile Reference
DESCRIPTION: These profile classes allow fine-grained control over model behavior. `ModelProfile` offers general customizations applicable to any model class, while `OpenAIModelProfile` provides additional settings specific to `OpenAIModel`, such as strict tool definition support.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_17

LANGUAGE: APIDOC
CODE:
```
ModelProfile:
  json_schema_transformer: Type[JsonSchemaTransformer]
    A class or instance that transforms JSON schemas for tool definitions.

OpenAIModelProfile (inherits from ModelProfile):
  openai_supports_strict_tool_definition: bool
    Indicates whether the OpenAI-compatible model supports strict tool definitions.
```

----------------------------------------

TITLE: PydanticAI OpenAIProvider Class Reference
DESCRIPTION: The `OpenAIProvider` class configures access to generic OpenAI-compatible API endpoints. It requires a `base_url` for the API endpoint and an `api_key` for authentication, enabling connection to various self-hosted or third-party compatible services.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_15

LANGUAGE: APIDOC
CODE:
```
OpenAIProvider:
  __init__(
    base_url: str,
    api_key: str
  )
    base_url (str): The full URL of the OpenAI-compatible API endpoint.
    api_key (str): The API key for authentication with the service.
```

----------------------------------------

TITLE: Configure Custom HTTP Client for PydanticAI Providers
DESCRIPTION: This snippet shows how to provide a custom `httpx.AsyncClient` to a PydanticAI provider, such as `DeepSeekProvider`. This allows for advanced HTTP client configurations like custom timeouts, which can be useful for specific network environments or long-running requests.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_13

LANGUAGE: python
CODE:
```
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

custom_http_client = AsyncClient(timeout=30)
model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(
        api_key='your-deepseek-api-key', http_client=custom_http_client
    ),
)
agent = Agent(model)
...
```

----------------------------------------

TITLE: PydanticAI OpenAIModel Class Reference
DESCRIPTION: The `OpenAIModel` class is used to interact with OpenAI-compatible language models. It allows specifying the model name, the provider (either a string shorthand or an explicit provider instance), and an optional model profile for advanced customization of its behavior.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_14

LANGUAGE: APIDOC
CODE:
```
OpenAIModel:
  __init__(
    model_name: str,
    provider: Union[str, OpenAIProvider, DeepSeekProvider],
    profile: Optional[Union[ModelProfile, OpenAIModelProfile]] = None
  )
    model_name (str): The name of the OpenAI-compatible model (e.g., 'gpt-4', 'deepseek-chat').
    provider (Union[str, OpenAIProvider, DeepSeekProvider]): The provider to use. Can be a string shorthand (e.g., 'deepseek') or an instantiated provider class.
    profile (Optional[Union[ModelProfile, OpenAIModelProfile]]): An optional model profile to customize behavior.
```

----------------------------------------

TITLE: Configure Heroku AI Environment Variables
DESCRIPTION: Illustrates how to set `HEROKU_INFERENCE_KEY` and `HEROKU_INFERENCE_URL` as environment variables. This provides an alternative method for configuring Heroku AI credentials and base URL, which can be useful for deployment or CI/CD pipelines.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_28

LANGUAGE: bash
CODE:
```
export HEROKU_INFERENCE_KEY='your-heroku-inference-key'
export HEROKU_INFERENCE_URL='https://us.inference.heroku.com'
```

----------------------------------------

TITLE: Initialize Agent with Together AI Provider
DESCRIPTION: Demonstrates how to configure and use the `TogetherProvider` with `pydantic-ai`'s `Agent` and `OpenAIModel` classes. This snippet shows how to specify a Together AI model and pass the API key for authentication.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_26

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.together import TogetherProvider

model = OpenAIModel(
    'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free',  # model library available at https://www.together.ai/models
    provider=TogetherProvider(api_key='your-together-api-key'),
)
agent = Agent(model)
...
```

----------------------------------------

TITLE: Initialize Agent with Heroku AI Provider
DESCRIPTION: Shows how to set up `pydantic-ai`'s `Agent` using `HerokuProvider` and `OpenAIModel` for Heroku AI. This example includes selecting a specific model and configuring the API key for inference.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_27

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.heroku import HerokuProvider

model = OpenAIModel(
    'claude-3-7-sonnet',
    provider=HerokuProvider(api_key='your-heroku-inference-key'),
)
agent = Agent(model)
...
```

----------------------------------------

TITLE: Pydantic-AI Fireworks AI Integration
DESCRIPTION: Example of integrating pydantic-ai with Fireworks AI. This snippet demonstrates using FireworksProvider with an API key and specifying a model from the Fireworks AI library.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_25

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.fireworks import FireworksProvider

model = OpenAIModel(
    'accounts/fireworks/models/qwq-32b', # model library available at https://fireworks.ai/models
    provider=FireworksProvider(api_key='your-fireworks-api-key'),
)
agent = Agent(model)
...
```

----------------------------------------

TITLE: Initialize Pydantic-AI Agent with OpenAI Responses API Model
DESCRIPTION: Demonstrates how to use `OpenAIResponsesModel` to interact with OpenAI's Responses API, which provides built-in tools for enhanced model capabilities.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_7

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel

model = OpenAIResponsesModel('gpt-4o')
agent = Agent(model)
...
```

----------------------------------------

TITLE: PydanticAI DeepSeekProvider Class Reference
DESCRIPTION: The `DeepSeekProvider` class is specifically designed for integrating with DeepSeek's API. It simplifies configuration by handling the base URL internally and allows for a custom HTTP client for advanced network configurations.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_16

LANGUAGE: APIDOC
CODE:
```
DeepSeekProvider:
  __init__(
    api_key: str,
    http_client: Optional[httpx.AsyncClient] = None
  )
    api_key (str): The API key for DeepSeek.
    http_client (Optional[httpx.AsyncClient]): An optional custom HTTP client for advanced network configurations.
```

----------------------------------------

TITLE: Run PydanticAI Agent with Sync, Async, and Stream Methods
DESCRIPTION: Demonstrates the primary ways to execute a PydanticAI agent: `agent.run_sync()` for immediate synchronous results, `agent.run()` for asynchronous execution returning a completed response, and `agent.run_stream()` for streaming responses asynchronously. Each method returns a `RunResult` or `StreamedRunResult`.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_1

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.output)
#> Rome


async def main():
    result = await agent.run('What is the capital of France?')
    print(result.output)
    #> Paris

    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_output())
        #> London
```

----------------------------------------

TITLE: Configure PydanticAI Agent Model Settings (Temperature)
DESCRIPTION: This example shows how to apply `ModelSettings` to fine-tune the behavior of a PydanticAI agent. Specifically, it demonstrates setting the `temperature` parameter to `0.0` to ensure less random and more deterministic model outputs.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_9

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync(
    'What is the capital of Italy?', model_settings={'temperature': 0.0}
)
print(result_sync.output)
#> Rome
```

----------------------------------------

TITLE: Initialize Pydantic-AI Agent with OpenAI Model Name
DESCRIPTION: Shows how to create an `Agent` instance by directly passing an OpenAI model name string, leveraging default configurations and environment variables for the API key.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_2

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
...
```

----------------------------------------

TITLE: Set Gemini API Key Environment Variable
DESCRIPTION: This command sets the `GEMINI_API_KEY` environment variable, allowing PydanticAI to authenticate with Google's Generative Language API. Replace `your-api-key` with the actual API key obtained from Google AI Studio. This is a common method for securely providing credentials to applications.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/gemini.md#_snippet_0

LANGUAGE: bash
CODE:
```
export GEMINI_API_KEY=your-api-key
```

----------------------------------------

TITLE: Set OpenAI API Key Environment Variable
DESCRIPTION: Before using `clai` with OpenAI models, set the `OPENAI_API_KEY` environment variable to your personal API key. This allows `clai` to authenticate with the OpenAI service.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/clai/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
export OPENAI_API_KEY='your-api-key-here'
```

----------------------------------------

TITLE: Mypy Output for Pydantic-AI Type Checking Errors
DESCRIPTION: This snippet displays the console output from running `mypy` on the `type_mistakes.py` example. It clearly shows the specific type errors identified by `mypy`, including `arg-type` mismatches for `system_prompt` and `foobar` function arguments, demonstrating how static analysis helps catch issues.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_14

LANGUAGE: bash
CODE:
```
uv run mypy type_mistakes.py
type_mistakes.py:18: error: Argument 1 to "system_prompt" of "Agent" has incompatible type "Callable[[RunContext[str]], str]"; expected "Callable[[RunContext[User]], str]"  [arg-type]
type_mistakes.py:28: error: Argument 1 to "foobar" has incompatible type "bool"; expected "bytes"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
```

----------------------------------------

TITLE: Streaming Pydantic-AI Agent Run with Async Iteration
DESCRIPTION: This Python code snippet illustrates how to set up an `Agent` with custom tools and stream its execution. It defines a `WeatherService` with methods for fetching weather forecasts, which are then exposed as an agent tool. The `main` function demonstrates iterating over the agent's run nodes asynchronously, capturing and processing events related to user prompts, model requests, and tool invocations to provide real-time feedback on the agent's progress.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_6

LANGUAGE: python
CODE:
```
import asyncio
from dataclasses import dataclass
from datetime import date

from pydantic_ai import Agent
from pydantic_ai.messages import (
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
    ToolCallPartDelta,
)
from pydantic_ai.tools import RunContext


@dataclass
class WeatherService:
    async def get_forecast(self, location: str, forecast_date: date) -> str:
        # In real code: call weather API, DB queries, etc.
        return f'The forecast in {location} on {forecast_date} is 24°C and sunny.'

    async def get_historic_weather(self, location: str, forecast_date: date) -> str:
        # In real code: call a historical weather API or DB
        return (
            f'The weather in {location} on {forecast_date} was 18°C and partly cloudy.'
        )


weather_agent = Agent[WeatherService, str](
    'openai:gpt-4o',
    deps_type=WeatherService,
    output_type=str,  # We'll produce a final answer as plain text
    system_prompt='Providing a weather forecast at the locations the user provides.',
)


@weather_agent.tool
async def weather_forecast(
    ctx: RunContext[WeatherService],
    location: str,
    forecast_date: date,
) -> str:
    if forecast_date >= date.today():
        return await ctx.deps.get_forecast(location, forecast_date)
    else:
        return await ctx.deps.get_historic_weather(location, forecast_date)


output_messages: list[str] = []


async def main():
    user_prompt = 'What will the weather be like in Paris on Tuesday?'

    # Begin a node-by-node, streaming iteration
    async with weather_agent.iter(user_prompt, deps=WeatherService()) as run:
        async for node in run:
            if Agent.is_user_prompt_node(node):
                # A user prompt node => The user has provided input
                output_messages.append(f'=== UserPromptNode: {node.user_prompt} ===')
            elif Agent.is_model_request_node(node):
                # A model request node => We can stream tokens from the model's request
                output_messages.append(
                    '=== ModelRequestNode: streaming partial request tokens ==='
                )
                async with node.stream(run.ctx) as request_stream:
                    async for event in request_stream:
                        if isinstance(event, PartStartEvent):
                            output_messages.append(
                                f'[Request] Starting part {event.index}: {event.part!r}'
                            )
                        elif isinstance(event, PartDeltaEvent):
                            if isinstance(event.delta, TextPartDelta):
                                output_messages.append(
                                    f'[Request] Part {event.index} text delta: {event.delta.content_delta!r}'
                                )
                            elif isinstance(event.delta, ToolCallPartDelta):
                                output_messages.append(
                                    f'[Request] Part {event.index} args_delta={event.delta.args_delta}'
                                )
                        elif isinstance(event, FinalResultEvent):
                            output_messages.append(
                                f'[Result] The model produced a final output (tool_name={event.tool_name})'
                            )
            elif Agent.is_call_tools_node(node):
                # A handle-response node => The model returned some data, potentially calls a tool
                output_messages.append(
                    '=== CallToolsNode: streaming partial response & tool usage ==='
                )
                async with node.stream(run.ctx) as handle_stream:
                    async for event in handle_stream:
                        if isinstance(event, FunctionToolCallEvent):
                            output_messages.append(
                                f'[Tools] The LLM calls tool={event.part.tool_name!r} with args={event.part.args} (tool_call_id={event.part.tool_call_id!r})'
                            )
                        elif isinstance(event, FunctionToolResultEvent):
                            output_messages.append(
                                f'[Tools] Tool call {event.tool_call_id!r} returned => {event.result.content}'
                            )
            elif Agent.is_end_node(node):
                assert run.result.output == node.data.output
                # Once an End node is reached, the agent run is complete
                output_messages.append(
                    f'=== Final Agent Output: {run.result.output} ==='
                )


if __name__ == '__main__':
    asyncio.run(main())

    print(output_messages)
```

----------------------------------------

TITLE: Install PydanticAI Slim with OpenAI Model
DESCRIPTION: For users who know they will only use specific models, the `pydantic-ai-slim` package can be installed with targeted optional groups. This command installs `pydantic-ai-slim` specifically for the OpenAI model, avoiding unnecessary package installations.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/install.md#_snippet_3

LANGUAGE: bash
CODE:
```
pip/uv-add "pydantic-ai-slim[openai]"
```

----------------------------------------

TITLE: Define Custom PydanticAI Agent
DESCRIPTION: You can define a custom `Agent` instance in a Python file to customize behavior, such as setting specific instructions for the LLM. This agent can then be used with the CLI.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/cli.md#_snippet_6

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', instructions='You always respond in Italian.')
```

----------------------------------------

TITLE: Specify LLM Model for PydanticAI CLI
DESCRIPTION: The `--model` flag allows you to specify which large language model to use for the interactive session. This enables switching between different providers and model versions.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/cli.md#_snippet_5

LANGUAGE: bash
CODE:
```
uvx clai --model anthropic:claude-3-7-sonnet-latest
```

----------------------------------------

TITLE: Limit PydanticAI Agent Response Tokens
DESCRIPTION: This example demonstrates how to use `UsageLimits` to restrict the number of tokens generated in a model's response. It shows how to set a `response_tokens_limit` and how `UsageLimitExceeded` exceptions are raised when the limit is surpassed.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_7

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.usage import UsageLimits

agent = Agent('anthropic:claude-3-5-sonnet-latest')

result_sync = agent.run_sync(
    'What is the capital of Italy? Answer with just the city.',
    usage_limits=UsageLimits(response_tokens_limit=10),
)
print(result_sync.output)
#> Rome
print(result_sync.usage())
#> Usage(requests=1, request_tokens=62, response_tokens=1, total_tokens=63)

try:
    result_sync = agent.run_sync(
        'What is the capital of Italy? Answer with a paragraph.',
        usage_limits=UsageLimits(response_tokens_limit=10),
    )
except UsageLimitExceeded as e:
    print(e)
    #> Exceeded the response_tokens_limit of 10 (response_tokens=32)
```

----------------------------------------

TITLE: Run PydanticAI CLI with Custom Agent
DESCRIPTION: To use a custom agent defined in a Python module, specify its path and variable name using the `--agent` flag. This allows the CLI to load and utilize your custom agent's configuration.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/cli.md#_snippet_7

LANGUAGE: bash
CODE:
```
uvx clai --agent custom_agent:agent "What's the weather today?"
```

----------------------------------------

TITLE: Run PydanticAI CLI with uvx
DESCRIPTION: After setting the API key, you can run the `clai` interactive session using `uvx`. This command launches the CLI directly without global installation.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/cli.md#_snippet_1

LANGUAGE: bash
CODE:
```
uvx clai
```

----------------------------------------

TITLE: PydanticAI Agent Execution Methods API Reference
DESCRIPTION: Detailed API documentation for the core methods used to run and inspect PydanticAI agents, including their purpose, parameters, and return types.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_3

LANGUAGE: APIDOC
CODE:
```
Agent:
  run() -> RunResult (coroutine)
    Description: Executes the agent asynchronously and returns a completed response.
  run_sync() -> RunResult
    Description: Executes the agent synchronously, internally calling `run()` via `loop.run_until_complete()`.
  run_stream() -> StreamedRunResult (coroutine)
    Description: Executes the agent asynchronously and returns an object for streaming the response.
  iter() -> AgentRun (context manager)
    Description: Returns an async-iterable `AgentRun` object for iterating over the agent's underlying graph nodes.

AgentRun:
  __aiter__() -> BaseNode | End
    Description: Async-iterates over the nodes of the agent's graph.
  next() -> BaseNode | End
    Description: Manually drives the agent's graph node-by-node.
  result: FinalResult
    Description: The final result of the agent run, available after the run completes.

RunResult:
  output: Any
    Description: The final output of the agent run.

StreamedRunResult:
  get_output() -> Any (coroutine)
    Description: Retrieves the final output from the streamed response.

BaseNode:
  Description: Base class for nodes in the pydantic-graph, representing steps in the agent's execution.
  Examples: UserPromptNode, ModelRequestNode, CallToolsNode.

End:
  data: FinalResult
    Description: A special node indicating the end of the agent's execution, containing the final result.
```

----------------------------------------

TITLE: Launch PydanticAI CLI from Agent Instance (Synchronous)
DESCRIPTION: An `Agent` instance can directly launch an interactive CLI session using the `to_cli_sync()` method. This is useful for embedding CLI functionality within a Python application.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/cli.md#_snippet_8

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', instructions='You always respond in Italian.')
agent.to_cli_sync()
```

----------------------------------------

TITLE: Set Groq API Key environment variable
DESCRIPTION: Demonstrates how to set the `GROQ_API_KEY` environment variable, which `pydantic-ai` uses to authenticate with the Groq API. This is the recommended way to manage your API key.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/groq.md#_snippet_1

LANGUAGE: bash
CODE:
```
export GROQ_API_KEY='your-api-key'
```

----------------------------------------

TITLE: Iterate PydanticAI Agent Graph with Async For
DESCRIPTION: Illustrates how to use `agent.iter()` as an async context manager to gain fine-grained control over an agent's execution. It shows how to asynchronously iterate over the `AgentRun` object, yielding each node (e.g., `UserPromptNode`, `ModelRequestNode`, `CallToolsNode`, `End`) in the agent's underlying pydantic-graph, allowing for detailed inspection of the execution flow.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_2

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')


async def main():
    nodes = []
    # Begin an AgentRun, which is an async-iterable over the nodes of the agent's graph
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            # Each node represents a step in the agent's execution
            nodes.append(node)
    print(nodes)
    """
    [
        UserPromptNode(
            user_prompt='What is the capital of France?',
            instructions=None,
            instructions_functions=[],
            system_prompts=(),
            system_prompt_functions=[],
            system_prompt_dynamic_functions={},
        ),
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                    )
                ]
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='Paris')],
                usage=(
                    Usage(
                        requests=1, request_tokens=56, response_tokens=1, total_tokens=57
                    )
                ),
                model_name='gpt-4o',
                timestamp=datetime.datetime(...),
            )
        ),
        End(data=FinalResult(output='Paris')),
    ]
    """
    print(agent_run.result.output)
    #> Paris
```

----------------------------------------

TITLE: Set Cohere API Key Environment Variable
DESCRIPTION: This command sets the `CO_API_KEY` environment variable with your Cohere API key. This is a common method for securely providing credentials to applications without hardcoding them.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/cohere.md#_snippet_1

LANGUAGE: bash
CODE:
```
export CO_API_KEY='your-api-key'
```

----------------------------------------

TITLE: Initialize pydantic-ai Agent with BedrockConverseModel Object
DESCRIPTION: Illustrates how to explicitly instantiate a `BedrockConverseModel` object with a specific model name and then pass this object to the `pydantic-ai` Agent. This approach offers more granular control over the model instance.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/bedrock.md#_snippet_3

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel

model = BedrockConverseModel('anthropic.claude-3-sonnet-20240229-v1:0')
agent = Agent(model)
...
```

----------------------------------------

TITLE: Install GoogleModel Package
DESCRIPTION: Instructions on how to install the necessary `pydantic-ai-slim` package with the `google` optional group using `pip` or `uv` to enable `GoogleModel` functionality.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/google.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip/uv-add "pydantic-ai-slim[google]"
```

----------------------------------------

TITLE: Manual AgentRun Iteration with .next(...)
DESCRIPTION: This example demonstrates how to manually drive the iteration of an `AgentRun` instance in Pydantic-AI. By passing the current node to `agent_run.next(...)`, developers can inspect or modify nodes before execution, implement custom logic for skipping nodes, and handle errors more effectively during the agent's graph traversal.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_4

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_graph import End

agent = Agent('openai:gpt-4o')


async def main():
    async with agent.iter('What is the capital of France?') as agent_run:
        node = agent_run.next_node  # (1)!

        all_nodes = [node]

        # Drive the iteration manually:
        while not isinstance(node, End):  # (2)!
            node = await agent_run.next(node)  # (3)!
            all_nodes.append(node)  # (4)!

        print(all_nodes)
        """
        [
            UserPromptNode(
                user_prompt='What is the capital of France?',
                instructions=None,
                instructions_functions=[],
                system_prompts=(),
                system_prompt_functions=[],
                system_prompt_dynamic_functions={},
            ),
            ModelRequestNode(
                request=ModelRequest(
                    parts=[
                        UserPromptPart(
                            content='What is the capital of France?',
                            timestamp=datetime.datetime(...),
                        )
                    ]
                )
            ),
            CallToolsNode(
                model_response=ModelResponse(
                    parts=[TextPart(content='Paris')],
                    usage=Usage(
                        requests=1,
                        request_tokens=56,
                        response_tokens=1,
                        total_tokens=57,
                    ),
                    model_name='gpt-4o',
                    timestamp=datetime.datetime(...),
                )
            ),
            End(data=FinalResult(output='Paris')),
        ]
        """
```

----------------------------------------

TITLE: Set OpenAI API Key environment variable
DESCRIPTION: Sets the `OPENAI_API_KEY` environment variable, which is crucial for authenticating with OpenAI models when running PydanticAI examples that interact with OpenAI services.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/examples/index.md#_snippet_2

LANGUAGE: bash
CODE:
```
export OPENAI_API_KEY=your-api-key
```

----------------------------------------

TITLE: Configure OpenAIProvider with API Key Programmatically
DESCRIPTION: Demonstrates how to explicitly instantiate `OpenAIProvider` with an API key and pass it to `OpenAIModel` for fine-grained control over the provider's configuration, overriding environment variables.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/openai.md#_snippet_4

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel('gpt-4o', provider=OpenAIProvider(api_key='your-api-key'))
agent = Agent(model)
...
```

----------------------------------------

TITLE: Manage Multi-Turn Conversations with Pydantic-AI Agent
DESCRIPTION: This example illustrates how to maintain conversational context across multiple `Agent` runs by passing `message_history`. It shows two sequential calls to `agent.run_sync`, where the second call uses messages from the first to understand context, preventing the model from losing track of previous turns.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/agents.md#_snippet_12

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# First run
result1 = agent.run_sync('Who was Albert Einstein?')
print(result1.output)
# Albert Einstein was a German-born theoretical physicist.

# Second run, passing previous messages
result2 = agent.run_sync(
    'What was his most famous equation?',
    message_history=result1.new_messages(),  # (1)!
)
print(result2.output)
# Albert Einstein's most famous equation is (E = mc^2).
```

----------------------------------------

TITLE: PydanticAI: Custom History Processor to Keep Only Recent Messages
DESCRIPTION: This Python snippet demonstrates another custom history processor for PydanticAI agents, designed to manage token usage by keeping only the most recent messages in the conversation history. The `keep_recent_messages` asynchronous function truncates the message list to the last five entries, preventing excessively long contexts from being sent to the LLM.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/message-history.md#_snippet_7

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage


async def keep_recent_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Keep only the last 5 messages to manage token usage."""
    return messages[-5:] if len(messages) > 5 else messages

agent = Agent('openai:gpt-4o', history_processors=[keep_recent_messages])

# Example: Even with a long conversation history, only the last 5 messages are sent to the model
long_conversation_history: list[ModelMessage] = []  # Your long conversation history here
# result = agent.run_sync('What did we discuss?', message_history=long_conversation_history)
```

----------------------------------------

TITLE: Storing and loading PydanticAI messages to JSON
DESCRIPTION: Illustrates methods for serializing and deserializing PydanticAI message histories to and from JSON, enabling persistence of conversation state for various use cases like evaluations or data sharing. It shows using `ModelMessagesTypeAdapter` with `pydantic_core.to_jsonable_python` and provides alternatives for creating the adapter and direct JSON handling.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/message-history.md#_snippet_4

LANGUAGE: python
CODE:
```
from pydantic_core import to_jsonable_python

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter

agent = Agent('openai:gpt-4o', system_prompt='Be a helpful assistant.')

result1 = agent.run_sync('Tell me a joke.')
history_step_1 = result1.all_messages()
as_python_objects = to_jsonable_python(history_step_1)
same_history_as_step_1 = ModelMessagesTypeAdapter.validate_python(as_python_objects)

result2 = agent.run_sync(
    'Tell me a different joke.', message_history=same_history_as_step_1
)
```

LANGUAGE: python
CODE:
```
from pydantic import TypeAdapter
from pydantic_ai.messages import ModelMessage
ModelMessagesTypeAdapter = TypeAdapter(list[ModelMessage])
```

LANGUAGE: python
CODE:
```
from pydantic_core import to_json
# ... (assuming history_step_1 is available)
as_json_objects = to_json(history_step_1)
same_history_as_step_1 = ModelMessagesTypeAdapter.validate_json(as_json_objects)
```

----------------------------------------

TITLE: Configure PydanticAI Event Mode for OpenTelemetry
DESCRIPTION: Illustrates how to change PydanticAI's OpenTelemetry event capturing from a single `events` attribute to individual log events using `logfire.instrument_pydantic_ai(event_mode='logs')`. This helps avoid truncation for long conversations by emitting messages as separate events.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/logfire.md#_snippet_9

LANGUAGE: python
CODE:
```
import logfire

from pydantic_ai import Agent

logfire.configure()
logfire.instrument_pydantic_ai(event_mode='logs')
agent = Agent('openai:gpt-4o')
result = agent.run_sync('What is the capital of France?')
print(result.output)
#> Paris
```

----------------------------------------

TITLE: Set Custom OpenTelemetry Providers for PydanticAI
DESCRIPTION: Shows how to explicitly set custom `TracerProvider` and `EventLoggerProvider` instances for PydanticAI's instrumentation using `InstrumentationSettings`. This allows for fine-grained control over which OpenTelemetry SDK providers are used for tracing and event logging, either per agent or globally.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/logfire.md#_snippet_10

LANGUAGE: python
CODE:
```
from opentelemetry.sdk._events import EventLoggerProvider
from opentelemetry.sdk.trace import TracerProvider

from pydantic_ai.agent import Agent, InstrumentationSettings

instrumentation_settings = InstrumentationSettings(
    tracer_provider=TracerProvider(),
    event_logger_provider=EventLoggerProvider(),
)

agent = Agent('gpt-4o', instrument=instrumentation_settings)
# or to instrument all agents:
Agent.instrument_all(instrumentation_settings)
```

----------------------------------------

TITLE: Inspect Agent Conversation Messages and Tool Calls in Python
DESCRIPTION: This Python snippet demonstrates how to retrieve and print the complete message history of an agent's run. It showcases the structured output, including `SystemPromptPart`, `UserPromptPart`, `ModelResponse` with `ToolCallPart`, and `ToolReturnPart`, providing insight into the agent's internal reasoning and tool interactions.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/tools.md#_snippet_2

LANGUAGE: python
CODE:
```
from dice_game import dice_result

print(dice_result.all_messages())
"""
[
    ModelRequest(
        parts=[
            SystemPromptPart(
                content="You're a dice game, you should roll the die and see if the number you get back matches the user's guess. If so, tell them they're a winner. Use the player's name in the response.",
                timestamp=datetime.datetime(...),
            ),
            UserPromptPart(
                content='My guess is 4',
                timestamp=datetime.datetime(...),
            ),
        ]
    ),
    ModelResponse(
        parts=[
            ToolCallPart(
                tool_name='roll_dice', args={}, tool_call_id='pyd_ai_tool_call_id'
            )
        ],
        usage=Usage(requests=1, request_tokens=90, response_tokens=2, total_tokens=92),
        model_name='gemini-1.5-flash',
        timestamp=datetime.datetime(...),
    ),
    ModelRequest(
        parts=[
            ToolReturnPart(
                tool_name='roll_dice',
                content='4',
                tool_call_id='pyd_ai_tool_call_id',
                timestamp=datetime.datetime(...),
            )
        ]
    ),
    ModelResponse(
        parts=[
            ToolCallPart(
                tool_name='get_player_name', args={}, tool_call_id='pyd_ai_tool_call_id'
            )
        ],
        usage=Usage(requests=1, request_tokens=91, response_tokens=4, total_tokens=95),
        model_name='gemini-1.5-flash',
        timestamp=datetime.datetime(...),
    ),
    ModelRequest(
        parts=[
            ToolReturnPart(
                tool_name='get_player_name',
                content='Anne',
                tool_call_id='pyd_ai_tool_call_id',
                timestamp=datetime.datetime(...),
            )
        ]
    ),
    ModelResponse(
        parts=[
            TextPart(
                content="Congratulations Anne, you guessed correctly! You're a winner!"
            )
        ],
        usage=(
            requests=1, request_tokens=92, response_tokens=12, total_tokens=104
        ),
        model_name='gemini-1.5-flash',
        timestamp=datetime.datetime(...),
    ),
]
"""
```

----------------------------------------

TITLE: Handling Diverse Function Tool Outputs in Pydantic-AI
DESCRIPTION: This example illustrates the flexibility of Pydantic-AI function tools in handling various return types. It showcases tools returning standard Python objects like `datetime`, custom Pydantic `BaseModel` instances, and multi-modal content represented by `ImageUrl` and `DocumentUrl`. The snippet also highlights how Pydantic-AI serializes Python objects to JSON when the model expects a string output.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/tools.md#_snippet_5

LANGUAGE: python
CODE:
```
from datetime import datetime

from pydantic import BaseModel

from pydantic_ai import Agent, DocumentUrl, ImageUrl
from pydantic_ai.models.openai import OpenAIResponsesModel


class User(BaseModel):
    name: str
    age: int


agent = Agent(model=OpenAIResponsesModel('gpt-4o'))


@agent.tool_plain
def get_current_time() -> datetime:
    return datetime.now()


@agent.tool_plain
def get_user() -> User:
    return User(name='John', age=30)


@agent.tool_plain
def get_company_logo() -> ImageUrl:
    return ImageUrl(url='https://iili.io/3Hs4FMg.png')


@agent.tool_plain
def get_document() -> DocumentUrl:
    return DocumentUrl(url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf')


result = agent.run_sync('What time is it?')
print(result.output)
#> The current time is 10:45 PM on April 17, 2025.

result = agent.run_sync('What is the user name?')
print(result.output)
#> The user's name is John.

result = agent.run_sync('What is the company name in the logo?')
print(result.output)
#> The company name in the logo is "Pydantic."

result = agent.run_sync('What is the main content of the document?')
print(result.output)
#> The document contains just the text "Dummy PDF file."
```

----------------------------------------

TITLE: PydanticAI: Reusing Message History Across Different Models
DESCRIPTION: This Python snippet demonstrates how to reuse a conversation's message history from one PydanticAI agent run with a different AI model in a subsequent run. It shows passing `result1.new_messages()` to `message_history` in a new `agent.run_sync()` call, effectively continuing a conversation with a different LLM while preserving context. The output includes the full message history, illustrating the `ModelRequest` and `ModelResponse` structure.
SOURCE: https://github.com/pydantic/pydantic-ai/blob/main/docs/message-history.md#_snippet_5

LANGUAGE: python
CODE:
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', system_prompt='Be a helpful assistant.')

result1 = agent.run_sync('Tell me a joke.')
print(result1.output)
# Did you hear about the toothpaste scandal? They called it Colgate.

result2 = agent.run_sync(
    'Explain?',
    model='google-gla:gemini-1.5-pro',
    message_history=result1.new_messages(),
)
print(result2.output)
# This is an excellent joke invented by Samuel Colvin, it needs no explanation.

print(result2.all_messages())
"""
[
    ModelRequest(
        parts=[
            SystemPromptPart(
                content='Be a helpful assistant.',
                timestamp=datetime.datetime(...),
            ),
            UserPromptPart(
                content='Tell me a joke.',
                timestamp=datetime.datetime(...),
            ),
        ]
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='Did you hear about the toothpaste scandal? They called it Colgate.'
            )
        ],
        usage=Usage(requests=1, request_tokens=60, response_tokens=12, total_tokens=72),
        model_name='gpt-4o',
        timestamp=datetime.datetime(...),
    ),
    ModelRequest(
        parts=[
            UserPromptPart(
                content='Explain?',
                timestamp=datetime.datetime(...),
            )
        ]
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='This is an excellent joke invented by Samuel Colvin, it needs no explanation.'
            )
        ],
        usage=Usage(requests=1, request_tokens=61, response_tokens=26, total_tokens=87),
        model_name='gemini-1.5-pro',
        timestamp=datetime.datetime(...),
    ),
]
"""
```