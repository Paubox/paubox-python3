"""
Paubox webhooks API client.

Every endpoint requires a Paubox scoped API key, sent as a Bearer token —
the same scheme as the Forms API, and a different one from the Email API's
``Token token=``. Which events a key may subscribe to is decided by its
scopes: asking for one it is not scoped for is refused with 403.
"""

import json
import uuid
from urllib.parse import quote

import requests

from .paubox import Response

# The public gateway exposes only /v1/webhooks/endpoints and rewrites it onto
# the service's own /v1/endpoints, so the producers' event-ingest route is not
# reachable from here. The bare base is deliberately unrouted; every request
# below carries the /endpoints resource.
WEBHOOKS_BASE_URL = "https://api.paubox.com/v1/webhooks"


class PauboxWebhooksClient(object):
    """Client for the Paubox webhooks API."""

    def __init__(self, base_url=WEBHOOKS_BASE_URL, api_key=None):
        """
        :param base_url: Webhooks API base URL. Defaults to
            https://api.paubox.com/v1/webhooks.
        :type base_url: str
        :param api_key: Paubox scoped API key. Required for every endpoint on
            this client — unlike PauboxFormsClient there are no public routes.
        :type api_key: str or None
        """
        self.base_url = base_url
        self.api_key = api_key

    def _auth_headers(self):
        """
        Build request headers.

        :returns: Headers dict with Content-Type and Authorization.
        :rtype: dict
        :raises ValueError: if the client was constructed without an api_key.
        """
        if not self.api_key:
            raise ValueError(
                "An API key is required for this endpoint. Pass api_key to "
                "PauboxWebhooksClient — the key must be a Paubox scoped API key."
            )
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    @staticmethod
    def _path_segment(value, name):
        """
        Sanitize a caller-supplied id before interpolating it into a URL path.

        Without this, a value containing "..", "/", "?" or "#" changes which
        endpoint is called. ``requests`` collapses dot-segments while preparing
        a URL, so the retargeting happens client-side with no server or proxy
        involvement, and a rewritten path can stay on the same host — taking
        the Authorization header with it, since ``requests`` only strips that
        header across a host change.

        Unlike the Forms client there is no non-UUID fallback: every id on this
        service is a UUID, and this client is new, so there are no existing
        callers to stay compatible with.

        :param value: Caller-supplied endpoint UUID.
        :type value: str
        :param name: Argument name, used in the error message.
        :type name: str
        :returns: The percent-encoded segment.
        :rtype: str
        :raises ValueError: if the value is empty or not a UUID.
        """
        if value is None or str(value) == "":
            raise ValueError(f"{name} is required")

        text = str(value)
        try:
            uuid.UUID(text)
        except (ValueError, AttributeError, TypeError):
            raise ValueError(f"{name} must be a UUID, got {text!r}")

        # A no-op for a UUID; kept as defense-in-depth so the guarantee holds
        # if the check above is ever relaxed.
        return quote(text, safe="")

    @staticmethod
    def _raise_for_status(response):
        """
        Raise with the service's own message rather than requests' generic text.

        The service answers failures as ``{"message": "..."}``, so a caller sees
        "target_url: must be an https URL" instead of "422 Client Error:
        Unprocessable Entity for url: ...". Falls back to the default message
        when the body is not that shape.

        This deliberately does not use ``helpers.errors.handle_error``, which
        prints the response body to stdout as a side effect.

        :raises requests.exceptions.HTTPError: on any non-2xx response.
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            message = None
            try:
                body = json.loads(response.text) if response.text else None
                if isinstance(body, dict) and isinstance(body.get("message"), str):
                    message = body["message"]
            except ValueError:
                message = None
            if message:
                raise requests.exceptions.HTTPError(
                    message, response=response
                ) from error
            raise

    def list_webhook_endpoints(self, page=None, items=None):
        """
        List the webhook endpoints this key can act on.

        GET /endpoints

        Endpoints carrying an event the key is not scoped for are filtered out
        by the service, so this is what the key may manage rather than
        everything on the account.

        :param page: Optional page number.
        :type page: int or None
        :param items: Optional results per page.
        :type items: int or None
        :returns: Response whose ``to_dict`` is ``{"data": [...],
            "page_info": {...}}``. ``page_info["count"]`` is the total number
            of matching endpoints, not the length of this page.
        :rtype: Response
        :raises ValueError: if the client has no api_key.
        :raises requests.exceptions.HTTPError: on 401, 403, or other HTTP errors.
        """
        headers = self._auth_headers()
        url = f"{self.base_url}/endpoints"
        params = {k: v for k, v in (("page", page), ("items", items)) if v is not None}
        response = requests.get(url, params=params, headers=headers)
        self._raise_for_status(response)
        return Response(response)

    def create_webhook_endpoint(self, target_url, events):
        """
        Subscribe a URL to one or more events.

        POST /endpoints

        Event names are not validated here on purpose: the catalog belongs to
        the service and grows without an SDK release. An unknown event comes
        back as 422, one this key is not scoped for as 403.

        :param target_url: Delivery target. Must be an https URL resolving to
            a publicly routable address.
        :type target_url: str
        :param events: Events to subscribe to. Must be non-empty.
        :type events: list[str]
        :returns: Response whose ``to_dict`` is ``{"data": {...}, "message":
            ...}``. The data carries ``signing_secret``, which the service
            returns ONLY here — it is absent from get and list. Store it on
            receipt; a lost secret means replacing the endpoint.
        :rtype: Response
        :raises ValueError: if the client has no api_key, or target_url or
            events is missing.
        :raises requests.exceptions.HTTPError: on 403, 422, or other HTTP errors.
        """
        headers = self._auth_headers()
        if not target_url:
            raise ValueError("target_url is required")
        if not events:
            raise ValueError("events is required and must not be empty")

        url = f"{self.base_url}/endpoints"
        body = {"target_url": target_url, "events": list(events)}
        response = requests.post(url, json=body, headers=headers)
        self._raise_for_status(response)
        return Response(response)

    def get_webhook_endpoint(self, endpoint_id):
        """
        Retrieve a single webhook endpoint.

        GET /endpoints/{id}

        A malformed UUID and another tenant's id both return 404 with the same
        message — the service gives no existence oracle.

        :param endpoint_id: Endpoint UUID.
        :type endpoint_id: str
        :returns: Response whose ``to_dict`` is ``{"data": {...}}``. The
            signing secret is not included.
        :rtype: Response
        :raises ValueError: if the client has no api_key or the id is not a UUID.
        :raises requests.exceptions.HTTPError: on 404 or other HTTP errors.
        """
        headers = self._auth_headers()
        endpoint_id = self._path_segment(endpoint_id, "endpoint_id")
        url = f"{self.base_url}/endpoints/{endpoint_id}"
        response = requests.get(url, headers=headers)
        self._raise_for_status(response)
        return Response(response)

    def update_webhook_endpoint(
        self, endpoint_id, target_url=None, status=None, events=None
    ):
        """
        Update an existing endpoint.

        PATCH /endpoints/{id}

        A partial update: only the arguments given are sent, so changing
        target_url leaves events and status untouched.

        :param endpoint_id: Endpoint UUID.
        :type endpoint_id: str
        :param target_url: Optional new delivery target.
        :type target_url: str or None
        :param status: Optional. "active" or "disabled".
        :type status: str or None
        :param events: Optional replacement event list.
        :type events: list[str] or None
        :returns: Response whose ``to_dict`` is ``{"data": {...}}``.
        :rtype: Response
        :raises ValueError: if the client has no api_key, the id is not a UUID,
            or no field was given to change.
        :raises requests.exceptions.HTTPError: on 403, 422, or other HTTP errors.
        """
        headers = self._auth_headers()
        endpoint_id = self._path_segment(endpoint_id, "endpoint_id")

        body = {}
        if target_url is not None:
            body["target_url"] = target_url
        if status is not None:
            body["status"] = status
        if events is not None:
            body["events"] = list(events)
        if not body:
            raise ValueError(
                "provide at least one of target_url, status, events"
            )

        url = f"{self.base_url}/endpoints/{endpoint_id}"
        response = requests.patch(url, json=body, headers=headers)
        self._raise_for_status(response)
        return Response(response)

    def delete_webhook_endpoint(self, endpoint_id):
        """
        Delete an endpoint, stopping every event on it.

        DELETE /endpoints/{id}

        The service answers 204 with no body, so ``to_dict`` is None.

        :param endpoint_id: Endpoint UUID.
        :type endpoint_id: str
        :returns: Response with status_code 204.
        :rtype: Response
        :raises ValueError: if the client has no api_key or the id is not a UUID.
        :raises requests.exceptions.HTTPError: on 404 or other HTTP errors.
        """
        headers = self._auth_headers()
        endpoint_id = self._path_segment(endpoint_id, "endpoint_id")
        url = f"{self.base_url}/endpoints/{endpoint_id}"
        response = requests.delete(url, headers=headers)
        self._raise_for_status(response)
        return Response(response)
