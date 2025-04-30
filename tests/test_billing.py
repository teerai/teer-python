"""
Tests for the billing resource.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC

from teer import TeerClient


class TestBillingResource(unittest.TestCase):
    """Test cases for the billing resource."""

    def setUp(self):
        """Set up the test environment."""
        self.client = TeerClient(api_key="test_api_key")
        self.timestamp = datetime.now(UTC).isoformat()

    @patch("teer.resources.base.BaseResource._request")
    def test_create_meter_event(self, mock_request):
        """Test creating a meter event."""
        # Set up the mock response
        mock_response = {
            "id": "meter_event_123",
            "event_name": "ai_search_api",
            "timestamp": self.timestamp,
            "payload": {"stripe_customer_id": "cus_12345678", "value": "25"},
            "identifier": "idmp_12345678",
            "created_at": self.timestamp,
            "updated_at": self.timestamp,
        }
        mock_request.return_value = mock_response

        # Create a meter event
        meter_event = self.client.billing.meter_events.create(
            {
                "provider": "stripe",
                "fields": {
                    "identifier": "idmp_12345678",
                    "event_name": "ai_search_api",
                    "timestamp": self.timestamp,
                    "payload": {
                        "stripe_customer_id": "cus_12345678",
                        "value": "25",
                    },
                },
            }
        )

        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(kwargs["data"]["provider"], "stripe")
        self.assertEqual(kwargs["data"]["fields"]["event_name"], "ai_search_api")
        self.assertEqual(kwargs["data"]["fields"]["identifier"], "idmp_12345678")
        self.assertEqual(
            kwargs["data"]["fields"]["payload"]["stripe_customer_id"], "cus_12345678"
        )
        self.assertEqual(kwargs["data"]["fields"]["payload"]["value"], "25")

        # Verify the response was processed correctly
        self.assertEqual(meter_event["id"], "meter_event_123")
        self.assertEqual(meter_event["event_name"], "ai_search_api")
        self.assertEqual(meter_event["payload"]["stripe_customer_id"], "cus_12345678")
        self.assertEqual(meter_event["payload"]["value"], "25")


if __name__ == "__main__":
    unittest.main()
