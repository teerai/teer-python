"""
Custom Base URL Example for the Teer Python SDK.

This example demonstrates how to initialize the Teer client with a custom base URL and API key.
This is useful for:
- Development and testing environments
- Self-hosted Teer instances
- Enterprise deployments with custom endpoints
"""

import os
from teer import TeerClient

# Example 1: Initialize with explicit API key and custom base URL
print("Example 1: Initialize with explicit API key and custom base URL")
client1 = TeerClient(
    api_key="YOUR_API_KEY",
    base_url="https://dev-track.teer.ai",  # Development environment
)

print(f"Client 1 Base URL: {client1.base_url}")
print(f"Client 1 API Base: {client1.api_base}")
print()

# Example 2: Initialize with environment variable for API key and custom base URL
print("Example 2: Initialize with environment variable for API key and custom base URL")
# Set environment variable (in a real scenario, this would be set outside the script)
os.environ["TEER_SECRET_API_KEY"] = "ENV_VARIABLE_API_KEY"

client2 = TeerClient(
    # API key will be read from TEER_SECRET_API_KEY environment variable
    base_url="https://staging-track.teer.ai"  # Staging environment
)

print(f"Client 2 Base URL: {client2.base_url}")
print(f"Client 2 API Base: {client2.api_base}")
print()

# Example 3: Initialize with custom API version
print("Example 3: Initialize with custom API version")
client3 = TeerClient(
    api_key="YOUR_API_KEY",
    base_url="https://enterprise.example.com/teer",  # Enterprise self-hosted instance
    api_version="v2",  # Using a different API version
)

print(f"Client 3 Base URL: {client3.base_url}")
print(f"Client 3 API Base: {client3.api_base}")
print()

# Example 4: Send usage data with custom base URL
print("Example 4: Send usage data with custom base URL")
# Note: This will only work if the custom base URL is valid and accessible
# For demonstration purposes, we'll use a try-except block
try:
    # Initialize with a mock API key and local development server
    local_client = TeerClient(api_key="test_api_key", base_url="http://localhost:5000")

    # Send usage data
    response = local_client.ingest.send(
        {
            "provider": "anthropic",
            "model": "claude-3-haiku-20240307",
            "function_id": "my-function",
            "usage": {"input": 1000, "output": 2000},
        }
    )

    print(f"Response: {response}")
except Exception as e:
    print(f"Error sending data to local server: {e}")
    print("Note: This is expected if you don't have a local server running.")
