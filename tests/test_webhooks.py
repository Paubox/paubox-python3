import json
import unittest
from unittest.mock import patch, MagicMock
import requests
from paubox.paubox import PauboxApiClient


def mock_response(status=200, body=None):
    resp = MagicMock()
    resp.status_code = status
    resp.headers = {'Content-Type': 'application/json'}
    resp.text = json.dumps(body or {})
    resp.content = resp.text.encode()
    resp.raise_for_status = MagicMock()
    return resp


def _http_error(status_code):
    response = MagicMock()
    response.status_code = status_code
    response.text = json.dumps({"error": f"HTTP {status_code}"})
    return requests.exceptions.HTTPError(response=response)


WEBHOOK_DATA = {
    'id': 1,
    'target_url': 'https://example.com/webhook',
    'events': ['api_mail_log_delivered'],
    'active': True,
    'signing_key': 'sk_test',
    'api_key': None,
    'created_at': '2026-09-01T00:00:00Z',
    'updated_at': '2026-09-01T00:00:00Z',
}


class TestWebhookEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = PauboxApiClient(api_key='test_key', host='https://test.api')

    @patch('paubox.paubox.requests.get')
    def test_list_webhook_endpoints(self, mock_get):
        mock_get.return_value = mock_response(body=[WEBHOOK_DATA])
        resp = self.client.list_webhook_endpoints()
        self.assertEqual(resp.to_dict[0]['id'], 1)
        mock_get.assert_called_once()
        self.assertIn('/webhook_endpoints', mock_get.call_args[0][0])

    @patch('paubox.paubox.requests.get')
    def test_list_webhook_endpoints_error(self, mock_get):
        mock_get.return_value = mock_response(status=401)
        mock_get.return_value.raise_for_status.side_effect = _http_error(401)
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.list_webhook_endpoints()

    @patch('paubox.paubox.requests.post')
    def test_create_webhook_endpoint(self, mock_post):
        mock_post.return_value = mock_response(201, {'message': 'Webhook created!', 'data': WEBHOOK_DATA})
        resp = self.client.create_webhook_endpoint(
            target_url='https://example.com/webhook',
            events=['api_mail_log_delivered'],
        )
        self.assertEqual(resp.to_dict['data']['target_url'], 'https://example.com/webhook')
        _, kwargs = mock_post.call_args
        body = kwargs['json']
        self.assertEqual(body['target_url'], 'https://example.com/webhook')
        self.assertEqual(body['events'], ['api_mail_log_delivered'])
        self.assertTrue(body['active'])
        self.assertNotIn('signing_key', body)
        self.assertNotIn('api_key', body)

    @patch('paubox.paubox.requests.post')
    def test_create_webhook_endpoint_with_optional_fields(self, mock_post):
        mock_post.return_value = mock_response(201, {'message': 'Webhook created!', 'data': WEBHOOK_DATA})
        self.client.create_webhook_endpoint(
            target_url='https://example.com/webhook',
            events=['api_mail_log_delivered', 'inbound_mail_received'],
            signing_key='sk_test',
            api_key='ak_test',
            active=False,
        )
        _, kwargs = mock_post.call_args
        body = kwargs['json']
        self.assertEqual(body['signing_key'], 'sk_test')
        self.assertEqual(body['api_key'], 'ak_test')
        self.assertFalse(body['active'])

    @patch('paubox.paubox.requests.post')
    def test_create_webhook_endpoint_error(self, mock_post):
        mock_post.return_value = mock_response(status=422)
        mock_post.return_value.raise_for_status.side_effect = _http_error(422)
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.create_webhook_endpoint('https://example.com/webhook', ['api_mail_log_delivered'])

    @patch('paubox.paubox.requests.get')
    def test_get_webhook_endpoint(self, mock_get):
        mock_get.return_value = mock_response(body={'data': WEBHOOK_DATA})
        resp = self.client.get_webhook_endpoint(1)
        self.assertEqual(resp.to_dict['data']['id'], 1)
        self.assertIn('/webhook_endpoints/1', mock_get.call_args[0][0])

    @patch('paubox.paubox.requests.get')
    def test_get_webhook_endpoint_error(self, mock_get):
        mock_get.return_value = mock_response(status=404)
        mock_get.return_value.raise_for_status.side_effect = _http_error(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_webhook_endpoint(999)

    @patch('paubox.paubox.requests.patch')
    def test_update_webhook_endpoint(self, mock_patch):
        updated = {**WEBHOOK_DATA, 'target_url': 'https://example.com/new'}
        mock_patch.return_value = mock_response(body={'message': 'Webhook updated!', 'data': updated})
        resp = self.client.update_webhook_endpoint(1, target_url='https://example.com/new')
        self.assertEqual(resp.to_dict['data']['target_url'], 'https://example.com/new')
        self.assertIn('/webhook_endpoints/1', mock_patch.call_args[0][0])
        _, kwargs = mock_patch.call_args
        self.assertEqual(kwargs['json'], {'target_url': 'https://example.com/new'})

    @patch('paubox.paubox.requests.patch')
    def test_update_webhook_endpoint_multiple_fields(self, mock_patch):
        mock_patch.return_value = mock_response(body={'message': 'Webhook updated!', 'data': WEBHOOK_DATA})
        self.client.update_webhook_endpoint(
            1,
            events=['api_mail_log_opened'],
            active=False,
            api_key='new_key',
        )
        _, kwargs = mock_patch.call_args
        body = kwargs['json']
        self.assertEqual(body['events'], ['api_mail_log_opened'])
        self.assertFalse(body['active'])
        self.assertEqual(body['api_key'], 'new_key')
        self.assertNotIn('target_url', body)

    @patch('paubox.paubox.requests.patch')
    def test_update_webhook_endpoint_error(self, mock_patch):
        mock_patch.return_value = mock_response(status=404)
        mock_patch.return_value.raise_for_status.side_effect = _http_error(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.update_webhook_endpoint(999, target_url='https://example.com/new')

    @patch('paubox.paubox.requests.delete')
    def test_delete_webhook_endpoint(self, mock_del):
        mock_del.return_value = mock_response(body={'message': 'Webhook deleted!', 'data': WEBHOOK_DATA})
        resp = self.client.delete_webhook_endpoint(1)
        self.assertEqual(resp.to_dict['message'], 'Webhook deleted!')
        self.assertIn('/webhook_endpoints/1', mock_del.call_args[0][0])

    @patch('paubox.paubox.requests.delete')
    def test_delete_webhook_endpoint_error(self, mock_del):
        mock_del.return_value = mock_response(status=404)
        mock_del.return_value.raise_for_status.side_effect = _http_error(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.delete_webhook_endpoint(999)

    @patch('paubox.paubox.requests.get')
    def test_uses_auth_headers(self, mock_get):
        mock_get.return_value = mock_response(body=[])
        self.client.list_webhook_endpoints()
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs['headers']['Authorization'], 'Token token=test_key')


if __name__ == '__main__':
    unittest.main()
