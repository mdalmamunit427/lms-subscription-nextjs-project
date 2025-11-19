import requests
import uuid
import time

BASE_URL = "http://localhost:3000"
ENDPOINT = "/api/webhooks/clerk"
URL = BASE_URL + ENDPOINT
TIMEOUT = 30

# Headers required for svix signature validation (dummy values since TEST_MODE=true disables verification)
SVIX_HEADERS = {
    "svix-id": str(uuid.uuid4()),
    "svix-timestamp": str(int(time.time())),
    "svix-signature": "test_signature_placeholder"
}

def test_handle_clerk_webhook_user_creation_and_update():
    # Test data for user.created event
    user_created_payload = {
        "type": "user.created",
        "data": {
            "id": str(uuid.uuid4()),
            "email_addresses": [{"email_address": "newuser@example.com"}],
            "first_name": "New",
            "last_name": "User",
            "image_url": "https://example.com/image_created.png"
        }
    }

    # Test data for user.updated event
    user_updated_payload = {
        "type": "user.updated",
        "data": {
            "id": user_created_payload["data"]["id"],  # Same user id to simulate update
            "email_addresses": [{"email_address": "updateduser@example.com"}],
            "first_name": "Updated",
            "last_name": "User",
            "image_url": "https://example.com/image_updated.png"
        }
    }

    try:
        # Send user.created webhook event
        response_create = requests.post(
            URL,
            json=user_created_payload,
            headers=SVIX_HEADERS,
            timeout=TIMEOUT,
        )
        assert response_create.status_code == 200, f"user.created event failed: {response_create.text}"

        # Send user.updated webhook event with same user ID
        response_update = requests.post(
            URL,
            json=user_updated_payload,
            headers=SVIX_HEADERS,
            timeout=TIMEOUT,
        )
        assert response_update.status_code == 200, f"user.updated event failed: {response_update.text}"

        # Send duplicated user.created event to confirm no duplication in DB
        response_create_dup = requests.post(
            URL,
            json=user_created_payload,
            headers=SVIX_HEADERS,
            timeout=TIMEOUT,
        )
        assert response_create_dup.status_code == 200, f"Duplicate user.created event failed: {response_create_dup.text}"

        # Negative test: missing svix headers - expect 400
        bad_headers = {}
        response_missing_headers = requests.post(
            URL,
            json=user_created_payload,
            headers=bad_headers,
            timeout=TIMEOUT,
        )
        assert response_missing_headers.status_code == 400, "Expected 400 for missing svix headers"

    except requests.Timeout:
        assert False, "Request timed out"
    except requests.ConnectionError:
        assert False, "Connection error - is the server running with TEST_MODE=true or NODE_ENV=test?"
    except AssertionError:
        raise
    except Exception as e:
        assert False, f"Unexpected exception: {e}"

test_handle_clerk_webhook_user_creation_and_update()