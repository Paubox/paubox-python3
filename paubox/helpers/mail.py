"""
This library allows you to send emails through the Paubox Transactional Email
API application and get the email disposition of sent emails.
Paubox Mail
"""

import base64


class Mail(object):
    """Paubox API send request formatter."""

    def __init__(
            self,
            from_=None,
            subject=None,
            recipients=None,
            content=None,
            optional_headers=None):
        """
        :param from_: From email address.
        :type from: basestring
        :param subject: Email subject.
        :type subject: basestring
        :param recipients: Email recipients.
        :type recipients: list
        :param content: Body of the email.
        :type content: dict
        :params optional_headers: Additional optional headers for the email.
        :type optional_headers: dict
        """
        self._from_ = from_ or None
        self._subject = subject or None
        self._recipients = recipients or []
        self._content = None
        self._bcc = None
        self._cc = []
        self._reply_to = None
        self._attachments = []
        self._forceSecureNotification = None
        self._allowNonTLS = False
        if content:
            _html_text = content.get('text/html')
            if _html_text is not None and _html_text != "":
                # _html_text (str) is encoded to a bytes-like object using _html_text.encode('utf-8')
                # and then encode that bytes-like obj with Base64
                # and then decode the Base64 into a string representation of the b64 conversion.
                # we will send the string representation of the b64 conversion.
                content['text/html'] = base64.b64encode(
                    _html_text.encode('utf-8')).decode('utf-8')
            self._content = content

        if optional_headers:
            self._bcc = optional_headers.get('bcc')
            self._cc = optional_headers.get('cc', [])
            self._reply_to = optional_headers.get('reply_to')
            self._attachments = optional_headers.get('attachments', [])
            self._forceSecureNotification = optional_headers.get('forceSecureNotification')
            self._allowNonTLS = optional_headers.get('allowNonTLS', False)

    def get(self):
        """Formats the Email to a Send Request for the Paubox Email API"""
        mail = {"data": {"message": {}}}
        headers = {"subject": self._subject, "from": self._from_}
        mail["data"]["message"]["recipients"] = self._recipients
        mail["data"]["message"]["headers"] = headers
        mail["data"]["message"]["content"] = self._content

        if self._bcc:
            mail["data"]["message"]["bcc"] = self._bcc
        if self._cc:
            mail["data"]["message"]["cc"] = self._cc
        if self._reply_to:
            mail["data"]["message"]["headers"]["reply-to"] = self._reply_to
        if self._attachments:
            mail["data"]["message"]["attachments"] = self._attachments
        self._forceSecureNotification = self._return_valid_forcesecurenotification_value()
        if self._forceSecureNotification is not None:
            mail["data"]["message"]["forceSecureNotification"] = self._forceSecureNotification
        mail["data"]["message"]["allowNonTLS"] = self._allowNonTLS
        return mail

    def _return_valid_forcesecurenotification_value(self):
        """ Returns valid ForceSecureNotification value """

        _forceSecureNotification = self._forceSecureNotification
        if isinstance(_forceSecureNotification, str):
            return {'true': True, 'false': False}.get(
                _forceSecureNotification.strip().lower())
        if isinstance(_forceSecureNotification, bool):
            return _forceSecureNotification
        return None
