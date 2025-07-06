TITLE: Accessing CrawlResult Properties in Python
DESCRIPTION: The `arun()` method returns a `CrawlResult` object. This snippet demonstrates how to access various content formats (HTML, Markdown), check success status, and retrieve extracted media and links from the `CrawlResult`.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/simple-crawling.md#_snippet_1

LANGUAGE: python
CODE:
```
config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.6),
        options={"ignore_links": True}
    )
)

result = await crawler.arun(
    url="https://example.com",
    config=config
)

# Different content formats
print(result.html)         # Raw HTML
print(result.cleaned_html) # Cleaned HTML
print(result.markdown.raw_markdown) # Raw markdown from cleaned html
print(result.markdown.fit_markdown) # Most relevant content in markdown

# Check success status
print(result.success)      # True if crawl succeeded
print(result.status_code)  # HTTP status code (e.g., 200, 404)

# Access extracted media and links
print(result.media)        # Dictionary of found media (images, videos, audio)
print(result.links)        # Dictionary of internal and external links
```

----------------------------------------

TITLE: Run a Basic Crawl with AsyncWebCrawler in Python
DESCRIPTION: This snippet demonstrates how to perform a minimal web crawl using Crawl4AI's `AsyncWebCrawler`. It fetches a webpage, automatically converts its HTML content to Markdown, and prints the first 300 characters of the result. The crawler launches a headless Chromium browser by default.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/quickstart.md#_snippet_0

LANGUAGE: Python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:300])  # Print first 300 chars

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Install Core Crawl4AI Library
DESCRIPTION: Installs the core Crawl4AI library along with essential dependencies. This installation does not include advanced features like transformers or PyTorch.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/installation.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip install crawl4ai
```

----------------------------------------

TITLE: Perform Basic Web Crawl with Crawl4AI in Python
DESCRIPTION: Demonstrates how to use the `AsyncWebCrawler` class in Python to fetch content from a specified URL. The example shows how to asynchronously run a crawl and print the extracted content in Markdown format.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/README.md#_snippet_2

LANGUAGE: python
CODE:
```
import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Calling `arun()` with `CrawlerRunConfig`
DESCRIPTION: Demonstrates the updated method for invoking `crawler.arun()`, passing a `CrawlerRunConfig` object instead of direct parameters. This centralizes configuration for crawl operations.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/api/arun.md#_snippet_0

LANGUAGE: python
CODE:
```
await crawler.arun(
    url="https://example.com",  
    config=my_run_config
)
```

----------------------------------------

TITLE: Set up a Basic Web Crawl with Crawl4AI in Python
DESCRIPTION: Set up a simple crawl using `BrowserConfig` and `CrawlerRunConfig` to fetch content from a URL and print its markdown.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/simple-crawling.md#_snippet_0

LANGUAGE: python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def main():
    browser_config = BrowserConfig()  # Default browser configuration
    run_config = CrawlerRunConfig()   # Default crawl run configuration

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=run_config
        )
        print(result.markdown)  # Print clean markdown content

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Run Crawl4AI Diagnostics
DESCRIPTION: Optionally runs the `crawl4ai-doctor` command to perform diagnostics, checking Python version compatibility, Playwright installation, and inspecting environment variables or library conflicts.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/installation.md#_snippet_2

LANGUAGE: bash
CODE:
```
crawl4ai-doctor
```

----------------------------------------

TITLE: Comprehensive Web Crawling Example with Crawl4AI in Python
DESCRIPTION: A comprehensive example demonstrating common usage patterns including content filtering, processing options, cache control, and handling successful and failed crawl results.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/simple-crawling.md#_snippet_5

LANGUAGE: python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=10,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,
        
        # Content processing
        process_iframes=True,
        remove_overlay_elements=True,
        
        # Cache control
        cache_mode=CacheMode.ENABLED  # Use cache if available
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=run_config
        )
        
        if result.success:
            # Print clean content
            print("Content:", result.markdown[:500])  # First 500 chars
            
            # Process images
            for image in result.media["images"]:
                print(f"Found image: {image['src']}")
            
            # Process links
            for link in result.links["internal"]:
                print(f"Internal link: {link['href']}")
                
        else:
            print(f"Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Use AsyncWebCrawler with Async Context Manager
DESCRIPTION: Shows the recommended way to use `AsyncWebCrawler` within an `async with` statement. This pattern ensures that the crawler automatically starts and cleans up resources (like closing the browser) when the block exits, simplifying resource management.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/api/async-webcrawler.md#_snippet_2

LANGUAGE: python
CODE:
```
async with AsyncWebCrawler(config=browser_cfg) as crawler:
    result = await crawler.arun("https://example.com")
    # The crawler automatically starts/closes resources
```

----------------------------------------

TITLE: Verify Crawl4AI Installation with Basic Python Crawl
DESCRIPTION: A minimal asynchronous Python script demonstrating a basic web crawl to verify the installation. It uses `AsyncWebCrawler`, `BrowserConfig`, and `CrawlerRunConfig` to load `example.com` and print the first 300 characters of the extracted markdown.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/installation.md#_snippet_3

LANGUAGE: python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.example.com",
        )
        print(result.markdown[:300])  # Show the first 300 characters of extracted text

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Define E-commerce HTML Data Extraction Schema in Python
DESCRIPTION: This Python dictionary defines a comprehensive schema for extracting structured data from an e-commerce HTML page. It specifies selectors for categories, products, product details, features, reviews, and related products, demonstrating how to handle nested objects (`nested`), lists of simple items (`list`), and lists of complex objects (`nested_list`). It also shows how to extract attributes from base elements using `baseFields`.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/no-llm-strategies.md#_snippet_2

LANGUAGE: Python
CODE:
```
schema = {
    "name": "E-commerce Product Catalog",
    "baseSelector": "div.category",
    # (1) We can define optional baseFields if we want to extract attributes 
    # from the category container
    "baseFields": [
        {"name": "data_cat_id", "type": "attribute", "attribute": "data-cat-id"}, 
    ],
    "fields": [
        {
            "name": "category_name",
            "selector": "h2.category-name",
            "type": "text"
        },
        {
            "name": "products",
            "selector": "div.product",
            "type": "nested_list",    # repeated sub-objects
            "fields": [
                {
                    "name": "name",
                    "selector": "h3.product-name",
                    "type": "text"
                },
                {
                    "name": "price",
                    "selector": "p.product-price",
                    "type": "text"
                },
                {
                    "name": "details",
                    "selector": "div.product-details",
                    "type": "nested",  # single sub-object
                    "fields": [
                        {
                            "name": "brand",
                            "selector": "span.brand",
                            "type": "text"
                        },
                        {
                            "name": "model",
                            "selector": "span.model",
                            "type": "text"
                        }
                    ]
                },
                {
                    "name": "features",
                    "selector": "ul.product-features li",
                    "type": "list",
                    "fields": [
                        {"name": "feature", "type": "text"} 
                    ]
                },
                {
                    "name": "reviews",
                    "selector": "div.review",
                    "type": "nested_list",
                    "fields": [
                        {
                            "name": "reviewer", 
                            "selector": "span.reviewer", 
                            "type": "text"
                        },
                        {
                            "name": "rating", 
                            "selector": "span.rating", 
                            "type": "text"
                        },
                        {
                            "name": "comment", 
                            "selector": "p.review-text", 
                            "type": "text"
                        }
                    ]
                },
                {
                    "name": "related_products",
                    "selector": "ul.related-products li",
                    "type": "list",
                    "fields": [
                        {
                            "name": "name", 
                            "selector": "span.related-name", 
                            "type": "text"
                        },
                        {
                            "name": "price", 
                            "selector": "span.related-price", 
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    ]
}
```

----------------------------------------

TITLE: Run Crawl4AI with Docker Compose (Pre-built Image)
DESCRIPTION: Shows how to pull and run the latest pre-built Crawl4AI Docker image from Docker Hub using `docker compose`. This command automatically selects the correct architecture for your system.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_6

LANGUAGE: bash
CODE:
```
IMAGE=unclecode/crawl4ai:latest docker compose up -d
```

----------------------------------------

TITLE: Python: Using a Custom Dispatcher with arun_many
DESCRIPTION: Illustrates how to integrate a custom `MemoryAdaptiveDispatcher` with `arun_many`. This allows fine-grained control over concurrency and resource management during multi-URL crawls by setting specific memory thresholds and session permits.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/api/arun_many.md#_snippet_3

LANGUAGE: python
CODE:
```
dispatcher = MemoryAdaptiveDispatcher(
    memory_threshold_percent=70.0,
    max_session_permit=10
)
results = await crawler.arun_many(
    urls=["https://site1.com", "https://site2.com", "https://site3.com"],
    config=my_run_config,
    dispatcher=dispatcher
)
```

----------------------------------------

TITLE: Configure Browser and Crawler Settings in Python
DESCRIPTION: This example illustrates how to customize Crawl4AI's behavior using `BrowserConfig` for browser settings (e.g., headless mode) and `CrawlerRunConfig` for crawl-specific settings (e.g., cache mode). It shows how to pass these configuration objects to the `AsyncWebCrawler`.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/quickstart.md#_snippet_1

LANGUAGE: Python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=run_conf
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Run Crawl4AI Docker Container
DESCRIPTION: Commands to run the Crawl4AI Docker container in detached mode, mapping port 11235 and allocating shared memory. Options include running without LLM support or with LLM API keys loaded from a '.llm.env' file.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_2

LANGUAGE: bash
CODE:
```
docker run -d \
  -p 11235:11235 \
  --name crawl4ai \
  --shm-size=1g \
  unclecode/crawl4ai:latest
```

LANGUAGE: bash
CODE:
```
# Make sure .llm.env is in the current directory
docker run -d \
  -p 11235:11235 \
  --name crawl4ai \
  --env-file .llm.env \
  --shm-size=1g \
  unclecode/crawl4ai:latest
```

----------------------------------------

TITLE: Extract Structured Data using LLM Strategy with Crawl4AI
DESCRIPTION: Demonstrates using `LLMExtractionStrategy` to extract structured data (like OpenAI model pricing) from a webpage. It defines a Pydantic schema for the target data and configures the strategy with a provider, API token, and extraction instructions. This method is suitable for retrieving specific, schema-defined information.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/examples/quickstart.ipynb#_snippet_13

LANGUAGE: python
CODE:
```
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
import os, json

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(
        ..., description="Fee for output token for the OpenAI model."
    )

async def extract_structured_data_using_llm(provider: str, api_token: str = None, extra_headers: dict = None):
    print(f"\n--- Extracting Structured Data with {provider} ---")
    
    # Skip if API token is missing (for providers that require it)
    if api_token is None and provider != "ollama":
        print(f"API token is required for {provider}. Skipping this example.")
        return

    extra_args = {"extra_headers": extra_headers} if extra_headers else {}

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/",
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                provider=provider,
                api_token=api_token,
                schema=OpenAIModelFee.schema(),
                extraction_type="schema",
                instruction="""Extract all model names along with fees for input and output tokens."
                "{model_name: 'GPT-4', input_fee: 'US$10.00 / 1M tokens', output_fee: 'US$30.00 / 1M tokens'}.""",
                **extra_args
            ),
            bypass_cache=True,
        )
        print(json.loads(result.extracted_content)[:5])

# Usage:
await extract_structured_data_using_llm("openai/gpt-4o-mini", os.getenv("OPENAI_API_KEY"))
```

----------------------------------------

TITLE: Perform a Basic Web Crawl with Crawl4AI
DESCRIPTION: This example shows the fundamental setup for using `AsyncWebCrawler` to fetch content from a specified URL. It demonstrates how to initialize the crawler within an asynchronous context and retrieve the raw markdown content of a webpage, bypassing the cache.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/examples/quickstart.ipynb#_snippet_1

LANGUAGE: python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler

async def simple_crawl():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            bypass_cache=True # By default this is False, meaning the cache will be used
        )
        print(result.markdown.raw_markdown[:500])  # Print the first 500 characters
        
asyncio.run(simple_crawl())
```

----------------------------------------

TITLE: Extracting Common Entities with RegexExtractionStrategy
DESCRIPTION: This Python example illustrates the use of `crawl4ai`'s `RegexExtractionStrategy` to quickly extract common data types like URLs and currency values from a webpage. It leverages built-in pre-compiled regex patterns for efficient, zero-LLM data extraction.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/no-llm-strategies.md#_snippet_4

LANGUAGE: python
CODE:
```
import json
import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    RegexExtractionStrategy
)

async def extract_with_regex():
    # Create a strategy using built-in patterns for URLs and currencies
    strategy = RegexExtractionStrategy(
        pattern = RegexExtractionStrategy.Url | RegexExtractionStrategy.Currency
    )
    
    config = CrawlerRunConfig(extraction_strategy=strategy)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=config
        )
        
        if result.success:
            data = json.loads(result.extracted_content)
            for item in data[:5]:  # Show first 5 matches
                print(f"{item['label']}: {item['value']}")
            print(f"Total matches: {len(data)}")

asyncio.run(extract_with_regex())
```

----------------------------------------

TITLE: Pull Crawl4AI Docker Images
DESCRIPTION: Commands to pull the Crawl4AI Docker images from Docker Hub, including release candidates and the latest stable version, ensuring multi-architecture support.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_0

LANGUAGE: bash
CODE:
```
# Pull the release candidate (recommended for latest features)
docker pull unclecode/crawl4ai:0.6.0-r1

# Or pull the latest stable version
docker pull unclecode/crawl4ai:latest
```

----------------------------------------

TITLE: Combine Dynamic Interaction with CSS-based Data Extraction in Python
DESCRIPTION: This example shows how to integrate a JsonCssExtractionStrategy with CrawlerRunConfig to extract structured data after dynamic content has been loaded through multi-step interactions. It defines a schema for extracting commit titles from the loaded page.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/page-interaction.md#_snippet_11

LANGUAGE: Python
CODE:
```
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

schema = {
    "name": "Commits",
    "baseSelector": "li.Box-sc-g0xbh4-0",
    "fields": [
        {"name": "title", "selector": "h4.markdown-title", "type": "text"}
    ]
}
config = CrawlerRunConfig(
    session_id="ts_commits_session",
    js_code=js_next_page,
    wait_for=wait_for_more,
    extraction_strategy=JsonCssExtractionStrategy(schema)
)
```

----------------------------------------

TITLE: Crawl a Web URL with Crawl4AI in Python
DESCRIPTION: To crawl a live web page, provide the URL starting with `http://` or `https://`, using a `CrawlerRunConfig` object.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/local-files.md#_snippet_0

LANGUAGE: python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig

async def crawl_web():
    config = CrawlerRunConfig(bypass_cache=True)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://en.wikipedia.org/wiki/apple", 
            config=config
        )
        if result.success:
            print("Markdown Content:")
            print(result.markdown)
        else:
            print(f"Failed to crawl: {result.error_message}")

asyncio.run(crawl_web())
```

----------------------------------------

TITLE: Stop Crawl4AI Docker Compose Service
DESCRIPTION: Command to gracefully stop and remove the services defined in the `docker-compose.yml` file, effectively shutting down the Crawl4AI server and its associated containers.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_9

LANGUAGE: bash
CODE:
```
docker compose down
```

----------------------------------------

TITLE: Track Token Usage with LLMExtractionStrategy
DESCRIPTION: This example illustrates how to monitor token consumption when using `LLMExtractionStrategy`. The strategy records usage in `usages` and `total_usage` fields, and the `show_usage()` method provides a summary report. Users should note that usage data availability depends on the specific LLM provider.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/llm-strategies.md#_snippet_8

LANGUAGE: python
CODE:
```
llm_strategy = LLMExtractionStrategy(...)
# ...
llm_strategy.show_usage()
# e.g. “Total usage: 1241 tokens across 2 chunk calls”
```

----------------------------------------

TITLE: Clone Crawl4AI Repository
DESCRIPTION: Instructions to clone the Crawl4AI GitHub repository and navigate into its directory. This is the essential first step for both Docker Compose and manual setup methods.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_4

LANGUAGE: bash
CODE:
```
git clone https://github.com/unclecode/crawl4ai.git
cd crawl4ai
```

----------------------------------------

TITLE: AsyncWebCrawler.arun() Method API
DESCRIPTION: Documents the `arun` asynchronous method, which is the primary way to crawl a single URL. It outlines its parameters, including the `CrawlerRunConfig` for detailed crawl settings, and its `CrawlResult` return type. It also notes the acceptance of legacy parameters for backward compatibility.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/api/async-webcrawler.md#_snippet_4

LANGUAGE: APIDOC
CODE:
```
async def arun(
    self,
    url: str,
    config: Optional[CrawlerRunConfig] = None,
    # Legacy parameters for backward compatibility...
) -> CrawlResult:
    ...
```

----------------------------------------

TITLE: Quick Example: Asynchronous Web Crawling with AsyncWebCrawler
DESCRIPTION: A complete example demonstrating how to set up `BrowserConfig` and `CrawlerRunConfig` with a `JsonCssExtractionStrategy`, execute a crawl using `AsyncWebCrawler.arun()`, and process the returned `CrawlResult`.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/api/async-webcrawler.md#_snippet_8

LANGUAGE: Python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import json

async def main():
    # 1. Browser config
    browser_cfg = BrowserConfig(
        browser_type="firefox",
        headless=False,
        verbose=True
    )

    # 2. Run config
    schema = {
        "name": "Articles",
        "baseSelector": "article.post",
        "fields": [
            {
                "name": "title", 
                "selector": "h2", 
                "type": "text"
            },
            {
                "name": "url", 
                "selector": "a", 
                "type": "attribute", 
                "attribute": "href"
            }
        ]
    }

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema),
        word_count_threshold=15,
        remove_overlay_elements=True,
        wait_for="css:.post"  # Wait for posts to appear
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://example.com/blog",
            config=run_cfg
        )

        if result.success:
            print("Cleaned HTML length:", len(result.cleaned_html))
            if result.extracted_content:
                articles = json.loads(result.extracted_content)
                print("Extracted articles:", articles[:2])
        else:
            print("Error:", result.error_message)

asyncio.run(main())
```

----------------------------------------

TITLE: Check Crawl4AI API Health Status with cURL
DESCRIPTION: Provides a simple `curl` command to perform a quick health check on the Crawl4AI API's `/health` endpoint, verifying its operational status.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_30

LANGUAGE: bash
CODE:
```
curl http://localhost:11235/health
```

----------------------------------------

TITLE: Build Crawl4AI Docker Image Manually (Multi-Architecture)
DESCRIPTION: Explains how to use `docker buildx` to build the Crawl4AI image for the current or multiple architectures, loading it into Docker. It also shows how to pass build arguments for customization like install type and GPU support.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_10

LANGUAGE: bash
CODE:
```
docker buildx build -t crawl4ai-local:latest --load .

# Or build for multiple architectures (useful for publishing)
docker buildx build --platform linux/amd64,linux/arm64 -t crawl4ai-local:latest --load .

# Build with additional options
docker buildx build \
  --build-arg INSTALL_TYPE=all \
  --build-arg ENABLE_GPU=false \
  -t crawl4ai-local:latest --load .
```

----------------------------------------

TITLE: Crawl4AI Screenshot API Endpoint
DESCRIPTION: This endpoint captures a full-page PNG screenshot of a given URL. Users can specify an optional delay before capture and a path to save the output file. The request body is a JSON object containing the URL and optional parameters.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_18

LANGUAGE: APIDOC
CODE:
```
POST /screenshot
```

LANGUAGE: json
CODE:
```
{
  "url": "https://example.com",
  "screenshot_wait_for": 2,
  "output_path": "/path/to/save/screenshot.png"
}
```

----------------------------------------

TITLE: LlmConfig Parameters for LLM Configuration
DESCRIPTION: This API documentation outlines the key parameters for configuring Large Language Models within Crawl4AI using LlmConfig. It details how to specify the LLM provider, model name, API token (if required), and an optional base URL for custom endpoints, ensuring flexible and provider-agnostic LLM integration.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/llm-strategies.md#_snippet_1

LANGUAGE: APIDOC
CODE:
```
LlmConfig:
  provider: The <provider>/<model_name> identifier (e.g., "openai/gpt-4", "ollama/llama2", "huggingface/google-flan", etc.).
  api_token: If needed (for OpenAI, HuggingFace, etc.); local models or Ollama might not require it.
  base_url (optional): If your provider has a custom endpoint.
```

----------------------------------------

TITLE: Accessing Crawl Session ID in Python
DESCRIPTION: Demonstrates how to retrieve the `session_id` from the `CrawlResult` object, which is used for reusing a browser context across multiple crawl calls.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/api/crawl-result.md#_snippet_5

LANGUAGE: python
CODE:
```
# If you used session_id="login_session" in CrawlerRunConfig, see it here:
print("Session:", result.session_id)
```

----------------------------------------

TITLE: Perform Data Extraction from Raw HTML using a Pre-defined Schema
DESCRIPTION: This Python example illustrates how to use `crawl4ai`'s `AsyncWebCrawler` with a pre-defined `JsonCssExtractionStrategy` schema to extract structured data from raw HTML. It demonstrates setting up the crawler configuration, passing raw HTML as the URL, and parsing the extracted JSON content. This method is efficient for repetitive page structures and avoids AI costs during extraction.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/quickstart.md#_snippet_5

LANGUAGE: python
CODE:
```
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="raw://" + raw_html,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(schema)
            )
        )
        # The JSON output is stored in 'extracted_content'
        data = json.loads(result.extracted_content)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Crawl4AI Observability Configuration
DESCRIPTION: Default configuration for observability features including Prometheus metrics and health checks. This snippet shows the structure for enabling and defining endpoints for monitoring.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_32

LANGUAGE: yaml
CODE:
```
observability:
  prometheus:
    enabled: True
    endpoint: "/metrics"
  health_check:
    endpoint: "/health"
```

----------------------------------------

TITLE: Crawl4AI HTML Extraction API Endpoint
DESCRIPTION: This endpoint allows users to crawl a specified URL and retrieve preprocessed HTML, optimized for schema extraction. It accepts a JSON payload containing the target URL.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_17

LANGUAGE: APIDOC
CODE:
```
POST /html
```

LANGUAGE: json
CODE:
```
{
  "url": "https://example.com"
}
```

----------------------------------------

TITLE: Crawl4AI JavaScript Execution API Endpoint
DESCRIPTION: This endpoint executes a list of JavaScript snippets on a specified URL and returns the full crawl result. The snippets are executed sequentially, allowing for dynamic content extraction or interaction. The request body is a JSON object containing the URL and an array of JavaScript strings.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_20

LANGUAGE: APIDOC
CODE:
```
POST /execute_js
```

LANGUAGE: json
CODE:
```
{
  "url": "https://example.com",
  "scripts": [
    "return document.title",
    "return Array.from(document.querySelectorAll('a')).map(a => a.href)"
  ]
}
```

----------------------------------------

TITLE: Run Crawl4AI Docker Container with LLM Support
DESCRIPTION: Runs the Crawl4AI Docker container in detached mode, mapping port 11235, and providing LLM API keys via an environment file.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/deploy/docker/README.md#_snippet_15

LANGUAGE: bash
CODE:
```
# Make sure .llm.env is in the current directory (project root)
docker run -d \
  -p 11235:11235 \
  --name crawl4ai-standalone \
  --env-file .llm.env \
  --shm-size=1g \
  crawl4ai-local:latest
```

----------------------------------------

TITLE: Apply Topic-Based Text Segmentation with TextTiling in Python
DESCRIPTION: Uses algorithms like NLTK's TextTiling to create topic-coherent chunks. This class utilizes `nltk.tokenize.TextTilingTokenizer` to identify and segment text based on topic shifts.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/chunking.md#_snippet_2

LANGUAGE: python
CODE:
```
from nltk.tokenize import TextTilingTokenizer

class TopicSegmentationChunking:
    def __init__(self):
        self.tokenizer = TextTilingTokenizer()

    def chunk(self, text):
        return self.tokenizer.tokenize(text)

# Example Usage
text = """This is an introduction.
This is a detailed discussion on the topic."""
chunker = TopicSegmentationChunking()
print(chunker.chunk(text))
```

----------------------------------------

TITLE: Extracting Structured Data with XPath and raw:// HTML in Python
DESCRIPTION: This Python example showcases the `crawl4ai` library's capabilities for web scraping. It demonstrates how to use `JsonXPathExtractionStrategy` to define a JSON schema for data extraction using XPath selectors. The `raw://` scheme is utilized to pass a dummy HTML string directly to the crawler, bypassing network requests, which is useful for local testing or processing pre-fetched content. The entire extraction configuration is encapsulated within `CrawlerRunConfig`.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/no-llm-strategies.md#_snippet_1

LANGUAGE: Python
CODE:
```
import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy

async def extract_crypto_prices_xpath():
    # 1. Minimal dummy HTML with some repeating rows
    dummy_html = """
    <html>
      <body>
        <div class='crypto-row'>
          <h2 class='coin-name'>Bitcoin</h2>
          <span class='coin-price'>$28,000</span>
        </div>
        <div class='crypto-row'>
          <h2 class='coin-name'>Ethereum</h2>
          <span class='coin-price'>$1,800</span>
        </div>
      </body>
    </html>
    """

    # 2. Define the JSON schema (XPath version)
    schema = {
        "name": "Crypto Prices via XPath",
        "baseSelector": "//div[@class='crypto-row']",
        "fields": [
            {
                "name": "coin_name",
                "selector": ".//h2[@class='coin-name']",
                "type": "text"
            },
            {
                "name": "price",
                "selector": ".//span[@class='coin-price']",
                "type": "text"
            }
        ]
    }

    # 3. Place the strategy in the CrawlerRunConfig
    config = CrawlerRunConfig(
        extraction_strategy=JsonXPathExtractionStrategy(schema, verbose=True)
    )

    # 4. Use raw:// scheme to pass dummy_html directly
    raw_url = f"raw://{dummy_html}"

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=raw_url,
            config=config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return

        data = json.loads(result.extracted_content)
        print(f"Extracted {len(data)} coin rows")
        if data:
            print("First item:", data[0])

asyncio.run(extract_crypto_prices_xpath())
```

----------------------------------------

TITLE: Configuring HTML Source for Markdown Generation in crawl4ai
DESCRIPTION: This Python example demonstrates how to configure the `DefaultMarkdownGenerator` in `crawl4ai` to use different HTML content sources (`raw_html`, `cleaned_html`, `fit_html`) for Markdown generation. It shows how to integrate these generators into a `CrawlerRunConfig` and run an asynchronous web crawl to observe the effect of each source.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/markdown-generation.md#_snippet_2

LANGUAGE: Python
CODE:
```
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def main():
    # Option 1: Use the raw HTML directly from the webpage (before any processing)
    raw_md_generator = DefaultMarkdownGenerator(
        content_source="raw_html",
        options={"ignore_links": True}
    )
    
    # Option 2: Use the cleaned HTML (after scraping strategy processing - default)
    cleaned_md_generator = DefaultMarkdownGenerator(
        content_source="cleaned_html",  # This is the default
        options={"ignore_links": True}
    )
    
    # Option 3: Use preprocessed HTML optimized for schema extraction
    fit_md_generator = DefaultMarkdownGenerator(
        content_source="fit_html",
        options={"ignore_links": True}
    )
    
    # Use one of the generators in your crawler config
    config = CrawlerRunConfig(
        markdown_generator=raw_md_generator  # Try each of the generators
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com", config=config)
        if result.success:
            print("Markdown:\n", result.markdown.raw_markdown[:500])
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

LANGUAGE: APIDOC
CODE:
```
DefaultMarkdownGenerator `content_source` options:
- "cleaned_html" (default): Uses the HTML after it has been processed by the scraping strategy. This HTML is typically cleaner and more focused on content, with some boilerplate removed.
- "raw_html": Uses the original HTML directly from the webpage, before any cleaning or processing. This preserves more of the original content, but may include navigation bars, ads, footers, and other elements that might not be relevant to the main content.
- "fit_html": Uses HTML preprocessed for schema extraction. This HTML is optimized for structured data extraction and may have certain elements simplified or removed.
```

----------------------------------------

TITLE: Build Crawl4AI Docker Image with Build Arguments
DESCRIPTION: This example demonstrates how to build the Crawl4AI Docker image using `docker buildx build` with specific build arguments. It shows how to specify platforms and an `INSTALL_TYPE` to customize the feature set included in the image.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_21

LANGUAGE: bash
CODE:
```
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg INSTALL_TYPE=all \
  -t yourname/crawl4ai-all:latest \
  --load \
  . # Build from root context
```

----------------------------------------

TITLE: Crawl4ai REST API: Simple Non-Streaming Crawl with Python Requests
DESCRIPTION: Demonstrates how to initiate a basic non-streaming web crawl by making a direct HTTP POST request to the Crawl4ai `/crawl` endpoint. The example uses Python's `requests` library and shows how to construct the JSON payload for `BrowserConfig` and `CrawlerRunConfig`.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/deploy/docker/README.md#_snippet_33

LANGUAGE: python
CODE:
```
import requests

# Configuration objects converted to the required JSON structure
browser_config_payload = {
    "type": "BrowserConfig",
    "params": {"headless": True}
}
crawler_config_payload = {
    "type": "CrawlerRunConfig",
    "params": {"stream": False, "cache_mode": "bypass"} # Use string value of enum
}

crawl_payload = {
    "urls": ["https://httpbin.org/html"],
    "browser_config": browser_config_payload,
    "crawler_config": crawler_config_payload
}
response = requests.post(
    "http://localhost:11235/crawl", # Updated port
    # headers={"Authorization": f"Bearer {token}"},  # If JWT is enabled
    json=crawl_payload
)
print(f"Status Code: {response.status_code}")
if response.ok:
    print(response.json())
else:
    print(f"Error: {response.text}")
```

----------------------------------------

TITLE: Stream Crawl Results from Crawl4AI API with Python
DESCRIPTION: This Python asynchronous example demonstrates how to consume streaming results from the `/crawl/stream` endpoint using `httpx`. It shows how to send a payload with multiple URLs and browser/crawler configurations, and then process the NDJSON response line by line, checking for completion markers and handling potential JSON decoding errors.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/deploy/docker/README.md#_snippet_34

LANGUAGE: python
CODE:
```
import json
import httpx # Use httpx for async streaming example

async def test_stream_crawl(token: str = None):
    """Test the /crawl/stream endpoint with multiple URLs."""
    url = "http://localhost:11235/crawl/stream"
    payload = {
        "urls": [
            "https://httpbin.org/html",
            "https://httpbin.org/links/5/0"
        ],
        "browser_config": {
            "type": "BrowserConfig",
            "params": {"headless": True, "viewport": {"type": "dict", "value": {"width": 1200, "height": 800}}}
        },
        "crawler_config": {
            "type": "CrawlerRunConfig",
            "params": {"stream": True, "cache_mode": "bypass"}
        }
    }

    headers = {}
    # if token:
    #    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, json=payload, headers=headers, timeout=120.0) as response:
                print(f"Status: {response.status_code} (Expected: 200)")
                response.raise_for_status()

                # Read streaming response line-by-line (NDJSON)
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            # Check for completion marker
                            if data.get("status") == "completed":
                                print("Stream completed.")
                                break
                            print(f"Streamed Result: {json.dumps(data, indent=2)}")
                        except json.JSONDecodeError:
                            print(f"Warning: Could not decode JSON line: {line}")

    except httpx.HTTPStatusError as e:
         print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Error in streaming crawl test: {str(e)}")
```

----------------------------------------

TITLE: Implement Fixed-Length Word Chunking in Python
DESCRIPTION: Segments text into chunks of a fixed word count. This class takes a `chunk_size` and splits the input text into segments containing approximately that many words.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/chunking.md#_snippet_3

LANGUAGE: python
CODE:
```
class FixedLengthWordChunking:
    def __init__(self, chunk_size=100):
        self.chunk_size = chunk_size

    def chunk(self, text):
        words = text.split()
        return [' '.join(words[i:i + self.chunk_size]) for i in range(0, len(words), self.chunk_size)]

# Example Usage
text = "This is a long text with many words to be chunked into fixed sizes."
chunker = FixedLengthWordChunking(chunk_size=5)
print(chunker.chunk(text))
```

----------------------------------------

TITLE: Combining Built-in RegexExtractionStrategy Patterns
DESCRIPTION: This Python snippet demonstrates how to utilize and combine the various built-in patterns provided by `crawl4ai`'s `RegexExtractionStrategy`. It shows examples of using individual patterns, combining multiple patterns with bitwise OR, and selecting all available patterns for comprehensive data extraction.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/no-llm-strategies.md#_snippet_5

LANGUAGE: python
CODE:
```
# Use individual patterns
strategy = RegexExtractionStrategy(pattern=RegexExtractionStrategy.Email)

# Combine multiple patterns
strategy = RegexExtractionStrategy(
    pattern = (
        RegexExtractionStrategy.Email |
        RegexExtractionStrategy.PhoneUS |
        RegexExtractionStrategy.Url
    )
)

# Use all available patterns
strategy = RegexExtractionStrategy(pattern=RegexExtractionStrategy.All)
```

----------------------------------------

TITLE: Extract Structured Data using LLM (Python)
DESCRIPTION: This Python example demonstrates how to use Crawl4AI's LLMExtractionStrategy to parse web content into a predefined Pydantic schema. It configures an LLM provider (e.g., OpenAI, Ollama) and specifies extraction instructions to intelligently extract structured data like model names and their associated fees from a webpage.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/quickstart.md#_snippet_6

LANGUAGE: python
CODE:
```
import os
import json
import asyncio
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, BrowserConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from typing import Dict

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(
        ..., description="Fee for output token for the OpenAI model."
    )

async def extract_structured_data_using_llm(
    provider: str, api_token: str = None, extra_headers: Dict[str, str] = None
):
    print(f"\n--- Extracting Structured Data with {provider} ---")

    if api_token is None and provider != "ollama":
        print(f"API token is required for {provider}. Skipping this example.")
        return

    browser_config = BrowserConfig(headless=True)

    extra_args = {"temperature": 0, "top_p": 0.9, "max_tokens": 2000}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLMExtractionStrategy(
            llm_config = LLMConfig(provider=provider,api_token=api_token),
            schema=OpenAIModelFee.model_json_schema(),
            extraction_type="schema",
            instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content.""",
            extra_args=extra_args,
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/", config=crawler_config
        )
        print(result.extracted_content)

if __name__ == "__main__":

    asyncio.run(
        extract_structured_data_using_llm(
            provider="openai/gpt-4o", api_token=os.getenv("OPENAI_API_KEY")
        )
    )
```

----------------------------------------

TITLE: Crawl4AI Dockerfile Build Arguments Reference
DESCRIPTION: This section provides a reference for the available build arguments that can be used to customize the Crawl4AI Docker image. It details each argument's purpose, default value, and possible options, allowing users to tailor the image to their specific needs.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/core/docker-deployment.md#_snippet_22

LANGUAGE: APIDOC
CODE:
```
INSTALL_TYPE: Feature set
  Default: `default`
  Options: `default`, `all`, `torch`, `transformer`
ENABLE_GPU: GPU support (CUDA for AMD64)
  Default: `false`
  Options: `true`, `false`
APP_HOME: Install path inside container (advanced)
  Default: `/app`
  Options: any valid path
USE_LOCAL: Install library from local source
  Default: `true`
  Options: `true`, `false`
GITHUB_REPO: Git repo to clone if USE_LOCAL=false
  Default: *(see Dockerfile)*
  Options: any git URL
GITHUB_BRANCH: Git branch to clone if USE_LOCAL=false
  Default: `main`
  Options: any branch name
```

----------------------------------------

TITLE: Configure Proxy for Web Crawling with Crawl4AI (Python)
DESCRIPTION: This snippet demonstrates how to configure proxy settings for web crawling using Crawl4AI's `BrowserConfig.proxy_config`. It shows how to specify a proxy server, username, and password, and then uses the configured crawler to fetch a page, verifying the proxy usage. The `proxy_config` expects a dictionary with `server` and optional authentication credentials.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/advanced/advanced-features.md#_snippet_0

LANGUAGE: Python
CODE:
```
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def main():
    browser_cfg = BrowserConfig(
        proxy_config={
            "server": "http://proxy.example.com:8080",
            "username": "myuser",
            "password": "mypass"
        },
        headless=True
    )
    crawler_cfg = CrawlerRunConfig(
        verbose=True
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://www.whatismyip.com/",
            config=crawler_cfg
        )
        if result.success:
            print("[OK] Page fetched via proxy.")
            print("Page HTML snippet:", result.html[:200])
        else:
            print("[ERROR]", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
```

----------------------------------------

TITLE: Perform Sliding Window Text Chunking in Python
DESCRIPTION: Generates overlapping chunks for better contextual coherence. This class allows defining a `window_size` and `step` to create overlapping segments of text, useful for maintaining context.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/chunking.md#_snippet_4

LANGUAGE: python
CODE:
```
class SlidingWindowChunking:
    def __init__(self, window_size=100, step=50):
        self.window_size = window_size
        self.step = step

    def chunk(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words) - self.window_size + 1, self.step):
            chunks.append(' '.join(words[i:i + self.window_size]))
        return chunks

# Example Usage
text = "This is a long text to demonstrate sliding window chunking."
chunker = SlidingWindowChunking(window_size=5, step=2)
print(chunker.chunk(text))
```

----------------------------------------

TITLE: Delete a Browser Profile
DESCRIPTION: After running this command, choose option '3' in the TUI, pick the profile index, and confirm to remove the profile folder.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/codebase/cli.md#_snippet_13

LANGUAGE: Shell
CODE:
```
crwl profiles
```

----------------------------------------

TITLE: Define and Use Custom Regex Patterns with Crawl4AI
DESCRIPTION: This Python example demonstrates how to use `crawl4ai`'s `RegexExtractionStrategy` to define and apply a custom regular expression for extracting specific data, such as US Dollar prices. It shows configuring the crawler with the custom pattern and processing the extracted JSON results, highlighting a direct, pattern-based extraction method.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/md_v2/extraction/no-llm-strategies.md#_snippet_7

LANGUAGE: python
CODE:
```
import json
import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    RegexExtractionStrategy
)

async def extract_prices():
    # Define a custom pattern for US Dollar prices
    price_pattern = {"usd_price": r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"}
    
    # Create strategy with custom pattern
    strategy = RegexExtractionStrategy(custom=price_pattern)
    config = CrawlerRunConfig(extraction_strategy=strategy)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.example.com/products",
            config=config
        )
        
        if result.success:
            data = json.loads(result.extracted_content)
            for item in data:
                print(f"Found price: {item['value']}")

asyncio.run(extract_prices())
```

----------------------------------------

TITLE: Test Crawl4AI MCP WebSocket Connection
DESCRIPTION: Executes a Python script from the repository root to test the Model Context Protocol (MCP) WebSocket connection.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/deploy/docker/README.md#_snippet_21

LANGUAGE: bash
CODE:
```
# From the repository root
python tests/mcp/test_mcp_socket.py
```

----------------------------------------

TITLE: One-off Crawl with Explicit Profile Path
DESCRIPTION: Performs a crawl by directly specifying the profile folder path, bypassing the named profile registry. This is useful for CI scripts.
SOURCE: https://github.com/unclecode/crawl4ai/blob/main/docs/codebase/cli.md#_snippet_19

LANGUAGE: Shell
CODE:
```
crwl https://site.com -b "user_data_dir=$HOME/.crawl4ai/profiles/my-profile,use_managed_browser=true"
```