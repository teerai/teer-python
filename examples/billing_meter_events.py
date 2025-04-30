"""
Billing Meter Events Example for the Teer Python SDK.

This example demonstrates how to use the billing resource to create meter events
for usage-based billing with Stripe.
"""

from teer import TeerClient
from datetime import datetime, UTC

# Initialize the client with your API key
client = TeerClient("YOUR_API_KEY")

# Get the current timestamp in ISO 8601 format using timezone-aware approach
current_timestamp = datetime.now(UTC).isoformat()

try:
    # Create a meter event
    meter_event = client.billing.meter_events.create(
        {
            "provider": "stripe",
            "fields": {
                "identifier": "idmp_12345678",
                "event_name": "ai_search_api",
                "timestamp": current_timestamp,
                "payload": {
                    "stripe_customer_id": "cus_12345678",
                    "value": "25",
                },
            },
        }
    )

    print("Meter event created:")
    print(f"  ID: {meter_event['id']}")
    print(f"  Event Name: {meter_event['event_name']}")
    print(f"  Timestamp: {meter_event['timestamp']}")
    print(f"  Created At: {meter_event['created_at']}")

except Exception as e:
    print(f"Error creating meter event: {e}")
