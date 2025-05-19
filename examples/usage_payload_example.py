"""
Example of creating a usage payload for the Teer ingest API.

This example demonstrates how to create a payload for the Teer ingest API
from an LLM provider response or from explicit token counts.
"""

from typing import Dict, Any, Optional
from teer.types import (
    IngestPayload,
    UsageObject,
    CacheObject,
    AnthropicCache,
    OpenAICache,
    GoogleCache,
)


def create_usage_payload(
    provider: str,
    model: str,
    function_id: str,
    response: Optional[Any] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    cache_data: Optional[Dict[str, Dict[str, int]]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> IngestPayload:
    """
    Create a payload for the Teer ingest API.

    This function can be used in several ways:
    1. Pass a response object from an LLM provider (e.g., Anthropic) and it will extract the usage information
    2. Directly provide input_tokens and output_tokens if you already have them
    3. Provide cache_data to include provider-specific cache information

    Args:
        provider: The LLM provider (e.g., "anthropic", "openai", "google").
        model: The model name (e.g., "claude-3-haiku-20240307").
        function_id: An identifier for the function or endpoint using the LLM.
        response: Optional response object from the LLM provider (e.g., Anthropic message).
        input_tokens: Optional number of input tokens used (if not providing response).
        output_tokens: Optional number of output tokens generated (if not providing response).
        cache_data: Optional cache information by provider.
        metadata: Optional additional metadata.

    Returns:
        A dictionary payload ready to be sent to the Teer ingest API.
    """
    # Initialize usage information
    usage_data: Dict[str, Any] = {}
    cache_info: Optional[Dict[str, Dict[str, int]]] = None

    # Extract usage information from response if provided
    if response is not None:
        if provider == "anthropic":
            # Extract usage information from Anthropic response
            if hasattr(response, "usage"):
                # Extract standard token counts
                usage_data["input"] = getattr(response.usage, "input_tokens", 0)
                usage_data["output"] = getattr(response.usage, "output_tokens", 0)

                # Extract cache-related token information
                cache_read = getattr(response.usage, "cache_read_input_tokens", 0)
                cache_creation = getattr(
                    response.usage, "cache_creation_input_tokens", 0
                )

                # Create cache info if cache tokens are present
                if cache_read > 0 or cache_creation > 0:
                    cache_info = {
                        "anthropic": {
                            "cache_read_input_tokens": cache_read,
                            "cache_creation_input_tokens": cache_creation,
                        }
                    }
            else:
                print(f"No usage information found in {provider} response")
        elif provider == "openai":
            # Extract usage information from OpenAI response
            if hasattr(response, "usage"):
                # Extract standard token counts
                usage_data["input"] = getattr(response.usage, "prompt_tokens", 0)
                usage_data["output"] = getattr(response.usage, "completion_tokens", 0)

                # Extract cache-related token information
                input_cached = getattr(response.usage, "input_cached_tokens", 0)

                # Create cache info if cache tokens are present
                if input_cached > 0:
                    cache_info = {
                        "openai": {
                            "input_cached_tokens": input_cached,
                        }
                    }
            else:
                print(f"No usage information found in {provider} response")
        elif provider == "google":
            # Extract usage information from Google response
            if hasattr(response, "usage_metadata"):
                # Extract standard token counts
                usage_data["input"] = getattr(
                    response.usage_metadata, "prompt_token_count", 0
                )
                usage_data["output"] = getattr(
                    response.usage_metadata, "candidates_token_count", 0
                )

                # Extract cache-related token information
                cached_content = getattr(
                    response.usage_metadata, "cached_content_token_count", 0
                )
                thoughts = getattr(response.usage_metadata, "thoughts_token_count", 0)

                # Create cache info if cache tokens are present
                if cached_content > 0 or thoughts > 0:
                    cache_info = {"google": {}}
                    if cached_content > 0:
                        cache_info["google"][
                            "cached_content_token_count"
                        ] = cached_content
                    if thoughts > 0:
                        cache_info["google"]["thoughts_token_count"] = thoughts
            else:
                print(f"No usage information found in {provider} response")
        else:
            # For other providers, implement their specific extraction logic here
            print(f"Usage extraction not implemented for provider: {provider}")
    else:
        # Use provided token counts if response is not available
        if input_tokens is not None and output_tokens is not None:
            usage_data["input"] = input_tokens
            usage_data["output"] = output_tokens

            # Use provided cache data if available
            if cache_data:
                cache_info = cache_data
        else:
            raise ValueError(
                "Either response or input_tokens and output_tokens must be provided"
            )

    # Create the payload
    payload = {
        "provider": provider,
        "model": model,
        "function_id": function_id,
        "usage": usage_data,
    }

    # Add cache information if available
    if cache_info:
        payload["usage"]["cache"] = cache_info

    # Add metadata if provided
    if metadata:
        payload["metadata"] = metadata

    return payload


# Example 1: Creating a payload with explicit token counts
payload1 = create_usage_payload(
    provider="anthropic",
    model="claude-3-haiku-20240307",
    function_id="my-function",
    input_tokens=1000,
    output_tokens=2000,
    metadata={"user_id": "user123", "session_id": "session456"},
)

print("Example 1: Creating a payload with explicit token counts")
print(f"Payload: {payload1}")
print()


# Example 2: Creating a payload from an Anthropic response (simulated)
class MockAnthropicUsage:
    def __init__(self):
        self.input_tokens = 1500
        self.output_tokens = 2500
        self.cache_read_input_tokens = 500
        self.cache_creation_input_tokens = 1000


class MockAnthropicResponse:
    def __init__(self):
        self.usage = MockAnthropicUsage()


# Create a mock Anthropic response
anthropic_response = MockAnthropicResponse()

payload2 = create_usage_payload(
    provider="anthropic",
    model="claude-3-haiku-20240307",
    function_id="my-function",
    response=anthropic_response,
)

print("Example 2: Creating a payload from an Anthropic response")
print(f"Payload: {payload2}")
print()


# Example 3: Creating a payload with OpenAI cache information
class MockOpenAIUsage:
    def __init__(self):
        self.prompt_tokens = 800
        self.completion_tokens = 1200
        self.input_cached_tokens = 300


class MockOpenAIResponse:
    def __init__(self):
        self.usage = MockOpenAIUsage()


# Create a mock OpenAI response
openai_response = MockOpenAIResponse()

payload3 = create_usage_payload(
    provider="openai",
    model="gpt-4o",
    function_id="code-generation",
    response=openai_response,
)

print("Example 3: Creating a payload from an OpenAI response")
print(f"Payload: {payload3}")
print()


# Example 4: Creating a payload with Google cache information
class MockGoogleUsageMetadata:
    def __init__(self):
        self.prompt_token_count = 1200
        self.candidates_token_count = 1800
        self.cached_content_token_count = 800
        self.thoughts_token_count = 400


class MockGoogleResponse:
    def __init__(self):
        self.usage_metadata = MockGoogleUsageMetadata()


# Create a mock Google response
google_response = MockGoogleResponse()

payload4 = create_usage_payload(
    provider="google",
    model="gemini-ultra",
    function_id="image-analysis",
    response=google_response,
)

print("Example 4: Creating a payload from a Google response")
print(f"Payload: {payload4}")
print()

# Example 5: Creating a payload with explicit cache data
payload5 = create_usage_payload(
    provider="openai",
    model="gpt-4o",
    function_id="custom-function",
    input_tokens=1000,
    output_tokens=1500,
    cache_data={"openai": {"input_cached_tokens": 250}},
    metadata={"user_id": "user456", "session_id": "session789"},
)

print("Example 5: Creating a payload with explicit cache data")
print(f"Payload: {payload5}")
