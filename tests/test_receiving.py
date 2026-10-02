import json
import unittest
import warnings
from unittest.mock import patch, MagicMock, PropertyMock
from paubox.paubox import PauboxApiClient


EMAIL_ID = '0192f0c4-0000-7000-8000-000000000001'
ATTACHMENT_ID = '0192f0c4-0000-7000-8000-0000000000a1'

ATTACHMENT = {
    'id': ATTACHMENT_ID,
    'filename': 'report.pdf',
    'content_type': 'application/pdf',
    'size': 1024,
    'content_id': None,
    'download_url': 'https://api.paubox.com/v1/email/receiving/' + EMAIL_ID + '/attachments/' + ATTACHMENT_ID,
}

LIST_ITEM = {
    'email_id': EMAIL_ID,
    'from': [{'name': 'Sender', 'address': 'sender@example.com'}],
    'to': [{'name': None, 'address': 'support@test.inbound.paubox.email'}],
    'subject': 'Test',
    'received_at': '2026-10-01T12:00:00Z',
    'has_attachment': True,
    'spam': False,
    'size': 2048,
    'domain': 'test.inbound.paubox.email',
}

DETAIL = {
    'email_id': EMAIL_ID,
    'from': [{'name': 'Sender', 'address': 'sender@example.com'}],
    'to': [{'name': None, 'address': 'support@test.inbound.paubox.email'}],
    'cc': [],
    'subject': 'Test',
    'date': '2026-10-01T11:59:58Z',
    'received_at': '2026-10-01T12:00:00Z',
    'message_id': ['<abc@example.com>'],
    'in_reply_to': None,
    'references': None,
    'spam': False,
    'spam_score': 0.1,
    'text_body': 'hello',
    'html_body': None,
    'attachments': [ATTACHMENT],
    'size': 2048,
    'authentication': {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'},
    'domain': 'test.inbound.paubox.email',
    'headers': [{'name': 'Subject', 'value': 'Test'}],
}

PDF_BYTES = b'%PDF-1.7\n\x00\xff\xfe binary'


def mock_response(status=200, body=None):
    resp = MagicMock()
    resp.status_code = status
    resp.headers = {'Content-Type': 'application/json'}
    resp.text = json.dumps(body or {})
    resp.content = resp.text.encode()
    resp.raise_for_status = MagicMock()
    return resp


def mock_file_response(content, headers):
    resp = MagicMock()
    resp.status_code = 200
    resp.headers = headers
    resp.content = content
    type(resp).text = PropertyMock(side_effect=AssertionError('binary body must not be decoded as text'))
    resp.raise_for_status = MagicMock()
    return resp


class TestReceiving(unittest.TestCase):
    def setUp(self):
        self.client = PauboxApiClient(api_key='test_key', host='https://test.api')

    @patch('paubox.paubox.requests.get')
    def test_list_receiving_domains(self, mock_get):
        mock_get.return_value = mock_response(body={'data': [{'id': 1}]})
        resp = self.client.list_receiving_domains()
        self.assertEqual(resp.to_dict['data'][0]['id'], 1)
        mock_get.assert_called_once()
        self.assertIn('/receiving/domains', mock_get.call_args[0][0])

    @patch('paubox.paubox.requests.post')
    def test_create_receiving_domain(self, mock_post):
        mock_post.return_value = mock_response(201, {'data': {'id': 1, 'domain': 'test.inbound.paubox.email'}})
        resp = self.client.create_receiving_domain(slug='test')
        self.assertEqual(resp.to_dict['data']['domain'], 'test.inbound.paubox.email')

    @patch('paubox.paubox.requests.get')
    def test_get_receiving_domain(self, mock_get):
        mock_get.return_value = mock_response(body={'data': {'id': 1}})
        resp = self.client.get_receiving_domain(1)
        self.assertEqual(resp.to_dict['data']['id'], 1)
        self.assertIn('/receiving/domains/1', mock_get.call_args[0][0])

    @patch('paubox.paubox.requests.delete')
    def test_delete_receiving_domain(self, mock_del):
        mock_del.return_value = mock_response(body={})
        resp = self.client.delete_receiving_domain(1)
        self.assertEqual(resp.to_dict, {})

    @patch('paubox.paubox.requests.get')
    def test_list_receiving_mailboxes(self, mock_get):
        mock_get.return_value = mock_response(body={'data': [{'id': 1}]})
        resp = self.client.list_receiving_mailboxes(1)
        self.assertEqual(len(resp.to_dict['data']), 1)
        self.assertIn('/receiving/domains/1/mailboxes', mock_get.call_args[0][0])

    @patch('paubox.paubox.requests.post')
    def test_create_receiving_mailbox(self, mock_post):
        mock_post.return_value = mock_response(201, {'data': {'id': 2, 'email': 'support@test.inbound.paubox.email'}})
        resp = self.client.create_receiving_mailbox(1, 'support', 'secret')
        self.assertEqual(resp.to_dict['data']['email'], 'support@test.inbound.paubox.email')

    @patch('paubox.paubox.requests.get')
    def test_get_receiving_mailbox(self, mock_get):
        mock_get.return_value = mock_response(body={'data': {'id': 2}})
        resp = self.client.get_receiving_mailbox(1, 2)
        self.assertIn('/receiving/domains/1/mailboxes/2', mock_get.call_args[0][0])

    @patch('paubox.paubox.requests.delete')
    def test_delete_receiving_mailbox(self, mock_del):
        mock_del.return_value = mock_response(body={})
        self.client.delete_receiving_mailbox(1, 2)
        self.assertIn('/receiving/domains/1/mailboxes/2', mock_del.call_args[0][0])

    @patch('paubox.paubox.requests.get')
    def test_list_received_emails(self, mock_get):
        mock_get.return_value = mock_response(body={'object': 'list', 'data': [LIST_ITEM], 'has_more': False})
        resp = self.client.list_received_emails()
        self.assertTrue(mock_get.call_args[0][0].endswith('/receiving'))
        self.assertEqual(mock_get.call_args[1]['params'], {})
        body = resp.to_dict
        self.assertEqual(body['object'], 'list')
        self.assertFalse(body['has_more'])
        item = body['data'][0]
        self.assertEqual(item['email_id'], EMAIL_ID)
        self.assertEqual(item['from'][0]['address'], 'sender@example.com')
        self.assertNotIn('blob_id', item)
        self.assertNotIn('account_id', item)

    @patch('paubox.paubox.requests.get')
    def test_list_received_emails_with_params(self, mock_get):
        mock_get.return_value = mock_response(body={'object': 'list', 'data': [], 'has_more': False})
        self.client.list_received_emails(
            limit=10, after=EMAIL_ID, before=ATTACHMENT_ID, search='invoice', sort='received_at', ascending=True,
        )
        self.assertEqual(mock_get.call_args[1]['params'], {
            'limit': 10,
            'after': EMAIL_ID,
            'before': ATTACHMENT_ID,
            'search': 'invoice',
            'sort': 'received_at',
            'ascending': 'true',
        })

    @patch('paubox.paubox.requests.get')
    def test_list_received_emails_ascending_false(self, mock_get):
        mock_get.return_value = mock_response(body={'object': 'list', 'data': [], 'has_more': False})
        self.client.list_received_emails(ascending=False)
        self.assertEqual(mock_get.call_args[1]['params'], {'ascending': 'false'})

    @patch('paubox.paubox.requests.get')
    def test_get_received_email(self, mock_get):
        mock_get.return_value = mock_response(body={'data': DETAIL})
        resp = self.client.get_received_email(EMAIL_ID)
        self.assertTrue(mock_get.call_args[0][0].endswith('/receiving/' + EMAIL_ID))
        data = resp.to_dict['data']
        self.assertEqual(data['email_id'], EMAIL_ID)
        self.assertEqual(data['authentication']['dmarc'], 'pass')
        self.assertEqual(data['attachments'][0]['id'], ATTACHMENT_ID)
        self.assertNotIn('blob_id', data['attachments'][0])

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_raw(self, mock_get):
        mock_get.return_value = mock_response(body={'data': {'raw_message': 'Subject: Test\r\n\r\nhello'}})
        resp = self.client.get_received_email_raw(EMAIL_ID)
        self.assertTrue(mock_get.call_args[0][0].endswith('/receiving/' + EMAIL_ID + '/raw'))
        self.assertEqual(resp.to_dict['data']['raw_message'], 'Subject: Test\r\n\r\nhello')

    @patch('paubox.paubox.requests.get')
    def test_list_received_email_attachments(self, mock_get):
        mock_get.return_value = mock_response(body={'data': [ATTACHMENT]})
        resp = self.client.list_received_email_attachments(EMAIL_ID)
        self.assertTrue(mock_get.call_args[0][0].endswith('/receiving/' + EMAIL_ID + '/attachments'))
        self.assertEqual(resp.to_dict['data'][0]['id'], ATTACHMENT_ID)

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_attachment_returns_bytes(self, mock_get):
        mock_get.return_value = mock_file_response(PDF_BYTES, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="report.pdf"',
        })
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            resp = self.client.get_received_email_attachment(EMAIL_ID, ATTACHMENT_ID)
        self.assertTrue(mock_get.call_args[0][0].endswith('/receiving/' + EMAIL_ID + '/attachments/' + ATTACHMENT_ID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, PDF_BYTES)
        self.assertEqual(resp.headers['Content-Type'], 'application/pdf')
        self.assertEqual(resp.headers['Content-Disposition'], 'attachment; filename="report.pdf"')

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_attachment_by_keyword(self, mock_get):
        mock_get.return_value = mock_file_response(PDF_BYTES, {'Content-Type': 'application/pdf'})
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            resp = self.client.get_received_email_attachment(email_id=EMAIL_ID, attachment_id=ATTACHMENT_ID)
        self.assertTrue(mock_get.call_args[0][0].endswith('/attachments/' + ATTACHMENT_ID))
        self.assertEqual(resp.content, PDF_BYTES)

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_attachment_blob_id_alias_is_deprecated(self, mock_get):
        mock_get.return_value = mock_file_response(PDF_BYTES, {'Content-Type': 'application/pdf'})
        with self.assertWarns(DeprecationWarning) as caught:
            resp = self.client.get_received_email_attachment(EMAIL_ID, blob_id=ATTACHMENT_ID)
        self.assertIn('attachment_id', str(caught.warning))
        self.assertEqual(caught.filename, __file__)
        self.assertTrue(mock_get.call_args[0][0].endswith('/receiving/' + EMAIL_ID + '/attachments/' + ATTACHMENT_ID))
        self.assertEqual(resp.content, PDF_BYTES)

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_attachment_rejects_both_ids(self, mock_get):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            with self.assertRaises(TypeError):
                self.client.get_received_email_attachment(EMAIL_ID, ATTACHMENT_ID, blob_id=ATTACHMENT_ID)
        mock_get.assert_not_called()

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_attachment_requires_id(self, mock_get):
        with self.assertRaises(TypeError):
            self.client.get_received_email_attachment(EMAIL_ID)
        mock_get.assert_not_called()

if __name__ == '__main__':
    unittest.main()
