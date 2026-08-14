"""
Unit tests for PauboxApiClient.
No real HTTP calls are made — all network I/O is patched with unittest.mock.
No credentials or config.cfg required.

Note: the constructor defaults (api_key=os.environ.get('PAUBOX_API_KEY'),
host=os.environ.get('PAUBOX_HOST')) are evaluated at import time, so these
tests always pass arguments explicitly rather than relying on the environment.
"""
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock
import requests

from paubox.paubox import PauboxApiClient

TestCase.maxDiff = None

API_KEY = "0123456789abcdef0123456789abcdef"
DEFAULT_HOST = "https://api.paubox.com/v1"
CUSTOM_HOST = "https://custom.example.com/v1"
AUTH_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Token token={API_KEY}",
}
TRACKING_ID = "3d38ab13-0af8-4028-bd45-52e882e0d584"


def _mock_response(status_code=200, text="", raise_for_status=None, content=b""):
    mock = MagicMock()
    mock.status_code = status_code
    mock.headers = {"Content-Type": "application/json"}
    mock.text = text
    mock.content = content
    if raise_for_status:
        mock.raise_for_status.side_effect = raise_for_status
    else:
        mock.raise_for_status.return_value = None
    return mock


def _http_error(status_code):
    response = MagicMock()
    response.status_code = status_code
    response.text = f'{{"error": "HTTP {status_code}"}}'
    return requests.exceptions.HTTPError(response=response)


class TestPauboxApiClientInit(TestCase):
    """Tests for the PauboxApiClient constructor."""

    def test_module_exposes_default_base_url_constant(self):
        import paubox.paubox as paubox_module
        self.assertEqual(
            getattr(paubox_module, "PAUBOX_API_BASE_URL", None), DEFAULT_HOST
        )

    def test_default_host_when_none_passed(self):
        client = PauboxApiClient(api_key=API_KEY)
        self.assertEqual(client.host, DEFAULT_HOST)

    def test_default_host_when_host_is_none(self):
        client = PauboxApiClient(API_KEY, None)
        self.assertEqual(client.host, DEFAULT_HOST)

    def test_explicit_host_overrides_default(self):
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        self.assertEqual(client.host, CUSTOM_HOST)

    def test_explicit_host_overrides_default_keyword(self):
        client = PauboxApiClient(api_key=API_KEY, host=CUSTOM_HOST)
        self.assertEqual(client.host, CUSTOM_HOST)

    def test_api_key_stored(self):
        client = PauboxApiClient(API_KEY)
        self.assertEqual(client.api_key, API_KEY)


class TestSend(TestCase):
    """Tests for PauboxApiClient.send."""

    MAIL = {
        "data": {
            "message": {
                "recipients": ["recipient@example.com"],
                "headers": {
                    "subject": "Testing!",
                    "from": "sender@yourdomain.com",
                },
                "content": {"text/plain": "Hello World!"},
            }
        }
    }

    @patch("paubox.paubox.requests.post")
    def test_send_posts_to_messages_with_auth(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=200, text='{"sourceTrackingId": "%s"}' % TRACKING_ID
        )
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        client.send(self.MAIL)
        mock_post.assert_called_once_with(
            f"{CUSTOM_HOST}/messages",
            json=self.MAIL,
            headers=AUTH_HEADERS,
        )

    @patch("paubox.paubox.requests.post")
    def test_send_uses_default_host_when_none_passed(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxApiClient(api_key=API_KEY)
        client.send(self.MAIL)
        args, _ = mock_post.call_args
        self.assertEqual(args[0], f"{DEFAULT_HOST}/messages")

    @patch("paubox.paubox.requests.post")
    def test_send_parses_response(self, mock_post):
        body = f'{{"sourceTrackingId": "{TRACKING_ID}", "data": "Service OK"}}'
        mock_post.return_value = _mock_response(status_code=200, text=body)
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        response = client.send(self.MAIL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.to_dict["sourceTrackingId"], TRACKING_ID)

    @patch("paubox.paubox.requests.post")
    def test_send_returns_response_object(self, mock_post):
        from paubox.paubox import Response
        mock_post.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        self.assertIsInstance(client.send(self.MAIL), Response)

    @patch("paubox.paubox.requests.post")
    def test_send_http_error_raises(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=400, raise_for_status=_http_error(400)
        )
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.send(self.MAIL)


class TestGet(TestCase):
    """Tests for PauboxApiClient.get (message disposition)."""

    @patch("paubox.paubox.requests.get")
    def test_get_calls_message_receipt_with_params_and_auth(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        client.get(TRACKING_ID)
        mock_get.assert_called_once_with(
            f"{CUSTOM_HOST}/message_receipt",
            params={"sourceTrackingId": TRACKING_ID},
            headers=AUTH_HEADERS,
        )

    @patch("paubox.paubox.requests.get")
    def test_get_uses_default_host_when_none_passed(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxApiClient(api_key=API_KEY)
        client.get(TRACKING_ID)
        args, _ = mock_get.call_args
        self.assertEqual(args[0], f"{DEFAULT_HOST}/message_receipt")

    @patch("paubox.paubox.requests.get")
    def test_get_parses_response(self, mock_get):
        body = (
            f'{{"sourceTrackingId": "{TRACKING_ID}",'
            '"data": {"message": {"message_deliveries": []}}}'
        )
        mock_get.return_value = _mock_response(status_code=200, text=body)
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        response = client.get(TRACKING_ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.to_dict["sourceTrackingId"], TRACKING_ID)

    @patch("paubox.paubox.requests.get")
    def test_get_http_error_raises(self, mock_get):
        mock_get.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxApiClient(API_KEY, CUSTOM_HOST)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get(TRACKING_ID)


if __name__ == "__main__":
    unittest.main(verbosity=2)
