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
SUBMISSION_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"
API_KEY = "0123456789abcdef0123456789abcdef"
AUTH_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


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
    err = requests.exceptions.HTTPError(response=response)
    return err


class TestPauboxFormsClientInit(TestCase):
    """Tests for PauboxFormsClient constructor."""

    def test_default_base_url(self):
        client = PauboxFormsClient()
        self.assertEqual(client.base_url, FORMS_BASE_URL)
        self.assertEqual(client.base_url, "https://apx.paubox.com/forms")

    def test_custom_base_url(self):
        client = PauboxFormsClient(base_url="http://localhost:3000")
        self.assertEqual(client.base_url, "http://localhost:3000")

    def test_api_key_defaults_to_none(self):
        client = PauboxFormsClient()
        self.assertIsNone(client.api_key)

    def test_api_key_stored(self):
        client = PauboxFormsClient(api_key=API_KEY)
        self.assertEqual(client.api_key, API_KEY)

    def test_base_url_still_first_positional(self):
        client = PauboxFormsClient("http://localhost:3000")
        self.assertEqual(client.base_url, "http://localhost:3000")
        self.assertIsNone(client.api_key)

    def test_base_url_and_api_key_positional(self):
        client = PauboxFormsClient("http://localhost:3000", API_KEY)
        self.assertEqual(client.base_url, "http://localhost:3000")
        self.assertEqual(client.api_key, API_KEY)


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
        client = PauboxFormsClient(base_url="https://apx.paubox.com/forms")
        client.get_form(FORM_ID)
        mock_get.assert_called_once_with(
            f"https://apx.paubox.com/forms/public/form_data/{FORM_ID}",
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
        client = PauboxFormsClient(base_url="https://apx.paubox.com/forms")
        client.submit_form(FORM_ID, form_data={"x": "y"})
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], f"https://apx.paubox.com/forms/api/forms/{FORM_ID}/submissions")

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


class TestAuthRequired(TestCase):
    """Every authenticated method raises ValueError without an api_key
    and makes no HTTP call."""

    def _assert_requires_api_key(self, call):
        client = PauboxFormsClient()
        with patch("paubox.forms.requests.get") as mock_get, \
                patch("paubox.forms.requests.post") as mock_post, \
                patch("paubox.forms.requests.put") as mock_put:
            with self.assertRaises(ValueError):
                call(client)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_put.assert_not_called()

    def test_list_forms_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.list_forms())

    def test_get_form_by_id_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.get_form_by_id(FORM_ID))

    def test_create_form_requires_api_key(self):
        self._assert_requires_api_key(
            lambda c: c.create_form("Title", {"fields": []}, 1234)
        )

    def test_update_form_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.update_form(FORM_ID, title="x"))

    def test_archive_form_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.archive_form(FORM_ID))

    def test_unarchive_form_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.unarchive_form(FORM_ID))

    def test_copy_form_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.copy_form(FORM_ID, "Copy"))

    def test_get_form_stats_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.get_form_stats())

    def test_list_submissions_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.list_submissions(FORM_ID))

    def test_export_submissions_csv_requires_api_key(self):
        self._assert_requires_api_key(lambda c: c.export_submissions_csv(FORM_ID))

    def test_export_submission_pdf_requires_api_key(self):
        self._assert_requires_api_key(
            lambda c: c.export_submission_pdf(FORM_ID, SUBMISSION_ID)
        )


class TestListForms(TestCase):
    """Tests for PauboxFormsClient.list_forms."""

    @patch("paubox.forms.requests.get")
    def test_list_forms_calls_correct_url_with_auth(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.list_forms()
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms",
            params={},
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.get")
    def test_list_forms_omits_none_params(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.list_forms(search="intake", page=2)
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"], {"search": "intake", "page": 2})

    @patch("paubox.forms.requests.get")
    def test_list_forms_serializes_booleans_lowercase(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.list_forms(archived=True, active=False)
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"], {"archived": "true", "active": "false"})

    @patch("paubox.forms.requests.get")
    def test_list_forms_passes_all_params(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.list_forms(
            customer_id=1234,
            form_id=FORM_ID,
            search="intake",
            order="asc",
            order_by="title",
            archived=False,
            active=True,
            page=3,
            items=25,
        )
        _, kwargs = mock_get.call_args
        self.assertEqual(
            kwargs["params"],
            {
                "customer_id": 1234,
                "form_id": FORM_ID,
                "search": "intake",
                "order": "asc",
                "order_by": "title",
                "archived": "false",
                "active": "true",
                "page": 3,
                "items": 25,
            },
        )

    @patch("paubox.forms.requests.get")
    def test_list_forms_parses_response(self, mock_get):
        body = (
            '{"results": [{"id": "550e8400-e29b-41d4-a716-446655440000"}],'
            '"page_info": {"count": 1, "pages": 1, "page": 1, "items": 50}}'
        )
        mock_get.return_value = _mock_response(status_code=200, text=body)
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.list_forms()
        data = response.to_dict
        self.assertEqual(data["results"][0]["id"], FORM_ID)
        self.assertEqual(data["page_info"]["count"], 1)

    @patch("paubox.forms.requests.get")
    def test_list_forms_forbidden_raises_http_error(self, mock_get):
        mock_get.return_value = _mock_response(
            status_code=403, raise_for_status=_http_error(403)
        )
        client = PauboxFormsClient(api_key=API_KEY)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.list_forms()


class TestGetFormById(TestCase):
    """Tests for PauboxFormsClient.get_form_by_id."""

    @patch("paubox.forms.requests.get")
    def test_get_form_by_id_calls_correct_url_with_auth(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.get_form_by_id(FORM_ID)
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}",
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.get")
    def test_get_form_by_id_parses_response(self, mock_get):
        body = f'{{"data": {{"id": "{FORM_ID}", "title": "Patient Intake Form"}}}}'
        mock_get.return_value = _mock_response(status_code=200, text=body)
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.get_form_by_id(FORM_ID)
        self.assertEqual(response.to_dict["data"]["id"], FORM_ID)

    @patch("paubox.forms.requests.get")
    def test_get_form_by_id_not_found_raises_http_error(self, mock_get):
        mock_get.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient(api_key=API_KEY)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_form_by_id(FORM_ID)


class TestCreateForm(TestCase):
    """Tests for PauboxFormsClient.create_form."""

    @patch("paubox.forms.requests.post")
    def test_create_form_calls_correct_url_with_auth(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text='{"id": "x"}')
        client = PauboxFormsClient(api_key=API_KEY)
        client.create_form("Intake", {"fields": []}, 1234)
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], f"{FORMS_BASE_URL}/api/forms")
        self.assertEqual(kwargs["headers"], AUTH_HEADERS)

    @patch("paubox.forms.requests.post")
    def test_create_form_required_fields_and_defaults(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text='{"id": "x"}')
        client = PauboxFormsClient(api_key=API_KEY)
        form_json = {"fields": [{"name": "first_name"}]}
        client.create_form("Intake", form_json, 1234)
        _, kwargs = mock_post.call_args
        self.assertEqual(
            kwargs["json"],
            {
                "title": "Intake",
                "form_json": form_json,
                "customer_id": 1234,
                "signable": False,
                "active": False,
                "version": 1,
                "submission_count": 0,
            },
        )

    @patch("paubox.forms.requests.post")
    def test_create_form_omits_none_optionals(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text='{"id": "x"}')
        client = PauboxFormsClient(api_key=API_KEY)
        client.create_form("Intake", {"fields": []}, 1234)
        _, kwargs = mock_post.call_args
        for key in (
            "description",
            "form_html",
            "form_css",
            "recipient",
            "signature_confirmation_label",
            "subscription_list_id",
            "type",
        ):
            self.assertNotIn(key, kwargs["json"])

    @patch("paubox.forms.requests.post")
    def test_create_form_form_type_maps_to_type_key(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text='{"id": "x"}')
        client = PauboxFormsClient(api_key=API_KEY)
        client.create_form("Intake", {"fields": []}, 1234, form_type="marketing_form")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["type"], "marketing_form")
        self.assertNotIn("form_type", kwargs["json"])

    @patch("paubox.forms.requests.post")
    def test_create_form_includes_optionals_when_set(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text='{"id": "x"}')
        client = PauboxFormsClient(api_key=API_KEY)
        client.create_form(
            "Intake",
            {"fields": []},
            1234,
            description="Patient intake",
            recipient="a@example.com,b@example.com",
            signable=True,
            active=True,
        )
        _, kwargs = mock_post.call_args
        payload = kwargs["json"]
        self.assertEqual(payload["description"], "Patient intake")
        self.assertEqual(payload["recipient"], "a@example.com,b@example.com")
        self.assertTrue(payload["signable"])
        self.assertTrue(payload["active"])

    @patch("paubox.forms.requests.post")
    def test_create_form_parses_response(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=200, text=f'{{"id": "{FORM_ID}"}}'
        )
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.create_form("Intake", {"fields": []}, 1234)
        self.assertEqual(response.to_dict["id"], FORM_ID)


class TestUpdateForm(TestCase):
    """Tests for PauboxFormsClient.update_form."""

    @patch("paubox.forms.requests.put")
    def test_update_form_calls_correct_url_with_auth(self, mock_put):
        mock_put.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.update_form(FORM_ID, title="New Title")
        args, kwargs = mock_put.call_args
        self.assertEqual(args[0], f"{FORMS_BASE_URL}/api/forms/{FORM_ID}")
        self.assertEqual(kwargs["headers"], AUTH_HEADERS)

    @patch("paubox.forms.requests.put")
    def test_update_form_sends_only_non_none_keys(self, mock_put):
        mock_put.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.update_form(FORM_ID, title="New Title")
        _, kwargs = mock_put.call_args
        self.assertEqual(kwargs["json"], {"title": "New Title"})

    @patch("paubox.forms.requests.put")
    def test_update_form_with_no_fields_sends_empty_body(self, mock_put):
        mock_put.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.update_form(FORM_ID)
        _, kwargs = mock_put.call_args
        self.assertEqual(kwargs["json"], {})

    @patch("paubox.forms.requests.put")
    def test_update_form_active_false_is_sent(self, mock_put):
        mock_put.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.update_form(FORM_ID, active=False)
        _, kwargs = mock_put.call_args
        self.assertEqual(kwargs["json"], {"active": False})

    @patch("paubox.forms.requests.put")
    def test_update_form_not_found_raises_http_error(self, mock_put):
        mock_put.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient(api_key=API_KEY)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.update_form(FORM_ID, title="x")


class TestArchiveUnarchiveForm(TestCase):
    """Tests for PauboxFormsClient.archive_form and unarchive_form."""

    @patch("paubox.forms.requests.post")
    def test_archive_form_calls_correct_url_with_auth_and_empty_body(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=200, text='{"detail": "Form archived."}'
        )
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.archive_form(FORM_ID)
        mock_post.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/archive",
            headers=AUTH_HEADERS,
        )
        self.assertEqual(response.to_dict["detail"], "Form archived.")

    @patch("paubox.forms.requests.post")
    def test_unarchive_form_calls_correct_url_with_auth_and_empty_body(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=200, text='{"detail": "Form unarchived."}'
        )
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.unarchive_form(FORM_ID)
        mock_post.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/unarchive",
            headers=AUTH_HEADERS,
        )
        self.assertEqual(response.to_dict["detail"], "Form unarchived.")


class TestCopyForm(TestCase):
    """Tests for PauboxFormsClient.copy_form."""

    @patch("paubox.forms.requests.post")
    def test_copy_form_calls_correct_url_with_auth_and_payload(self, mock_post):
        mock_post.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.copy_form(FORM_ID, "Intake (Copy)")
        mock_post.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/copy",
            json={"form_id": FORM_ID, "title": "Intake (Copy)"},
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.post")
    def test_copy_form_not_found_raises_http_error(self, mock_post):
        mock_post.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient(api_key=API_KEY)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.copy_form(FORM_ID, "Copy")


class TestGetFormStats(TestCase):
    """Tests for PauboxFormsClient.get_form_stats."""

    @patch("paubox.forms.requests.get")
    def test_get_form_stats_without_customer_id(self, mock_get):
        body = (
            '{"active_form_count": 3, "total_submission_count": 120,'
            '"submissions_last_7_days": 7}'
        )
        mock_get.return_value = _mock_response(status_code=200, text=body)
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.get_form_stats()
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/stats",
            params={},
            headers=AUTH_HEADERS,
        )
        self.assertEqual(response.to_dict["active_form_count"], 3)

    @patch("paubox.forms.requests.get")
    def test_get_form_stats_with_customer_id(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.get_form_stats(customer_id=1234)
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/stats",
            params={"customer_id": 1234},
            headers=AUTH_HEADERS,
        )


class TestListSubmissions(TestCase):
    """Tests for PauboxFormsClient.list_submissions."""

    @patch("paubox.forms.requests.get")
    def test_list_submissions_calls_correct_url_with_auth(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.list_submissions(FORM_ID)
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/submissions",
            params={},
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.get")
    def test_list_submissions_passes_params(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.list_submissions(
            FORM_ID,
            submission_id=SUBMISSION_ID,
            order_by="submitter_email",
            order="asc",
            page=2,
            items=10,
        )
        _, kwargs = mock_get.call_args
        self.assertEqual(
            kwargs["params"],
            {
                "submission_id": SUBMISSION_ID,
                "order_by": "submitter_email",
                "order": "asc",
                "page": 2,
                "items": 10,
            },
        )

    @patch("paubox.forms.requests.get")
    def test_list_submissions_parses_response(self, mock_get):
        body = (
            f'{{"data": [{{"id": "{SUBMISSION_ID}", "form_id": "{FORM_ID}",'
            '"form_data": "{\\"first_name\\": \\"Jane\\"}",'
            '"submitter_email": "jane@example.com"}],'
            '"total": 1, "page": 1, "items": 50}'
        )
        mock_get.return_value = _mock_response(status_code=200, text=body)
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.list_submissions(FORM_ID)
        data = response.to_dict
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["data"][0]["id"], SUBMISSION_ID)
        self.assertIsInstance(data["data"][0]["form_data"], str)

    @patch("paubox.forms.requests.get")
    def test_list_submissions_not_found_raises_http_error(self, mock_get):
        mock_get.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient(api_key=API_KEY)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.list_submissions(FORM_ID)


class TestExportSubmissionsCsv(TestCase):
    """Tests for PauboxFormsClient.export_submissions_csv."""

    @patch("paubox.forms.requests.get")
    def test_export_all_submissions_url(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, content=b"a,b\n1,2\n")
        client = PauboxFormsClient(api_key=API_KEY)
        client.export_submissions_csv(FORM_ID)
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/submissions/submission-csv",
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.get")
    def test_export_single_submission_url(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, content=b"a,b\n1,2\n")
        client = PauboxFormsClient(api_key=API_KEY)
        client.export_submissions_csv(FORM_ID, submission_id=SUBMISSION_ID)
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/submissions/submission-csv/{SUBMISSION_ID}",
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.get")
    def test_export_csv_content_returns_bytes(self, mock_get):
        csv_bytes = b"first_name,last_name\nJane,Doe\n"
        mock_get.return_value = _mock_response(status_code=200, content=csv_bytes)
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.export_submissions_csv(FORM_ID)
        self.assertEqual(response.content, csv_bytes)


class TestExportSubmissionPdf(TestCase):
    """Tests for PauboxFormsClient.export_submission_pdf."""

    @patch("paubox.forms.requests.get")
    def test_export_pdf_calls_correct_url_with_auth(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, content=b"%PDF-1.4")
        client = PauboxFormsClient(api_key=API_KEY)
        client.export_submission_pdf(FORM_ID, SUBMISSION_ID)
        mock_get.assert_called_once_with(
            f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/submissions/{SUBMISSION_ID}/submission-pdf",
            headers=AUTH_HEADERS,
        )

    @patch("paubox.forms.requests.get")
    def test_export_pdf_content_returns_bytes(self, mock_get):
        pdf_bytes = b"%PDF-1.4 fake pdf body"
        mock_get.return_value = _mock_response(status_code=200, content=pdf_bytes)
        client = PauboxFormsClient(api_key=API_KEY)
        response = client.export_submission_pdf(FORM_ID, SUBMISSION_ID)
        self.assertEqual(response.content, pdf_bytes)

    @patch("paubox.forms.requests.get")
    def test_export_pdf_not_found_raises_http_error(self, mock_get):
        mock_get.return_value = _mock_response(
            status_code=404, raise_for_status=_http_error(404)
        )
        client = PauboxFormsClient(api_key=API_KEY)
        with self.assertRaises(requests.exceptions.HTTPError):
            client.export_submission_pdf(FORM_ID, SUBMISSION_ID)


class TestPublicEndpointsWithApiKey(TestCase):
    """Public endpoints must not send an Authorization header even when the
    client has an api_key."""

    @patch("paubox.forms.requests.get")
    def test_get_form_sends_no_auth_header_with_api_key(self, mock_get):
        mock_get.return_value = _mock_response(status_code=200, text="{}")
        client = PauboxFormsClient(api_key=API_KEY)
        client.get_form(FORM_ID)
        _, kwargs = mock_get.call_args
        self.assertNotIn("Authorization", kwargs.get("headers", {}))

    @patch("paubox.forms.requests.post")
    def test_submit_form_sends_no_auth_header_with_api_key(self, mock_post):
        mock_post.return_value = _mock_response(status_code=201, text="")
        client = PauboxFormsClient(api_key=API_KEY)
        client.submit_form(FORM_ID, form_data={"x": "y"})
        _, kwargs = mock_post.call_args
        self.assertNotIn("Authorization", kwargs.get("headers", {}))


class TestResponseContent(TestCase):
    """Tests for the Response.content property."""

    def test_response_content_returns_raw_bytes(self):
        from paubox.paubox import Response
        raw = b"\x89PNG\r\n\x1a\n binary payload"
        response = Response(_mock_response(status_code=200, content=raw))
        self.assertEqual(response.content, raw)

    def test_response_content_and_text_coexist(self):
        from paubox.paubox import Response
        response = Response(
            _mock_response(status_code=200, text='{"a": 1}', content=b'{"a": 1}')
        )
        self.assertEqual(response.text, '{"a": 1}')
        self.assertEqual(response.content, b'{"a": 1}')
        self.assertEqual(response.to_dict, {"a": 1})


# Hostile values for anything interpolated into a URL path. Each one changes
# which endpoint is called if the segment reaches the URL unencoded, because
# `requests` collapses dot-segments while preparing the URL.
HOSTILE_SEGMENTS = [
    "../submission-csv",          # single -> bulk export
    "..",                         # export -> list endpoint
    "../../../../../v1/messages",  # escapes /forms entirely, same host
    "../../../admin/customers",
    "abc#",                       # splices a fragment, dropping later segments
    "abc?items=100",              # splices a query, overriding our own params
    "a/b",
    "%2e%2e/x",
]


class TestPathSegmentSanitization(TestCase):
    """
    A caller-supplied form or submission id must never be able to change which
    endpoint is called. Assertions are on the URL the client *builds* — a
    retargeted request can return a perfectly valid 200, so status is not a
    useful signal here.
    """

    def _requested_url(self, mock):
        args, kwargs = mock.call_args
        return args[0] if args else kwargs["url"]

    def _prepared_path(self, url, params=None):
        """Resolve the URL the way requests will, including dot-segments."""
        return requests.Request("GET", url, params=params).prepare().url

    def test_authenticated_methods_reject_non_uuid_form_id(self):
        client = PauboxFormsClient(api_key=API_KEY)
        calls = [
            ("get_form_by_id", lambda c, v: c.get_form_by_id(v)),
            ("update_form", lambda c, v: c.update_form(v, title="x")),
            ("archive_form", lambda c, v: c.archive_form(v)),
            ("unarchive_form", lambda c, v: c.unarchive_form(v)),
            ("list_submissions", lambda c, v: c.list_submissions(v)),
            ("export_submissions_csv", lambda c, v: c.export_submissions_csv(v)),
            ("export_submission_pdf",
             lambda c, v: c.export_submission_pdf(v, SUBMISSION_ID)),
        ]
        for name, call in calls:
            for hostile in HOSTILE_SEGMENTS:
                with self.subTest(method=name, value=hostile):
                    with patch("paubox.forms.requests.get") as mock_get, \
                            patch("paubox.forms.requests.post") as mock_post, \
                            patch("paubox.forms.requests.put") as mock_put:
                        with self.assertRaises(ValueError):
                            call(client, hostile)
                        mock_get.assert_not_called()
                        mock_post.assert_not_called()
                        mock_put.assert_not_called()

    def test_export_submissions_csv_rejects_traversing_submission_id(self):
        """The escalation that motivated this: single-row export -> bulk export."""
        client = PauboxFormsClient(api_key=API_KEY)
        for hostile in HOSTILE_SEGMENTS:
            with self.subTest(value=hostile):
                with patch("paubox.forms.requests.get") as mock_get:
                    with self.assertRaises(ValueError):
                        client.export_submissions_csv(
                            FORM_ID, submission_id=hostile
                        )
                    mock_get.assert_not_called()

    def test_export_submission_pdf_rejects_traversing_submission_id(self):
        client = PauboxFormsClient(api_key=API_KEY)
        for hostile in HOSTILE_SEGMENTS:
            with self.subTest(value=hostile):
                with patch("paubox.forms.requests.get") as mock_get:
                    with self.assertRaises(ValueError):
                        client.export_submission_pdf(FORM_ID, hostile)
                    mock_get.assert_not_called()

    def test_public_endpoints_encode_rather_than_reject(self):
        """
        get_form/submit_form predate this change, so they must not start
        rejecting ids that used to be accepted — but the segment still has to be
        encoded so it cannot retarget the request. The bare dot-segments are the
        one exception: they are rejected everywhere (see the test below).
        """
        client = PauboxFormsClient()
        for hostile in [s for s in HOSTILE_SEGMENTS if s not in (".", "..")]:
            with self.subTest(value=hostile):
                with patch("paubox.forms.requests.get") as mock_get:
                    mock_get.return_value = _mock_response(200, "{}")
                    client.get_form(hostile)
                    url = self._requested_url(mock_get)
                prefix = f"{FORMS_BASE_URL}/public/form_data/"
                self.assertTrue(
                    url.startswith(prefix),
                    f"{hostile!r} escaped the endpoint: {url}",
                )
                # The invariant that matters: after requests resolves the URL it
                # must still address this endpoint. Encoded dots may survive
                # (..%2Fx is inert — it is not a dot-segment); what must not
                # happen is prepare_url resolving them into a different path.
                self.assertTrue(
                    self._prepared_path(url).startswith(prefix),
                    f"{hostile!r} retargeted the request: "
                    f"{self._prepared_path(url)}",
                )

    def test_dot_segments_are_rejected_on_public_endpoints_too(self):
        """
        "." and ".." cannot be neutralized by encoding — quote() leaves "."
        alone, and requests un-escapes %2E during preparation. Neither is a
        valid id, so both are rejected even where we otherwise stay permissive.
        """
        client = PauboxFormsClient()
        for bad in [".", ".."]:
            with self.subTest(value=bad):
                with patch("paubox.forms.requests.get") as mock_get, \
                        patch("paubox.forms.requests.post") as mock_post:
                    with self.assertRaises(ValueError):
                        client.get_form(bad)
                    with self.assertRaises(ValueError):
                        client.submit_form(bad, {"a": "b"})
                    mock_get.assert_not_called()
                    mock_post.assert_not_called()

    def test_empty_and_none_ids_are_rejected_before_any_request(self):
        client = PauboxFormsClient(api_key=API_KEY)
        for bad in ["", None]:
            with self.subTest(value=bad):
                with patch("paubox.forms.requests.get") as mock_get:
                    with self.assertRaises(ValueError):
                        client.get_form_by_id(bad)
                    with self.assertRaises(ValueError):
                        client.export_submission_pdf(FORM_ID, bad)
                    mock_get.assert_not_called()

    def test_valid_uuids_still_build_the_documented_urls(self):
        """The hardening must not change the happy path."""
        client = PauboxFormsClient(api_key=API_KEY)
        with patch("paubox.forms.requests.get") as mock_get:
            mock_get.return_value = _mock_response(200, "{}")
            client.export_submission_pdf(FORM_ID, SUBMISSION_ID)
            self.assertEqual(
                self._requested_url(mock_get),
                f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/submissions/"
                f"{SUBMISSION_ID}/submission-pdf",
            )
        with patch("paubox.forms.requests.get") as mock_get:
            mock_get.return_value = _mock_response(200, "{}")
            client.export_submissions_csv(FORM_ID, submission_id=SUBMISSION_ID)
            self.assertEqual(
                self._requested_url(mock_get),
                f"{FORMS_BASE_URL}/api/forms/{FORM_ID}/submissions/"
                f"submission-csv/{SUBMISSION_ID}",
            )

    def test_uppercase_uuid_is_accepted_unchanged(self):
        """UUIDs are hex; case must not be treated as hostile."""
        client = PauboxFormsClient(api_key=API_KEY)
        upper = FORM_ID.upper()
        with patch("paubox.forms.requests.get") as mock_get:
            mock_get.return_value = _mock_response(200, "{}")
            client.get_form_by_id(upper)
            self.assertEqual(
                self._requested_url(mock_get),
                f"{FORMS_BASE_URL}/api/forms/{upper}",
            )


if __name__ == "__main__":
    SUITE = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    unittest.TextTestRunner(verbosity=2).run(SUITE)
