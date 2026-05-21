"""
Unit tests for PauboxFormsClient.
No real HTTP calls are made — all network I/O is patched with unittest.mock.
No credentials or config.cfg required.
"""
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock
import requests

from paubox.forms import PauboxFormsClient, FORMS_BASE_URL

TestCase.maxDiff = None

FORM_ID = "550e8400-e29b-41d4-a716-446655440000"


def _mock_response(status_code=200, text="", raise_for_status=None):
    mock = MagicMock()
    mock.status_code = status_code
    mock.headers = {"Content-Type": "application/json"}
    mock.text = text
    if raise_for_status:
        mock.raise_for_status.side_effect = raise_for_status
    else:
        mock.raise_for_status.return_value = None
    return mock


def _http_error(status_code):
    response = MagicMock()
    response.status_code = status_code
    response.text = f'{{"error": "HTTP {status_code}"}}'
    err = requests.exceptions.HTTPError(response=response)
    return err


class TestPauboxFormsClientInit(TestCase):
    """Tests for PauboxFormsClient constructor."""

    def test_default_base_url(self):
        client = PauboxFormsClient()
        self.assertEqual(client.base_url, FORMS_BASE_URL)
        self.assertEqual(client.base_url, "https://next.paubox.com")

    def test_custom_base_url(self):
        client = PauboxFormsClient(base_url="http://localhost:3000")
        self.assertEqual(client.base_url, "http://localhost:3000")


class TestGetForm(TestCase):
    """Tests for PauboxFormsClient.get_form."""

    @patch("paubox.forms.requests.get")
    def test_get_form_success(self, mock_get):
        body = (
            '{"id": "550e8400-e29b-41d4-a716-446655440000", "title": "Patient Intake Form",'
            '"active": true, "submission_count": 42}'
        )
        mock_get.return_value = _mock_response(status_code=200, text=body)

        client = PauboxFormsClient()
        response = client.get_form(FORM_ID)

        self.assertEqual(response.status_code, 200)
        data = response.to_dict
        self.assertEqual(data["id"], FORM_ID)
        self.assertEqual(data["title"], "Patient Intake Form")
        self.assertTrue(data["active"])

    @patch("paubox.forms.requests.get")
    def test_get_form_calls_correct_url(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(base_url="https://next.paubox.com")
        client.get_form(FORM_ID)
        mock_get.assert_called_once_with(
            f"https://next.paubox.com/public/form_data/{FORM_ID}",
            headers={"Content-Type": "application/json"},
        )

    @patch("paubox.forms.requests.get")
    def test_get_form_sends_no_auth_header(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient()
        client.get_form(FORM_ID)
        _, kwargs = mock_get.call_args
        headers = kwargs.get("headers", {})
        self.assertNotIn("Authorization", headers)

    @patch("paubox.forms.requests.get")
    def test_get_form_not_found_raises_http_error(self, mock_get):
        mock_get.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient()
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_form(FORM_ID)

    @patch("paubox.forms.requests.get")
    def test_get_form_returns_response_object(self, mock_get):
        from paubox.paubox import Response
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient()
        response = client.get_form(FORM_ID)
        self.assertIsInstance(response, Response)


class TestSubmitForm(TestCase):
    """Tests for PauboxFormsClient.submit_form."""

    @patch("paubox.forms.requests.post")
    def test_submit_form_success(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient()
        response = client.submit_form(FORM_ID, form_data={"first_name": "Jane"})
        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.to_dict)

    @patch("paubox.forms.requests.post")
    def test_submit_form_calls_correct_url(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient(base_url="https://next.paubox.com")
        client.submit_form(FORM_ID, form_data={"x": "y"})
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], f"https://next.paubox.com/api/forms/{FORM_ID}/submissions")

    @patch("paubox.forms.requests.post")
    def test_submit_form_sends_no_auth_header(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient()
        client.submit_form(FORM_ID, form_data={"x": "y"})
        _, kwargs = mock_post.call_args
        headers = kwargs.get("headers", {})
        self.assertNotIn("Authorization", headers)

    @patch("paubox.forms.requests.post")
    def test_submit_form_payload_includes_form_data(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient()
        form_data = {"first_name": "Jane", "last_name": "Doe"}
        client.submit_form(FORM_ID, form_data=form_data)
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["form_data"], form_data)

    @patch("paubox.forms.requests.post")
    def test_submit_form_with_attachments(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient()
        attachments = [{"name": "consent.pdf", "content": "JVBERi0xLjQ="}]
        client.submit_form(FORM_ID, form_data={"sig": "x"}, attachments=attachments)
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["attachments"], attachments)

    @patch("paubox.forms.requests.post")
    def test_submit_form_without_attachments_omits_key(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient()
        client.submit_form(FORM_ID, form_data={"x": "y"})
        _, kwargs = mock_post.call_args
        self.assertNotIn("attachments", kwargs["json"])

    def test_submit_form_raises_value_error_on_empty_form_data(self):
        client = PauboxFormsClient()
        with self.assertRaises(ValueError):
            client.submit_form(FORM_ID, form_data={})

    def test_submit_form_raises_value_error_on_none_form_data(self):
        client = PauboxFormsClient()
        with self.assertRaises(ValueError):
            client.submit_form(FORM_ID, form_data=None)

    @patch("paubox.forms.requests.post")
    def test_submit_form_http_error_400(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=400, raise_for_status=_http_error(400)
        )
        client = PauboxFormsClient()
        with self.assertRaises(requests.exceptions.HTTPError):
            client.submit_form(FORM_ID, form_data={"x": "y"})

    @patch("paubox.forms.requests.post")
    def test_submit_form_http_error_404(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient()
        with self.assertRaises(requests.exceptions.HTTPError):
            client.submit_form(FORM_ID, form_data={"x": "y"})


SUITE = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(SUITE)
