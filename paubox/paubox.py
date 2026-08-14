"""
This library allows you to send emails through the Paubox Transactional Email
API application and get the email disposition of sent emails.
Paubox Client
"""

import json
import os
import requests
from .helpers.errors import handle_error

PAUBOX_API_BASE_URL = "https://api.paubox.com/v1"

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
