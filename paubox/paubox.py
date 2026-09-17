"""
This library allows you to send emails through the Paubox Transactional Email
API application and get the email disposition of sent emails.
Paubox Client
"""

import json
import os
import requests
from .helpers.errors import handle_error

PAUBOX_API_BASE_URL = "https://api.paubox.com/v1/email"

class Response(object):
    """Response from Paubox Transactional Email API"""

    def __init__(self, response):
        self._status_code = response.status_code
        self._headers = response.headers
        self._text = response.text
        self._content = response.content

    @property
    def status_code(self):
        """
        :return: Status code of Paubox API response
        """
        return self._status_code

    @property
    def headers(self):
        """
        :return: Headers of Paubox API response
        """
        return self._headers

    @property
    def text(self):
        """
        :return: Body of Paubox API response
        """
        return self._text

    @property
    def content(self):
        """
        :return: Body of Paubox API response as raw bytes
        """
        return self._content

    @property
    def to_dict(self):
        """
        :return: Body of Paubox API response as a dict
        """
        if self.text:
            return json.loads(self.text)
        return None

class PauboxApiClient(object):
    """
    Client to send requests to the Paubox Transactional Email API
    """
    def __init__(
            self,
            api_key=os.environ.get('PAUBOX_API_KEY'),
            host=os.environ.get('PAUBOX_HOST')):
        """
        Construct API client to the Paubox Transactional Email API
        :param api_key: Paubox API key.
        :type api_key: basestring
        :params host: Optional base URL override for API calls. Defaults to
            PAUBOX_API_BASE_URL; the PAUBOX_HOST environment variable is also
            an optional override.
        :type host: basestring
        """
        self.api_key = api_key
        self.host = host or PAUBOX_API_BASE_URL

    def send(self, mail):
        """
        Send messages through the Paubox API
        """
        key = "" if self.api_key is None else self.api_key
        headers = {
            'Content-Type':'application/json',
            'Authorization': "Token token=" + key
        }
        url = self.host + '/messages'
        try:
            response = requests.post(url, json=mail, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get(self, tracking_code):
        """
        Get the disposition of messages through the Paubox API
        """
        key = "" if self.api_key is None else self.api_key
        params = {'sourceTrackingId': tracking_code}
        headers = {
            'Content-Type':'application/json',
            'Authorization': "Token token=" + key
        }
        url = self.host + '/message_receipt'
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def schedule(self, mail, scheduled_at):
        """
        Schedule a message for future delivery through the Paubox API.

        :param mail: Message payload (same format as send()).
        :param scheduled_at: ISO 8601 UTC datetime string (e.g. "2024-12-25T15:00:00Z").
        """
        key = "" if self.api_key is None else self.api_key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Token token=" + key
        }
        body = {"data": {"message": mail.get("data", {}).get("message", mail), "scheduled_at": scheduled_at}}
        url = self.host + '/schedule'
        try:
            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_scheduled(self, source_tracking_id):
        """
        Get the status of a scheduled message.
        """
        key = "" if self.api_key is None else self.api_key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Token token=" + key
        }
        url = self.host + '/schedule/' + source_tracking_id
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def reschedule(self, source_tracking_id, scheduled_at):
        """
        Reschedule a pending scheduled message.

        :param source_tracking_id: The sourceTrackingId of the scheduled message.
        :param scheduled_at: New ISO 8601 UTC datetime string.
        """
        key = "" if self.api_key is None else self.api_key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Token token=" + key
        }
        body = {"scheduled_at": scheduled_at}
        url = self.host + '/schedule/' + source_tracking_id
        try:
            response = requests.patch(url, json=body, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def cancel_scheduled(self, source_tracking_id):
        """
        Cancel a pending scheduled message.
        """
        key = "" if self.api_key is None else self.api_key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Token token=" + key
        }
        url = self.host + '/schedule/' + source_tracking_id + '/cancel'
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def _auth_headers(self):
        key = "" if self.api_key is None else self.api_key
        return {
            'Content-Type': 'application/json',
            'Authorization': "Token token=" + key
        }

    def list_receiving_domains(self):
        url = self.host + '/receiving/domains'
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def create_receiving_domain(self, slug=None):
        url = self.host + '/receiving/domains'
        body = {}
        if slug is not None:
            body['slug'] = slug
        try:
            response = requests.post(url, json=body, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_receiving_domain(self, domain_id):
        url = self.host + '/receiving/domains/' + str(domain_id)
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def delete_receiving_domain(self, domain_id):
        url = self.host + '/receiving/domains/' + str(domain_id)
        try:
            response = requests.delete(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def list_receiving_mailboxes(self, domain_id):
        url = self.host + '/receiving/domains/' + str(domain_id) + '/mailboxes'
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def create_receiving_mailbox(self, domain_id, name, password, quota_bytes=None):
        url = self.host + '/receiving/domains/' + str(domain_id) + '/mailboxes'
        body = {'name': name, 'password': password}
        if quota_bytes is not None:
            body['quota_bytes'] = quota_bytes
        try:
            response = requests.post(url, json=body, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_receiving_mailbox(self, domain_id, mailbox_id):
        url = self.host + '/receiving/domains/' + str(domain_id) + '/mailboxes/' + str(mailbox_id)
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def delete_receiving_mailbox(self, domain_id, mailbox_id):
        url = self.host + '/receiving/domains/' + str(domain_id) + '/mailboxes/' + str(mailbox_id)
        try:
            response = requests.delete(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def list_received_emails(self, limit=None, after=None, before=None):
        url = self.host + '/receiving'
        params = {}
        if limit is not None:
            params['limit'] = limit
        if after is not None:
            params['after'] = after
        if before is not None:
            params['before'] = before
        try:
            response = requests.get(url, params=params, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_received_email(self, email_id):
        url = self.host + '/receiving/' + str(email_id)
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_received_email_attachment(self, email_id, blob_id):
        url = self.host + '/receiving/' + str(email_id) + '/attachments/' + str(blob_id)
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def list_webhook_endpoints(self):
        url = self.host + '/webhook_endpoints'
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def create_webhook_endpoint(self, target_url, events, signing_key=None, api_key=None, active=True):
        url = self.host + '/webhook_endpoints'
        body = {'target_url': target_url, 'events': events, 'active': active}
        if signing_key is not None:
            body['signing_key'] = signing_key
        if api_key is not None:
            body['api_key'] = api_key
        try:
            response = requests.post(url, json=body, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def get_webhook_endpoint(self, endpoint_id):
        url = self.host + '/webhook_endpoints/' + str(endpoint_id)
        try:
            response = requests.get(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def update_webhook_endpoint(self, endpoint_id, target_url=None, events=None, active=None, api_key=None):
        url = self.host + '/webhook_endpoints/' + str(endpoint_id)
        body = {}
        if target_url is not None:
            body['target_url'] = target_url
        if events is not None:
            body['events'] = events
        if active is not None:
            body['active'] = active
        if api_key is not None:
            body['api_key'] = api_key
        try:
            response = requests.patch(url, json=body, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)

    def delete_webhook_endpoint(self, endpoint_id):
        url = self.host + '/webhook_endpoints/' + str(endpoint_id)
        try:
            response = requests.delete(url, headers=self._auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise handle_error(error)
        return Response(response)
