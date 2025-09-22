import unittest
import os
import sys
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import directly from nexus_server modules
from nexus_server.server import (
    Request, Response, routes, setup_routes
)
from nexus_server.security.utils import (
    sanitize_recursive, sanitize_for_logging, is_suspicious
)
from nexus_server.security.tokens import (
    generate_secure_token, generate_correlation_id
)
from nexus_server.utils.validation import validate_json

class TestRequestParsing(unittest.TestCase):
    """Test request parsing functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/test',
            'QUERY_STRING': 'param1=value1&param2=value2',
            'HTTP_HOST': 'localhost:8000',
            'HTTP_USER_AGENT': 'test-agent',
            'wsgi.input': MagicMock()
        }
    
    def test_request_initialization(self):
        """Test Request object initialization"""
        request = Request(self.environ)
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.path, '/test')
        self.assertEqual(request.query_params, {'param1': ['value1'], 'param2': ['value2']})
        self.assertEqual(request.headers['Host'], 'localhost:8000')
        self.assertEqual(request.headers['User-Agent'], 'test-agent')
    
    def test_request_with_post_data(self):
        """Test Request object with POST data"""
        post_data = b'{"key": "value"}'
        environ = self.environ.copy()
        environ['REQUEST_METHOD'] = 'POST'
        environ['CONTENT_LENGTH'] = str(len(post_data))
        environ['CONTENT_TYPE'] = 'application/json'
        environ['wsgi.input'] = MagicMock()
        environ['wsgi.input'].read.return_value = post_data
        
        request = Request(environ)
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.data, {'key': 'value'})
    
    def test_request_with_form_data(self):
        """Test Request object with form data"""
        form_data = b'param1=value1&param2=value2'
        environ = self.environ.copy()
        environ['REQUEST_METHOD'] = 'POST'
        environ['CONTENT_LENGTH'] = str(len(form_data))
        environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
        environ['wsgi.input'] = MagicMock()
        environ['wsgi.input'].read.return_value = form_data
        
        request = Request(environ)
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.data, {'param1': ['value1'], 'param2': ['value2']})


class TestSecurityFunctions(unittest.TestCase):
    """Test security-related functions"""
    
    def test_sanitize_recursive_with_dict(self):
        """Test recursive sanitization of dictionaries"""
        data = {
            'clean': 'value',
            'xss': '<script>alert(1)</script>',
            'path': '../../etc/passwd'
        }
        sanitized = sanitize_recursive(data)
        self.assertEqual(sanitized['clean'], 'value')
        self.assertEqual(sanitized['xss'], '')
        self.assertEqual(sanitized['path'], '')
    
    def test_sanitize_recursive_with_list(self):
        """Test recursive sanitization of lists"""
        data = ['clean', '<script>alert(1)</script>', '../../etc/passwd']
        sanitized = sanitize_recursive(data)
        self.assertEqual(sanitized[0], 'clean')
        self.assertEqual(sanitized[1], '')
        self.assertEqual(sanitized[2], '')
    
    def test_sanitize_for_logging_with_sensitive_headers(self):
        """Test logging sanitization with sensitive headers"""
        data = {
            'Authorization': 'Bearer secret-token',
            'Cookie': 'session=abc123',
            'X-API-Key': 'super-secret-key',
            'Normal-Header': 'normal-value'
        }
        sanitized = sanitize_for_logging(data)
        self.assertEqual(sanitized['Authorization'], '[REDACTED]')
        self.assertEqual(sanitized['Cookie'], '[REDACTED]')
        self.assertEqual(sanitized['X-API-Key'], '[REDACTED]')
        self.assertEqual(sanitized['Normal-Header'], 'normal-value')
    
    def test_sanitize_for_logging_with_pii(self):
        """Test logging sanitization with PII"""
        data = {
            'message': 'Contact me at john.doe@example.com or call 123-45-6789',
            'normal': 'This is a normal message'
        }
        sanitized = sanitize_for_logging(data)
        self.assertIn('[REDACTED_PII]', sanitized['message'])
        self.assertNotIn('john.doe@example.com', sanitized['message'])
        self.assertNotIn('123-45-6789', sanitized['message'])
        self.assertEqual(sanitized['normal'], 'This is a normal message')
    
    def test_is_suspicious_with_xss(self):
        """Test detection of suspicious XSS patterns"""
        mock_request = MagicMock()
        mock_request.path = '/test'
        mock_request.query_params = {}
        mock_request.data = '<script>alert(1)</script>'
        mock_request.headers = {}
        
        self.assertTrue(is_suspicious(mock_request))
    
    def test_is_suspicious_with_sql_injection(self):
        """Test detection of suspicious SQL injection patterns"""
        mock_request = MagicMock()
        mock_request.path = '/test'
        mock_request.query_params = {}
        mock_request.data = "'; DROP TABLE users; --"
        mock_request.headers = {}
        
        self.assertTrue(is_suspicious(mock_request))
    
    def test_is_suspicious_clean_request(self):
        """Test that clean requests are not flagged as suspicious"""
        mock_request = MagicMock()
        mock_request.path = '/api/users'
        mock_request.query_params = {}
        mock_request.data = {'name': 'John Doe'}
        mock_request.headers = {}
        
        self.assertFalse(is_suspicious(mock_request))


class TestValidationDecorator(unittest.TestCase):
    """Test the JSON validation decorator"""
    
    def test_validate_json_valid_data(self):
        """Test validation with valid data"""
        schema = {'name': {'type': 'string'}, 'age': {'type': 'integer'}}
        
        @validate_json(schema)
        def mock_handler(request):
            return {'status': '200 OK', 'headers': [], 'body': 'Success'}
        
        mock_request = MagicMock()
        mock_request.data = {'name': 'John', 'age': 30}
        
        result = mock_handler(mock_request)
        self.assertEqual(result[2], 'Success')
    
    def test_validate_json_invalid_data(self):
        """Test validation with invalid data"""
        schema = {'name': {'type': 'string'}, 'age': {'type': 'integer'}}
        
        @validate_json(schema)
        def mock_handler(request):
            return {'status': '200 OK', 'headers': [], 'body': 'Success'}
        
        mock_request = MagicMock()
        mock_request.data = {'name': 'John', 'age': 'thirty'}  # age should be integer
        
        result = mock_handler(mock_request)
        self.assertEqual(result[0], '400 Bad Request')


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_generate_secure_token(self):
        """Test secure token generation"""
        token1 = generate_secure_token()
        token2 = generate_secure_token()
        
        self.assertIsInstance(token1, str)
        self.assertIsInstance(token2, str)
        self.assertNotEqual(token1, token2)  # Should be unique
        self.assertGreater(len(token1), 30)  # Should be reasonably long
    
    def test_generate_correlation_id(self):
        """Test correlation ID generation"""
        id1 = generate_correlation_id()
        id2 = generate_correlation_id()
        
        self.assertIsInstance(id1, str)
        self.assertIsInstance(id2, str)
        self.assertNotEqual(id1, id2)  # Should be unique


class TestRouting(unittest.TestCase):
    """Test routing functionality"""
    
    def setUp(self):
        """Set up routes before each test"""
        # Clear existing routes
        global routes
        routes.clear()
        # Setup routes
        setup_routes()
    
    def test_route_registration(self):
        """Test that routes are properly registered"""
        self.assertIn('/api/users', routes)
        self.assertIn('/api/routes', routes)
        self.assertIn('/api/stats', routes)
        self.assertIn('/api/logs', routes)
        self.assertIn('/api/echo', routes)
        self.assertIn('/api/login', routes)
    
    def test_route_handler_functions(self):
        """Test that route handlers are callable"""
        for path, handler in routes.items():
            self.assertTrue(callable(handler), f"Handler for {path} is not callable")


if __name__ == '__main__':
    unittest.main()