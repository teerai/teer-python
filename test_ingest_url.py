"""
Test script to verify that the ingest endpoint uses the correct base URL.
"""

import os
import logging
from teer import TeerClient

# Set up logging to see the URLs being used
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("teer")
logger.setLevel(logging.DEBUG)

# Initialize the client with a test API key
api_key = os.environ.get("TEER_SECRET_API_KEY", "test_api_key")
client = TeerClient(api_key=api_key)

# Print the client details
print(f"Client initialized with API key: {api_key}")
print(f"Base URL: {client.base_url}")
print(f"API base: {client.api_base}")
print(f"Track base: {client.track_base}")

# Print the ingest resource base URL
print(f"Ingest resource base URL: {client.ingest.base_url}")

# Try to send a test ingest request
# This will fail with an invalid API key, but we can see the URL in the logs
try:
    response = client.ingest.send({
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "function_id": "test-function",
        "usage": {
            "input": 100,
            "output": 200
        }
    })
    print(f"Response: {response}")
except Exception as e:
    print(f"Error sending ingest request (expected with test API key): {e}")

print("Test completed!")
