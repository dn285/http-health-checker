import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import requests
import unittest
from unittest.mock import patch, Mock
from src.health_checker import load_endpoints, check_health

class TestHealthChecker(unittest.TestCase):
    
    def test_load_endpoints_valid_file(self):
        filepath = os.path.join(os.path.dirname(__file__), 'valid_endpoints.yml')
        endpoints = load_endpoints(filepath)

        self.assertIsNotNone(endpoints)
        self.assertIsInstance(endpoints, list)
        self.assertTrue(len(endpoints) > 0)

        for endpoint in endpoints:
            self.assertIn('name', endpoint)
            self.assertIn('url', endpoint)

            if 'method' in endpoint:
                # assume is valid
                ... 
            else:
                self.assertEqual(endpoint.get('method', 'GET'), 'GET')
            
            if 'headers' in endpoint:
                self.assertIsInstance(endpoint['headers'], dict)
            else:
                self.assertIsNone(endpoint.get('headers'))
            
            if 'body' in endpoint:
                self.assertIsInstance(endpoint['body'], str)
            else:
                self.assertIsNone(endpoint.get('body'))
    
    def test_load_endpoints_invalid_file(self):
        filepath = os.path.join(os.path.dirname(__file__), 'invalid_endpoints.yml')
        endpoints = load_endpoints(filepath)
        self.assertIsNone(endpoints)

    @patch('src.health_checker.requests.request')
    def test_check_health_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.3
        mock_request.return_value = mock_response

        endpoint = {'url': "https://example.com"}

        self.assertTrue(check_health(endpoint))
    
    @patch('src.health_checker.requests.request')
    def test_check_health_timeout(self, mock_request):
        mock_request.side_effect = requests.RequestException

        endpoint = {'url': "https://example.com"}

        self.assertFalse(check_health(endpoint))
    
    @patch('src.health_checker.requests.request')
    def test_check_health_failure_status(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.elapsed.total_seconds.return_value = 0.2
        mock_request.return_value = mock_response

        endpoint = {'url': "https://example.com"}

        self.assertFalse(check_health(endpoint))
    
    @patch('src.health_checker.requests.request')
    def test_check_health_slow_response(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.6
        mock_request.return_value = mock_response

        endpoint = {'url': "https://example.com"}

        self.assertFalse(check_health(endpoint))