"""
Paubox Forms API client.
Public endpoints for retrieving form definitions and submitting responses
require no authentication. Form management and submission-export endpoints
require a Paubox scoped API key with the 'forms' scope (or a JWT), sent as
a Bearer token.
"""

import uuid
from urllib.parse import quote

import requests
from .paubox import Response
from .helpers.errors import handle_error

FORMS_BASE_URL = "https://api.paubox.com/forms"


class PauboxFormsClient(object):
    """Client for the Paubox Forms API.

    Public endpoints (get_form, submit_form) require no authentication.
    All other endpoints require an API key with the 'forms' scope.
    """

    def __init__(self, base_url=FORMS_BASE_URL, api_key=None):
        """
        :param base_url: Forms API base URL. Defaults to https://api.paubox.com/forms.
        :type base_url: str
        :param api_key: Optional Paubox scoped API key (or JWT) with the 'forms'
            scope. Required for the authenticated form management and
            submission-export endpoints; not used by the public endpoints.
        :type api_key: str or None
        """
        self.base_url = base_url
        self.api_key = api_key

    def _auth_headers(self):
        """
        Build request headers for authenticated endpoints.

        :returns: Headers dict with Content-Type and Authorization.
        :rtype: dict
        :raises ValueError: if the client was constructed without an api_key.
        """
        if not self.api_key:
            raise ValueError(
                "An API key is required for this endpoint. Pass api_key to "
                "PauboxFormsClient — the key must be a Paubox scoped API key "
                "with the 'forms' scope."
            )
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    @staticmethod
    def _query_params(params):
        """
        Build query params: drop None values and serialize booleans as the
        lowercase strings "true"/"false" (required by the server's query
        parsing).

        :param params: Candidate query parameters.
        :type params: dict
        :returns: Cleaned query parameters.
        :rtype: dict
        """
        cleaned = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                value = "true" if value else "false"
            cleaned[key] = value
        return cleaned

    @staticmethod
    def _path_segment(value, name, require_uuid=True):
        """
        Sanitize a caller-supplied value before interpolating it into a URL path.

        Without this, a value containing "..", "/", "?" or "#" changes which
        endpoint is called. `requests` collapses dot-segments while preparing a
        URL, so the retargeting happens client-side — no server or proxy
        involvement is needed. An application that passes user input through to
        a form or submission id would otherwise be able to reach an endpoint it
        did not intend to call, and a rewritten path can leave the /forms base
        path on the same host, taking the Authorization header with it (requests
        only strips that header across a host change).

        :param value: Caller-supplied path segment — a form or submission UUID.
        :type value: str
        :param name: Argument name, used in the error message.
        :type name: str
        :param require_uuid: Reject anything that is not a UUID. True for the
            authenticated endpoints, which are new in 1.2.0 and so have no
            existing callers to stay compatible with. False for the
            long-standing public endpoints, where percent-encoding alone closes
            the issue without rejecting ids that used to be accepted.
        :type require_uuid: bool
        :returns: The value, percent-encoded for use as a single path segment.
        :rtype: str
        :raises ValueError: if the value is empty, or is not a UUID while
            require_uuid is True.
        """
        if value is None or value == "":
            raise ValueError(f"{name} is required and must not be empty.")
        value = str(value)
        # "." and ".." are dot-segments: they are resolved away rather than sent,
        # so they always retarget the request. Percent-encoding does not help —
        # quote() leaves "." alone (it is unreserved), and requests un-escapes
        # %2E during preparation anyway. Neither is ever a valid id, so reject
        # them outright rather than depending on requests' internal ordering.
        if value in (".", ".."):
            raise ValueError(
                f"{name} must not be {value!r}, which is not a valid id."
            )
        if require_uuid:
            try:
                uuid.UUID(value)
            except (AttributeError, TypeError, ValueError):
                raise ValueError(
                    f"{name} must be a UUID, got {value!r}."
                )
        # Encoded even after UUID validation, so that this stays safe if the
        # validation above is ever relaxed.
        return quote(value, safe="")

    def get_form(self, form_id):
        """
        Retrieve a form's metadata, HTML, JSON schema, and CSS by UUID.

        GET /public/form_data/{form_id}

        Public endpoint — no authentication required.

        :param form_id: UUID of the form to retrieve.
        :type form_id: str
        :returns: Response containing the form definition.
        :rtype: Response
        :raises ValueError: if form_id is empty or a bare dot-segment.
        :raises requests.exceptions.HTTPError: on 404 or other HTTP errors.
        """
        form_id = self._path_segment(form_id, "form_id", require_uuid=False)
        url = f"{self.base_url}/public/form_data/{form_id}"
        try:
            response = requests.get(url, headers={"Content-Type": "application/json"})
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def submit_form(self, form_id, form_data, attachments=None):
        """
        Submit a respondent's answers for a form.

        POST /api/forms/{form_id}/submissions

        Public endpoint — no authentication required.
        Maximum request size is 250 MB (to support file attachments).

        :param form_id: UUID of the form being submitted.
        :type form_id: str
        :param form_data: Key-value pairs matching the form's field schema.
        :type form_data: dict
        :param attachments: Optional list of dicts with 'name' (filename) and
            'content' (base64-encoded file content).
        :type attachments: list or None
        :returns: Response with status 201 and no body on success.
        :rtype: Response
        :raises ValueError: if form_data is None or empty, or if form_id is
            empty or a bare dot-segment.
        :raises requests.exceptions.HTTPError: on 400, 404, or other HTTP errors.
        """
        if not form_data:
            raise ValueError("form_data is required and must not be empty")

        form_id = self._path_segment(form_id, "form_id", require_uuid=False)
        url = f"{self.base_url}/api/forms/{form_id}/submissions"
        payload = {"form_data": form_data}
        if attachments:
            payload["attachments"] = attachments

        try:
            response = requests.post(
                url, json=payload, headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def list_forms(self, customer_id=None, form_id=None, search=None, order=None,
                   order_by=None, archived=None, active=None, page=None, items=None):
        """
        List forms, with optional filtering, ordering, and pagination.

        GET /api/forms

        :param customer_id: Customer whose forms to list. Effectively required
            for API-key callers: the server returns 403 Forbidden when it is
            omitted, so pass the customer ID your key is scoped to (or a
            related customer's).
        :type customer_id: int or None
        :param form_id: Filter to a single form UUID.
        :type form_id: str or None
        :param search: Substring match against form title and description.
        :type search: str or None
        :param order: Sort direction, "asc" or "desc". Defaults to "desc".
        :type order: str or None
        :param order_by: Sort column: "title", "updated_at", or
            "submission_count". Anything else falls back to "created_at".
        :type order_by: str or None
        :param archived: Filter by archived state.
        :type archived: bool or None
        :param active: Filter by active state.
        :type active: bool or None
        :param page: Page number, starting at 1. Defaults to 1.
        :type page: int or None
        :param items: Items per page. Defaults to 50; the server caps it at 100.
        :type items: int or None
        :returns: Response with {"results": [form...], "page_info": {"count",
            "pages", "page", "items"}}.
        :rtype: Response
        :raises ValueError: if the client has no api_key.
        :raises requests.exceptions.HTTPError: on 401, 403, or other HTTP errors.
        """
        headers = self._auth_headers()
        url = f"{self.base_url}/api/forms"
        params = self._query_params({
            "customer_id": customer_id,
            "form_id": form_id,
            "search": search,
            "order": order,
            "order_by": order_by,
            "archived": archived,
            "active": active,
            "page": page,
            "items": items,
        })
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_form_by_id(self, form_id):
        """
        Retrieve a form by UUID (authenticated variant of get_form).

        GET /api/forms/{form_id}

        :param form_id: UUID of the form to retrieve.
        :type form_id: str
        :returns: Response with {"data": {...form...}}.
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, 404, or other
            HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        url = f"{self.base_url}/api/forms/{form_id}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def create_form(self, title, form_json, customer_id, description=None,
                    form_html=None, form_css=None, recipient=None, signable=False,
                    signature_confirmation_label=None, subscription_list_id=None,
                    form_type=None, active=False, version=1, submission_count=0):
        """
        Create a new form.

        POST /api/forms

        :param title: Form title.
        :type title: str
        :param form_json: Form definition (the form's JSON schema).
        :type form_json: dict
        :param customer_id: Customer the form belongs to.
        :type customer_id: int
        :param description: Optional form description.
        :type description: str or None
        :param form_html: Optional rendered form HTML.
        :type form_html: str or None
        :param form_css: Optional form CSS.
        :type form_css: str or None
        :param recipient: Comma-separated string of notification email
            addresses.
        :type recipient: str or None
        :param signable: Whether the form is signable. Defaults to False.
        :type signable: bool
        :param signature_confirmation_label: Optional signature confirmation
            label.
        :type signature_confirmation_label: str or None
        :param subscription_list_id: Optional connected Marketing contact list.
        :type subscription_list_id: str or None
        :param form_type: Optional form type (sent as the JSON key "type"),
            e.g. "marketing_form".
        :type form_type: str or None
        :param active: Whether the form is active. Defaults to False.
        :type active: bool
        :param version: Form version. Defaults to 1.
        :type version: int
        :param submission_count: Initial submission count. Defaults to 0.
        :type submission_count: int
        :returns: Response with {"id": "<new-uuid>"}.
        :rtype: Response
        :raises ValueError: if the client has no api_key.
        :raises requests.exceptions.HTTPError: on 401, 403, or other HTTP errors.
        """
        headers = self._auth_headers()
        url = f"{self.base_url}/api/forms"
        payload = {
            "title": title,
            "form_json": form_json,
            "customer_id": customer_id,
            "signable": signable,
            "active": active,
            "version": version,
            "submission_count": submission_count,
        }
        optional = {
            "description": description,
            "form_html": form_html,
            "form_css": form_css,
            "recipient": recipient,
            "signature_confirmation_label": signature_confirmation_label,
            "subscription_list_id": subscription_list_id,
            "type": form_type,
        }
        for key, value in optional.items():
            if value is not None:
                payload[key] = value
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def update_form(self, form_id, title=None, description=None, form_json=None,
                    vanity_url=None, recipient=None, active=None,
                    subscription_list_id=None):
        """
        Update a form. PATCH-style merge: only the arguments that are not None
        are sent, and only those fields are changed on the server.

        PUT /api/forms/{form_id}

        :param form_id: UUID of the form to update.
        :type form_id: str
        :param title: New form title.
        :type title: str or None
        :param description: New form description.
        :type description: str or None
        :param form_json: New form definition.
        :type form_json: dict or None
        :param vanity_url: New vanity URL. Note: the server currently accepts
            this field but does not persist it — the value is silently ignored
            even though the call returns 200.
        :type vanity_url: str or None
        :param recipient: Comma-separated string of notification email
            addresses.
        :type recipient: str or None
        :param active: New active state.
        :type active: bool or None
        :param subscription_list_id: Connected Marketing contact list.
        :type subscription_list_id: str or None
        :returns: Response with {"detail": "Form updated successfully",
            "form_id": "<id>"}.
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, 404 (form not
            found), or other HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        url = f"{self.base_url}/api/forms/{form_id}"
        candidates = {
            "title": title,
            "description": description,
            "form_json": form_json,
            "vanity_url": vanity_url,
            "recipient": recipient,
            "active": active,
            "subscription_list_id": subscription_list_id,
        }
        payload = {key: value for key, value in candidates.items() if value is not None}
        try:
            response = requests.put(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def archive_form(self, form_id):
        """
        Archive a form (archiving also deactivates it server-side).

        POST /api/forms/{form_id}/archive

        :param form_id: UUID of the form to archive.
        :type form_id: str
        :returns: Response with {"detail": "Form archived."}.
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, or other HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        url = f"{self.base_url}/api/forms/{form_id}/archive"
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def unarchive_form(self, form_id):
        """
        Unarchive a form.

        POST /api/forms/{form_id}/unarchive

        :param form_id: UUID of the form to unarchive.
        :type form_id: str
        :returns: Response with {"detail": "Form unarchived."}.
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, or other HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        url = f"{self.base_url}/api/forms/{form_id}/unarchive"
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def copy_form(self, form_id, title):
        """
        Copy an existing form under a new title. The copy gets a fresh UUID,
        a cleared vanity_url, and a submission_count of 0.

        POST /api/forms/copy

        :param form_id: UUID of the form to copy.
        :type form_id: str
        :param title: Title for the new copy.
        :type title: str
        :returns: Response containing the full new form object.
        :rtype: Response
        :raises ValueError: if the client has no api_key.
        :raises requests.exceptions.HTTPError: on 401, 403, 404 (source form
            not found), or other HTTP errors.
        """
        headers = self._auth_headers()
        url = f"{self.base_url}/api/forms/copy"
        payload = {"form_id": form_id, "title": title}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_form_stats(self, customer_id=None):
        """
        Retrieve form statistics for a customer.

        GET /api/forms/stats

        :param customer_id: Customer to get stats for. Defaults server-side to
            the API key's customer.
        :type customer_id: int or None
        :returns: Response with {"active_form_count",
            "total_submission_count", "submissions_last_7_days"}.
        :rtype: Response
        :raises ValueError: if the client has no api_key.
        :raises requests.exceptions.HTTPError: on 401, 403, or other HTTP errors.
        """
        headers = self._auth_headers()
        url = f"{self.base_url}/api/forms/stats"
        params = self._query_params({"customer_id": customer_id})
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def list_submissions(self, form_id, submission_id=None, order_by=None,
                         order=None, page=None, items=None):
        """
        List submissions for a form, with optional filtering, ordering, and
        pagination.

        GET /api/forms/{form_id}/submissions

        :param form_id: UUID of the form.
        :type form_id: str
        :param submission_id: Filter to a single submission UUID.
        :type submission_id: str or None
        :param order_by: Sort column: "submitter_email". Anything else falls
            back to "created_at".
        :type order_by: str or None
        :param order: Sort direction, "asc" or "desc". Defaults to "desc".
        :type order: str or None
        :param page: Page number, starting at 1. Defaults to 1.
        :type page: int or None
        :param items: Items per page. Defaults to 50; the server caps it at 100.
        :type items: int or None
        :returns: Response with {"data": [submission...], "total", "page",
            "items"}. Each submission has id, form_id, form_data (a JSON
            string), storage_type, storage_url, submitter_email, recipients,
            attachment_name, attachment_url, attachment_type, and created_at.
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, 404 (form not
            found), or other HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        url = f"{self.base_url}/api/forms/{form_id}/submissions"
        params = self._query_params({
            "submission_id": submission_id,
            "order_by": order_by,
            "order": order,
            "page": page,
            "items": items,
        })
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def export_submissions_csv(self, form_id, submission_id=None):
        """
        Export a form's submissions as CSV.

        GET /api/forms/{form_id}/submissions/submission-csv (all submissions)
        GET /api/forms/{form_id}/submissions/submission-csv/{submission_id}
        (a single submission)

        :param form_id: UUID of the form.
        :type form_id: str
        :param submission_id: Optional UUID of a single submission to export.
            Omit to export all of the form's submissions.
        :type submission_id: str or None
        :returns: Response whose content property holds the CSV bytes
            (text/csv attachment).
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            or submission_id is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, 404, or other
            HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        url = f"{self.base_url}/api/forms/{form_id}/submissions/submission-csv"
        if submission_id is not None:
            submission_id = self._path_segment(submission_id, "submission_id")
            url = f"{url}/{submission_id}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def export_submission_pdf(self, form_id, submission_id):
        """
        Export a single form submission as PDF.

        GET /api/forms/{form_id}/submissions/{submission_id}/submission-pdf

        :param form_id: UUID of the form.
        :type form_id: str
        :param submission_id: UUID of the submission to export.
        :type submission_id: str
        :returns: Response whose content property holds the PDF bytes
            (application/pdf attachment).
        :rtype: Response
        :raises ValueError: if the client has no api_key, or if form_id
            or submission_id is not a UUID.
        :raises requests.exceptions.HTTPError: on 401, 403, 404, or other
            HTTP errors.
        """
        headers = self._auth_headers()
        form_id = self._path_segment(form_id, "form_id")
        submission_id = self._path_segment(submission_id, "submission_id")
        url = f"{self.base_url}/api/forms/{form_id}/submissions/{submission_id}/submission-pdf"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)
