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
        self._from_ = None
        self._subject = None
        self._recipients = []
        self._content = None
        self._bcc = None
        self._cc = []
        self._reply_to = None
        self._attachments = []
        self._forceSecureNotification = None
        self._allowNonTLS = False
        if from_:
            self._from_ = from_
        if subject:
            self._subject = subject
        if recipients:
            self._recipients = recipients
        if content:
            if 'text/html' in content:
                _html_text = content.get('text/html')
                if(_html_text != None and _html_text != ""):
                    # _html_text (str) is encoded to a bytes-like object using _html_text.encode('utf-8')
                    # and then encode that bytes-like obj with Base64
                    # and then decode the Base64 into a string representation of the b64 conversion.
                    # we will send the string representation of the b64 conversion.
                    encoded_html = base64.b64encode(_html_text.encode('utf-8')).decode('utf-8')
                    content['text/html'] = encoded_html

            self._content = content

        if optional_headers:
            if 'bcc' in optional_headers:
                self._bcc = optional_headers['bcc']
            if 'cc' in optional_headers:
                self._cc = optional_headers['cc']
            if 'reply_to' in optional_headers:
                self._reply_to = optional_headers['reply_to']
            if 'attachments' in optional_headers:
                self._attachments = optional_headers['attachments']
            if 'forceSecureNotification' in optional_headers:
                self._forceSecureNotification = optional_headers['forceSecureNotification']
            if 'allowNonTLS' in optional_headers:
                self._allowNonTLS = optional_headers['allowNonTLS']

    def get(self):
        """Formats the Email to a Send Request for the Paubox Email API"""
        mail = {"data": {"message": {}}}
        headers = {"subject": self._subject, "from": self._from_}
        mail["data"]["message"]["recipients"] = self._recipients
        mail["data"]["message"]["headers"] = headers
        mail["data"]["message"]["content"] = self._content

        if hasattr(self, '_bcc') and self._bcc:
            mail["data"]["message"]["bcc"] = self._bcc
        if hasattr(self, '_cc') and self._cc:
            mail["data"]["message"]["cc"] = self._cc
        if hasattr(self, '_reply_to') and self._reply_to:
            mail["data"]["message"]["headers"]["reply-to"] = self._reply_to
        if hasattr(self, '_attachments') and self._attachments:
            mail["data"]["message"]["attachments"] = self._attachments
        if hasattr(self, '_forceSecureNotification'):
            self._forceSecureNotification = self._return_valid_forcesecurenotification_value()
            if(self._forceSecureNotification != None):
                mail["data"]["message"]["forceSecureNotification"] = self._forceSecureNotification
        if hasattr(self, '_allowNonTLS'):
            mail["data"]["message"]["allowNonTLS"] = self._allowNonTLS
        else:
            mail["data"]["message"]["allowNonTLS"] = False
        return mail

    def _return_valid_forcesecurenotification_value(self):
        """ Returns valid ForceSecureNotification value """

        _forceSecureNotification = self._forceSecureNotification
        if isinstance(_forceSecureNotification, str):
            if(_forceSecureNotification == None or _forceSecureNotification == ""):
                return None
            else:
                _forceSecureNotificationValue = _forceSecureNotification.strip().lower()
                if _forceSecureNotificationValue == 'true':
                    return True
                elif _forceSecureNotificationValue == 'false':
                    return False
                else:
                    return None
        elif isinstance(_forceSecureNotification, bool):
            return _forceSecureNotification
        else:
            return None
