"""
Comprehensive Usage Reports Example for the Teer Python SDK.

This example demonstrates various usage report scenarios for different LLM providers,
including provider-specific cache token information and metadata attribution.
"""

from teer import TeerClient

# Initialize the client with your API key
client = TeerClient("YOUR_API_KEY")

# -------------------------------------------------------------------------
# Basic Usage Report Examples
# -------------------------------------------------------------------------

print("Basic Usage Report Examples")
print("--------------------------")

# Example 1: Basic Anthropic usage report
print("\nExample 1: Basic Anthropic usage report")
response = client.ingest.send(
    {
        # Required: Specify the LLM provider
        "provider": "anthropic",
        # Required: Specify the model name
        "model": "claude-3-haiku-20240307",
        # Required: A unique identifier for the function or endpoint using the LLM
        "function_id": "summarize-article",
        # Required: Token usage information
        "usage": {
            # Number of input tokens
            "input": 1000,
            # Number of output tokens
            "output": 2000,
        },
        # Optional: Trace information for distributed tracing
        "trace_id": "trace-123456",
        "span_id": "span-abcdef",
    }
)

# Example 2: Basic OpenAI usage report
print("\nExample 2: Basic OpenAI usage report")
response = client.ingest.send(
    {
        "provider": "openai",
        "model": "gpt-4-turbo",
        "function_id": "generate-content",
        "usage": {"input": 500, "output": 1500},
        "trace_id": "trace-789012",
        "span_id": "span-ghijkl",
    }
)

# Example 3: Basic Google usage report
print("\nExample 3: Basic Google usage report")
response = client.ingest.send(
    {
        "provider": "google",
        "model": "gemini-pro",
        "function_id": "answer-question",
        "usage": {"input": 300, "output": 900},
        "trace_id": "trace-345678",
        "span_id": "span-mnopqr",
    }
)

# Example 3.1: Usage report without function_id
print("\nExample 3.1: Usage report without function_id")
response = client.ingest.send(
    {
        # Required: Specify the LLM provider
        "provider": "google",
        # Required: Specify the model name
        "model": "gemini-pro",
        # function_id is optional and can be omitted
        # Required: Token usage information
        "usage": {"input": 400, "output": 1200},
        # Optional: Trace information
        "trace_id": "trace-no-function-id",
        "span_id": "span-no-function-id",
    }
)

# -------------------------------------------------------------------------
# Advanced Usage Reports with Provider-Specific Cache Information
# -------------------------------------------------------------------------

print("\n\nAdvanced Usage Reports with Provider-Specific Cache Information")
print("--------------------------------------------------------------")

# Example 4: Anthropic usage report with cache information
print("\nExample 4: Anthropic usage report with cache information")
response = client.ingest.send(
    {
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "function_id": "legal-document-analysis",
        "usage": {
            "input": 2000,
            "output": 3000,
            # Anthropic-specific cache information
            "cache": {
                "anthropic": {
                    # Tokens used to create the cache
                    "cache_creation_input_tokens": 1500,
                    # Tokens read from the cache
                    "cache_read_input_tokens": 500,
                }
            },
        },
        "trace_id": "trace-abcdef",
        "span_id": "span-123456",
        # Whether this was part of a batch operation (affects pricing)
        "batch": True,
    }
)

# Example 5: OpenAI usage report with cache information
print("\nExample 5: OpenAI usage report with cache information")
response = client.ingest.send(
    {
        "provider": "openai",
        "model": "gpt-4o",
        "function_id": "code-generation",
        "usage": {
            "input": 800,
            "output": 2500,
            # OpenAI-specific cache information
            "cache": {
                "openai": {
                    # Tokens retrieved from cache
                    "input_cached_tokens": 300
                }
            },
        },
        "trace_id": "trace-ghijkl",
        "span_id": "span-789012",
        "batch": False,
    }
)

# Example 6: Google usage report with cache information
print("\nExample 6: Google usage report with cache information")
response = client.ingest.send(
    {
        "provider": "google",
        "model": "gemini-ultra",
        "function_id": "image-analysis",
        "usage": {
            "input": 1200,
            "output": 1800,
            # Google-specific cache information
            "cache": {
                "google": {
                    # Tokens retrieved from cache
                    "cached_content_token_count": 800,
                    # Tokens used for thoughts
                    "thoughts_token_count": 400,
                }
            },
        },
        "trace_id": "trace-mnopqr",
        "span_id": "span-345678",
        "batch": False,
    }
)

# -------------------------------------------------------------------------
# Usage Reports with Metadata for User Attribution
# -------------------------------------------------------------------------

print("\n\nUsage Reports with Metadata for User Attribution")
print("-----------------------------------------------")

# Example 7: Usage report with user attribution metadata
print("\nExample 7: Usage report with user attribution metadata")
response = client.ingest.send(
    {
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
        "function_id": "customer-support",
        "usage": {"input": 600, "output": 1200},
        # Metadata for user attribution and analytics
        "metadata": {
            # User identification
            "user_id": "user-123456",
            "organization_id": "org-abcdef",
            # Session information
            "session_id": "session-xyz789",
            # Request context
            "request_source": "web-app",
            "feature": "chat-assistant",
            # Business context
            "department": "customer-support",
            "priority": "high",
            # Custom dimensions
            "language": "en-US",
            "region": "us-west",
        },
        "trace_id": "trace-stuvwx",
        "span_id": "span-901234",
    }
)

# -------------------------------------------------------------------------
# Usage Reports with Billing Information
# -------------------------------------------------------------------------

print("\n\nUsage Reports with Billing Information")
print("------------------------------------")

# Example 8: Usage report with billing information (single meter)
print("\nExample 8: Usage report with billing information (single meter)")
response = client.ingest.send(
    {
        "provider": "openai",
        "model": "gpt-4-turbo",
        "function_id": "data-analysis",
        "usage": {"input": 1500, "output": 3500},
        # Teer-specific platform information
        "platform": {
            # ID of the rate card to use for billing
            "rate_card_id": "rate-card-premium"
        },
        # Billing information
        "billing": {
            # Billing provider (defaults to 'stripe')
            "provider": "stripe",
            "fields": {
                # Customer ID in the billing system
                "customer": "cus_1234567890",
                # Optional customer email
                "email": "customer@example.com",
                # Single meter ID
                "meter": "meter_premium_abc",
            },
        },
        "metadata": {"project_id": "proj-987654", "cost_center": "cc-finance-01"},
        "trace_id": "trace-yzabcd",
        "span_id": "span-567890",
    }
)

# Example 8.1: Usage report with billing information (multiple meters)
print("\nExample 8.1: Usage report with billing information (multiple meters)")
response = client.ingest.send(
    {
        "provider": "openai",
        "model": "gpt-4-turbo",
        "function_id": "data-analysis",
        "usage": {"input": 1500, "output": 3500},
        # Teer-specific platform information
        "platform": {
            # ID of the rate card to use for billing
            "rate_card_id": "rate-card-premium"
        },
        # Billing information
        "billing": {
            # Billing provider (defaults to 'stripe')
            "provider": "stripe",
            "fields": {
                # Customer ID in the billing system
                "customer": "cus_1234567890",
                # Optional customer email
                "email": "customer@example.com",
                # Multiple meters with different IDs
                "meters": {
                    "input": "input_meter_id",
                    "outout": "meter_viz_xyz",
                },
            },
        },
        "metadata": {"project_id": "proj-987654", "cost_center": "cc-finance-01"},
        "trace_id": "trace-yzabcd",
        "span_id": "span-567890",
    }
)

# -------------------------------------------------------------------------
# Complete Usage Report Example
# -------------------------------------------------------------------------

print("\n\nComplete Usage Report Example")
print("--------------------------")

# Example 9: Complete usage report with all fields
print("\nExample 9: Complete usage report with all fields")
response = client.ingest.send(
    {
        # Provider information
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "function_id": "enterprise-analysis",
        # Usage information
        "usage": {
            "input": 5000,
            "output": 8000,
            "cache": {
                "anthropic": {
                    "cache_creation_input_tokens": 3000,
                    "cache_read_input_tokens": 2000,
                }
            },
        },
        # Platform information
        "platform": {"rate_card_id": "rate-card-enterprise"},
        # Billing information
        "billing": {
            "provider": "stripe",
            "fields": {
                "customer": "cus_enterprise_abc",
                "email": "enterprise@example.com",
                "meters": {
                    "input": "input_meter_id",
                    "output": "output_meter_id",
                    "cache_creation_input_tokens": "cache_creation_input_meter_id",
                    "cache_read_input_tokens": "cache_read_input_meter_id",
                },
            },
        },
        # Metadata for attribution and analytics
        "metadata": {
            # User information
            "user_id": "user-admin-456",
            "organization_id": "org-enterprise-789",
            "member_id": "member-123",
            "team_id": "team-finance",
            # Session information
            "session_id": "session-long-running-xyz",
            # Request context
            "request_id": "req-abcdef123456",
            "source_ip": "10.0.0.1",
            "user_agent": "Mozilla/5.0...",
            # Business context
            "project": "quarterly-financial-analysis",
            "department": "finance",
            "cost_center": "cc-finance-hq",
            # Performance metrics
            "latency_ms": 1250,
            "request_time": "2023-04-16T10:30:15Z",
        },
        # Tracing information
        "trace_id": "trace-complete-example",
        "span_id": "span-main-operation",
        "parent_span_id": "span-parent-operation",
        # Batch information
        "batch": True,
    }
)

print(
    "\nAll examples completed. Check your Teer dashboard to see the reported usage data."
)
