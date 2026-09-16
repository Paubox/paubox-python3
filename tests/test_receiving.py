import json
import unittest
from unittest.mock import patch, MagicMock
from paubox.paubox import PauboxApiClient


def mock_response(status=200, body=None):
    resp = MagicMock()
    resp.status_code = status
    resp.headers = {'Content-Type': 'application/json'}
    resp.text = json.dumps(body or {})
    resp.content = resp.text.encode()
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
        mock_get.return_value = mock_response(body={'object': 'list', 'data': [], 'has_more': False})
        resp = self.client.list_received_emails()
        self.assertEqual(resp.to_dict['data'], [])

    @patch('paubox.paubox.requests.get')
    def test_list_received_emails_with_params(self, mock_get):
        mock_get.return_value = mock_response(body={'object': 'list', 'data': [], 'has_more': False})
        self.client.list_received_emails(limit=10, after='abc')
        call_kwargs = mock_get.call_args
        self.assertEqual(call_kwargs[1]['params']['limit'], 10)
        self.assertEqual(call_kwargs[1]['params']['after'], 'abc')

    @patch('paubox.paubox.requests.get')
    def test_get_received_email(self, mock_get):
        mock_get.return_value = mock_response(body={'data': {'email_id': 'eaaaaab', 'subject': 'Test'}})
        resp = self.client.get_received_email('eaaaaab')
        self.assertEqual(resp.to_dict['data']['subject'], 'Test')

    @patch('paubox.paubox.requests.get')
    def test_get_received_email_attachment(self, mock_get):
        mock_get.return_value = mock_response(body={})
        self.client.get_received_email_attachment('eaaaaab', 'blob123')
        self.assertIn('/receiving/eaaaaab/attachments/blob123', mock_get.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
