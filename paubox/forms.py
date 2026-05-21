"""
Paubox Forms API client.
Public endpoints for retrieving form definitions and submitting responses.
No authentication is required for these endpoints.
"""

import requests
from .paubox import Response
from .helpers.errors import handle_error

FORMS_BASE_URL = "https://apx.paubox.com/forms"


class PauboxFormsClient(object):
    """Client for the Paubox Forms API (public endpoints, no authentication required)."""

    def __init__(self, base_url=FORMS_BASE_URL):
        """
        :param base_url: Forms API base URL. Defaults to https://apx.paubox.com/forms.
        :type base_url: str
        """
        self.base_url = base_url

    def get_form(self, form_id):
        """
        Retrieve a form's metadata, HTML, JSON schema, and CSS by UUID.

        GET /public/form_data/{form_id}

        :param form_id: UUID of the form to retrieve.
        :type form_id: str
        :returns: Response containing the form definition.
        :rtype: Response
        :raises requests.exceptions.HTTPError: on 404 or other HTTP errors.
        """
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
        :raises ValueError: if form_data is None or empty.
        :raises requests.exceptions.HTTPError: on 400, 404, or other HTTP errors.
        """
        if not form_data:
            raise ValueError("form_data is required and must not be empty")

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
