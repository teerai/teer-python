# Teer Usage Reports

This document provides detailed information about the structure and fields of usage reports that can be sent to Teer using the Python SDK.

## Usage Report Schema

A usage report is a JSON object that contains information about LLM usage. The following table describes the fields that can be included in a usage report:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provider` | string | Yes | The LLM provider. Must be one of: `"anthropic"`, `"openai"`, or `"google"`. |
| `model` | string | Yes | The model name (e.g., `"claude-3-haiku-20240307"`, `"gpt-4o-mini-2024-07-18"`, `"gemini-2.0-flash-001"`). |
| `function_id` | string | No | A unique identifier for the function or endpoint using the LLM. |
| `usage` | object | Yes | Token usage information. See [Usage Object](#usage-object) for details. |
| `trace_id` | string | No | A unique identifier for the trace. Used for distributed tracing. |
| `span_id` | string | No | A unique identifier for the span within the trace. |
| `parent_span_id` | string | No | The ID of the parent span, if applicable. |
| `batch` | boolean | No | Whether this was part of a batch operation. This has an impact on pricing. |
| `platform` | object | No | Teer-specific platform information. See [Platform Object](#platform-object) for details. |
| `billing` | object | No | Billing information. See [Billing Object](#billing-object) for details. |
| `metadata` | object | No | Additional metadata for attribution and analytics. See [Metadata Object](#metadata-object) for details. |

### Usage Object

The `usage` object contains information about token usage:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | number | Yes | The number of input tokens. |
| `output` | number | Yes | The number of output tokens. |
| `cache` | object | No | Cache-related token information. See [Cache Object](#cache-object) for details. |

### Cache Object

The `cache` object contains provider-specific cache information:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `anthropic` | object | No | Anthropic-specific cache information. |
| `openai` | object | No | OpenAI-specific cache information. |
| `google` | object | No | Google-specific cache information. |

#### Anthropic Cache Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cache_creation_input_tokens` | number | No | The number of tokens used to create the cache. |
| `cache_read_input_tokens` | number | No | The number of tokens read from the cache. |

#### OpenAI Cache Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input_cached_tokens` | number | No | The number of input tokens retrieved from cache. |

#### Google Cache Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cached_content_token_count` | number | No | The number of tokens retrieved from cache. |

### Platform Object

The `platform` object contains Teer-specific platform information:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rate_card_id` | string | Yes | The ID of the rate card to use for billing. |

### Billing Object

The `billing` object contains billing information:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provider` | string | Yes | The billing provider. Currently only `"stripe"` is supported. |
| `fields` | object | Yes | Billing provider-specific fields. |

#### Billing Fields Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer` | string | Yes | The customer ID in the billing system. |

### Metadata Object

The `metadata` object can contain any key-value pairs for attribution and analytics. Here are some common fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | No | The ID of the user who made the request. |
| `organization_id` | string | No | The ID of the organization the user belongs to. |
| `member_id` | string | No | The ID of the member within the organization. |
| `team_id` | string | No | The ID of the team the user belongs to. |
| `session_id` | string | No | The ID of the user's session. |
| `request_id` | string | No | A unique identifier for the request. |
| `project_id` | string | No | The project or initiative the request is associated with. |

## Examples

### Basic Usage Report

```python
client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "function_id": "summarize-article",  # Optional but recommended for association to a specific feature / fn call
    "usage": {
        "input": 1000,
        "output": 2000
    }
})
```

### Usage Report Without Function ID

```python
client.ingest.send({
    "provider": "openai",
    "model": "gpt-4o-mini-2024-07-18",
    # function_id is optional and can be omitted
    "usage": {
        "input": 500,
        "output": 1500
    }
})
```

### Usage Report with Cache Information

```python
client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "function_id": "legal-document-analysis",
    "usage": {
        "input": 2000,
        "output": 3000,
        "cache": {
            "anthropic": {
                "cache_creation_input_tokens": 1500,
                "cache_read_input_tokens": 500
            }
        }
    }
})
```

### Usage Report with User Attribution

```python
client.ingest.send({
    "provider": "openai",
    "model": "gpt-4o-mini-2024-07-18",
    "function_id": "generate-content",
    "usage": {
        "input": 500,
        "output": 1500
    },
    "metadata": {
        "user_id": "user-123456",
        "organization_id": "org-abcdef",
        "session_id": "session-xyz789"
    }
})
```

### Complete Usage Report

```python
client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "function_id": "enterprise-analysis",
    "usage": {
        "input": 5000,
        "output": 8000,
        "cache": {
            "anthropic": {
                "cache_creation_input_tokens": 3000,
                "cache_read_input_tokens": 2000
            }
        }
    },
    "platform": {
        "rate_card_id": "rate-card-enterprise"
    },
    "billing": {
        "provider": "stripe",
        "fields": {
            "customer": "cus_enterprise_abc"
        }
    },
    "metadata": {
        "user_id": "user-admin-456",
        "organization_id": "org-enterprise-789",
        "session_id": "session-long-running-xyz"
    },
    "trace_id": "trace-complete-example",
    "span_id": "span-main-operation"
})
```

For more examples, see the [comprehensive_usage_reports.py](../examples/comprehensive_usage_reports.py) file in the examples directory.
