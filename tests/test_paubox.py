"""
This library allows you to send emails through the Paubox Transactional Email
API application and get the email disposition of sent emails.
Paubox Test Suite
"""
import unittest
from unittest import TestCase
import base64
import os

from paubox import paubox
from paubox.helpers.mail import Mail

from config import Config 
with open("tests/config.cfg") as config_file:
    test_credentials = Config(config_file)

TestCase.maxDiff = None


class TestPaubox(unittest.TestCase):
    """Paubox Python SDK Test Suite"""

    def test_mail_class_all_headers(self):
        """Test Mail class formatting"""
        recipients = ['recipient@example.com']
        from_ = 'sender@yourdomain.com'
        subject = 'Testing!'
        plain_html_content = '<html><body><h1>Hello World!</h1></body></html>'
        content = {
            'text/plain': 'Hello World!',
            'text/html': plain_html_content
        }
        # encode the attachment in b64 and decode to compare the string representation of the encoding
        attachment_content = base64.b64encode('Hello World!'.encode('utf-8')).decode('utf-8')
        optional_headers = {
            'attachments': [{
                'fileName': 'the_file.txt',
                'contentType': 'text/plain',
                'content': attachment_content
            }],
            'reply_to': 'replies@yourdomain.com',
            'bcc': 'recipient2@example.com',
            'cc': ['recipientcc@example.com'],
            'forceSecureNotification': 'true',
            'allowNonTLS': True
        }
        # compare the string representations of the base64 encoded message contents
        encodedHtmlContent = base64.b64encode(plain_html_content.encode('utf-8')).decode('utf-8')
        mail = Mail(from_, subject, recipients, content, optional_headers)
        expected_mail = {
            'data': {
                'message': {
                    'content': {
                        'text/plain': 'Hello World!',
                        'text/html': encodedHtmlContent
                    },
                    'headers': {
                        'reply-to': 'replies@yourdomain.com',
                        'from': 'sender@yourdomain.com',
                        'subject': 'Testing!'
                    },
                    'attachments': [
                        {
                            'content': 'SGVsbG8gV29ybGQh',
                            'contentType': 'text/plain',
                            'fileName': 'the_file.txt'
                        }
                    ],
                    'recipients': ['recipient@example.com'],
                    'bcc': 'recipient2@example.com',
                    'cc': ['recipientcc@example.com'],
                    'forceSecureNotification': True,
                    'allowNonTLS': True
                }
            }
        }
        self.assertEqual(
            mail.get(),
            expected_mail
        )

    def test_mail_class_setters(self):
        """ Test Mail class setters functionality"""
        recipients = ['recipient@example.com']
        content = {'text/plain': 'Hello World!'}
        optional_headers = {
            'cc': ['recipientcc@example.com'],
            'forceSecureNotification': 'false',
            'allowNonTLS': False
        }
        mail = Mail('', '', recipients, content, optional_headers)
        mail._from_ = 'sender@yourdomain.com'
        mail._subject = 'Testing!'
        expected_mail = {
            'data': {
                'message': {
                    'content': {
                        'text/plain': 'Hello World!'
                    },
                    'headers': {
                        'from': 'sender@yourdomain.com',
                        'subject': 'Testing!'
                    },
                    'recipients': ['recipient@example.com'],
                    'cc': ['recipientcc@example.com'],
                    'forceSecureNotification': False,
                    'allowNonTLS': False
                }
            }
        }
        self.assertEqual(
            mail.get(),
            expected_mail
        )

    def test_sending(self):
        """Test send email functionality"""
        paubox_client = paubox.PauboxApiClient(test_credentials["PAUBOX_API_KEY"], test_credentials["PAUBOX_HOST"])
        recipients = ['recipient1@example.com']
        from_ = test_credentials["APPROVED_SENDER"]
        subject = 'Testing!'
        attachment_content = base64.b64encode('Hello World!'.encode('utf-8')).decode('utf-8')
        content = {
            'text/plain': 'Hello World!',
            'text/html': "<html><body><h1>Hello World!</h1></body></html>"
        }
        optional_headers = {
            'attachments': [{
                'fileName': 'the_file.txt',
                'contentType': 'text/plain',
                'content': attachment_content
            }],
            'reply_to': test_credentials["APPROVED_SENDER"],
            'bcc': ['recipient2@example.com'],
            'cc': ['recipient3@example.com'],
            'forceSecureNotification': 'false'
        }

        mail = Mail(from_, subject, recipients, content, optional_headers)
        paubox_response = paubox_client.send(mail.get())
        self.assertEqual(paubox_response.status_code, 200)
        self.assertTrue('sourceTrackingId' in paubox_response.text)

    def test_retrieve_disposition(self):
        """Test get email disposition functionality"""
        recipients = ['recipient@example.com']
        from_ = test_credentials["APPROVED_SENDER"]
        subject = 'Testing!'
        content = {'text/plain': 'Hello World!'}
        optional_headers = {
            'cc': ['recipient3@example.com'],
            'forceSecureNotification': 'true',
            'allowNonTLS': False
        }
        mail = Mail(from_, subject, recipients, content, optional_headers)

        paubox_client = paubox.PauboxApiClient(test_credentials["PAUBOX_API_KEY"], test_credentials["PAUBOX_HOST"])
        send_response = paubox_client.send(mail.get())
        source_tracking_id = send_response.to_dict['sourceTrackingId']

        get_response = paubox_client.get(source_tracking_id)
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue('errors' not in get_response.text)


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestPaubox)
unittest.TextTestRunner(verbosity=2).run(SUITE)
