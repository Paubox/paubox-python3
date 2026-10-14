import json
import unittest
from unittest.mock import MagicMock, patch

import requests

from paubox.webhooks import WEBHOOKS_BASE_URL, PauboxWebhooksClient

API_KEY = "test-scoped-api-key"
ENDPOINT_ID = "2ec66c21-bf48-48eb-8d28-f80b2d6b77c7"
AUTH_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

ENDPOINT = {
    "id": ENDPOINT_ID,
    "target_url": "https://hooks.example.com/paubox",
    "status": "active",
    "events": ["forms.submission.created"],
    "created_at": "2026-10-09T01:43:41.639968+00:00",
    "updated_at": "2026-10-09T01:43:41.639968+00:00",
}


def _mock_response(status_code=200, body=None):
    """A requests.Response stand-in that Response() can wrap."""
    response = MagicMock()
    response.status_code = status_code
    text = "" if body is None else json.dumps(body)
    response.text = text
    response.content = text.encode()
    response.headers = {}
    response.raise_for_status = MagicMock()
    return response


def _error_response(status_code, body):
    """A failing response whose raise_for_status raises, as requests does."""
    response = _mock_response(status_code, body)
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{status_code} Client Error", response=response
    )
    return response


def client(api_key=API_KEY):
    return PauboxWebhooksClient(api_key=api_key)


class TestConstruction(unittest.TestCase):
    def test_defaults_to_the_production_base_url(self):
        self.assertEqual(client().base_url, "https://api.paubox.com/v1/webhooks")
        self.assertEqual(WEBHOOKS_BASE_URL, "https://api.paubox.com/v1/webhooks")

    def test_base_url_is_overridable(self):
        c = PauboxWebhooksClient(
            base_url="https://api.staging.paubox.net/v1/webhooks", api_key=API_KEY
        )
        self.assertEqual(c.base_url, "https://api.staging.paubox.net/v1/webhooks")

    @patch("paubox.webhooks.requests.get")
    def test_every_method_requires_an_api_key(self, mock_get):
        c = client(api_key=None)
        for call in (
            lambda: c.list_webhook_endpoints(),
            lambda: c.get_webhook_endpoint(ENDPOINT_ID),
            lambda: c.delete_webhook_endpoint(ENDPOINT_ID),
            lambda: c.create_webhook_endpoint("https://e.test/h", ["x"]),
        ):
            with self.assertRaises(ValueError):
                call()
        mock_get.assert_not_called()


class TestListWebhookEndpoints(unittest.TestCase):
    @patch("paubox.webhooks.requests.get")
    def test_sends_bearer_auth_to_the_endpoints_resource(self, mock_get):
        mock_get.return_value = _mock_response(
            200, {"data": [ENDPOINT], "page_info": {"count": 1, "items": 50}}
        )

        result = client().list_webhook_endpoints()

        mock_get.assert_called_once_with(
            f"{WEBHOOKS_BASE_URL}/endpoints", params={}, headers=AUTH_HEADERS
        )
        self.assertEqual(result.to_dict["data"][0]["id"], ENDPOINT_ID)

    @patch("paubox.webhooks.requests.get")
    def test_count_is_the_total_not_the_page_length(self, mock_get):
        mock_get.return_value = _mock_response(
            200, {"data": [ENDPOINT], "page_info": {"count": 2, "items": 1}}
        )

        body = client().list_webhook_endpoints().to_dict

        self.assertEqual(body["page_info"]["count"], 2)
        self.assertEqual(len(body["data"]), 1)

    @patch("paubox.webhooks.requests.get")
    def test_sends_pagination_when_given(self, mock_get):
        mock_get.return_value = _mock_response(200, {"data": [], "page_info": {}})

        client().list_webhook_endpoints(page=2, items=1)

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"], {"page": 2, "items": 1})

    @patch("paubox.webhooks.requests.get")
    def test_omits_pagination_when_not_given(self, mock_get):
        mock_get.return_value = _mock_response(200, {"data": [], "page_info": {}})

        client().list_webhook_endpoints()

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"], {})


class TestCreateWebhookEndpoint(unittest.TestCase):
    @patch("paubox.webhooks.requests.post")
    def test_returns_the_signing_secret(self, mock_post):
        created = dict(ENDPOINT, signing_secret="whsec_abc123")
        mock_post.return_value = _mock_response(
            201, {"data": created, "message": "Store this signing_secret now"}
        )

        body = client().create_webhook_endpoint(
            "https://hooks.example.com/paubox", ["forms.submission.created"]
        ).to_dict

        # The secret is sent only on create; losing it means replacing the
        # endpoint.
        self.assertEqual(body["data"]["signing_secret"], "whsec_abc123")

    @patch("paubox.webhooks.requests.post")
    def test_posts_target_url_and_events(self, mock_post):
        mock_post.return_value = _mock_response(201, {"data": ENDPOINT})

        client().create_webhook_endpoint(
            "https://hooks.example.com/paubox", ["forms.submission.created"]
        )

        mock_post.assert_called_once_with(
            f"{WEBHOOKS_BASE_URL}/endpoints",
            json={
                "target_url": "https://hooks.example.com/paubox",
                "events": ["forms.submission.created"],
            },
            headers=AUTH_HEADERS,
        )

    @patch("paubox.webhooks.requests.post")
    def test_validates_locally_before_sending(self, mock_post):
        with self.assertRaises(ValueError):
            client().create_webhook_endpoint("", ["forms.submission.created"])
        with self.assertRaises(ValueError):
            client().create_webhook_endpoint("https://e.test/h", [])
        mock_post.assert_not_called()

    @patch("paubox.webhooks.requests.post")
    def test_does_not_validate_event_names(self, mock_post):
        # The catalog belongs to the service and grows without an SDK release,
        # so an unrecognised name must reach the server.
        mock_post.return_value = _mock_response(201, {"data": ENDPOINT})

        client().create_webhook_endpoint("https://e.test/h", ["some.future.event"])

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["events"], ["some.future.event"])


class TestGetWebhookEndpoint(unittest.TestCase):
    @patch("paubox.webhooks.requests.get")
    def test_requests_the_endpoint_by_id(self, mock_get):
        mock_get.return_value = _mock_response(200, {"data": ENDPOINT})

        body = client().get_webhook_endpoint(ENDPOINT_ID).to_dict

        mock_get.assert_called_once_with(
            f"{WEBHOOKS_BASE_URL}/endpoints/{ENDPOINT_ID}", headers=AUTH_HEADERS
        )
        self.assertEqual(body["data"]["id"], ENDPOINT_ID)
        self.assertNotIn("signing_secret", body["data"])

    @patch("paubox.webhooks.requests.get")
    def test_rejects_a_non_uuid_before_any_request(self, mock_get):
        with self.assertRaises(ValueError):
            client().get_webhook_endpoint("not-a-uuid")
        mock_get.assert_not_called()

    @patch("paubox.webhooks.requests.get")
    def test_rejects_a_traversal_id_before_any_request(self, mock_get):
        for bad in ("../endpoints", "..", "", None):
            with self.assertRaises(ValueError):
                client().get_webhook_endpoint(bad)
        mock_get.assert_not_called()


class TestUpdateWebhookEndpoint(unittest.TestCase):
    @patch("paubox.webhooks.requests.patch")
    def test_sends_only_the_fields_given(self, mock_patch):
        mock_patch.return_value = _mock_response(
            200, {"data": dict(ENDPOINT, status="disabled")}
        )

        client().update_webhook_endpoint(ENDPOINT_ID, status="disabled")

        mock_patch.assert_called_once_with(
            f"{WEBHOOKS_BASE_URL}/endpoints/{ENDPOINT_ID}",
            json={"status": "disabled"},
            headers=AUTH_HEADERS,
        )

    @patch("paubox.webhooks.requests.patch")
    def test_refuses_an_update_with_nothing_to_change(self, mock_patch):
        with self.assertRaises(ValueError):
            client().update_webhook_endpoint(ENDPOINT_ID)
        mock_patch.assert_not_called()


class TestDeleteWebhookEndpoint(unittest.TestCase):
    @patch("paubox.webhooks.requests.delete")
    def test_handles_an_empty_204(self, mock_delete):
        mock_delete.return_value = _mock_response(204, None)

        result = client().delete_webhook_endpoint(ENDPOINT_ID)

        mock_delete.assert_called_once_with(
            f"{WEBHOOKS_BASE_URL}/endpoints/{ENDPOINT_ID}", headers=AUTH_HEADERS
        )
        self.assertEqual(result.status_code, 204)
        self.assertIsNone(result.to_dict)


class TestErrorHandling(unittest.TestCase):
    @patch("paubox.webhooks.requests.post")
    def test_promotes_the_service_message(self, mock_post):
        mock_post.return_value = _error_response(
            422, {"message": "target_url: must be an https URL"}
        )

        with self.assertRaises(requests.exceptions.HTTPError) as ctx:
            client().create_webhook_endpoint("http://insecure.test", ["x"])

        self.assertEqual(str(ctx.exception), "target_url: must be an https URL")

    @patch("paubox.webhooks.requests.get")
    def test_names_the_event_on_a_403(self, mock_get):
        mock_get.return_value = _error_response(
            403, {"message": "events: not entitled to 'api_mail_log_delivered'"}
        )

        with self.assertRaises(requests.exceptions.HTTPError) as ctx:
            client().list_webhook_endpoints()

        self.assertIn("not entitled", str(ctx.exception))

    @patch("paubox.webhooks.requests.post")
    def test_duplicate_target_url_is_422_not_409(self, mock_post):
        # Error mapping keyed on 409 would miss this entirely.
        mock_post.return_value = _error_response(
            422, {"message": "target_url: an endpoint already exists for this URL"}
        )

        with self.assertRaises(requests.exceptions.HTTPError) as ctx:
            client().create_webhook_endpoint("https://e.test/h", ["x"])

        self.assertEqual(ctx.exception.response.status_code, 422)
        self.assertIn("already exists", str(ctx.exception))

    @patch("paubox.webhooks.requests.get")
    def test_falls_back_when_the_body_is_not_the_usual_shape(self, mock_get):
        response = _mock_response(500, None)
        response.text = "plain text failure"
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error", response=response
        )
        mock_get.return_value = response

        with self.assertRaises(requests.exceptions.HTTPError) as ctx:
            client().list_webhook_endpoints()

        self.assertIn("500 Server Error", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
