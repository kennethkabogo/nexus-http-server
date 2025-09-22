import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import directly from nexus_server modules
from nexus_server.server import Request, Response
from nexus_server.middleware.error import error_middleware
from nexus_server.middleware.auth import authentication_middleware
from nexus_server.middleware.security import security_headers_middleware
from nexus_server.middleware.rate_limit import rate_limit_middleware
from nexus_server.middleware.monitoring import security_monitoring_middleware
from nexus_server.middleware.simple import simple_middleware

class TestMiddleware(unittest.TestCase):
    """Test middleware functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock handler that returns a simple response
        self.mock_handler = MagicMock(return_value=Response('Test response'))
        
        # Create a mock request
        self.mock_request = MagicMock()
        self.mock_request.path = '/test'
        self.mock_request.environ = {'REMOTE_ADDR': '127.0.0.1'}
    
    def test_error_middleware_success(self):
        """Test error middleware with successful handler"""
        middleware = error_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        self.assertEqual(response.body, 'Test response')
        self.mock_handler.assert_called_once_with(self.mock_request)
    
    def test_error_middleware_exception(self):
        """Test error middleware handling exceptions"""
        # Create a handler that raises an exception
        def failing_handler(request):
            raise Exception("Test exception")
        
        middleware = error_middleware(failing_handler)
        response = middleware(self.mock_request)
        
        self.assertEqual(response.status, '500 Internal Server Error')
        self.assertIn('Internal Server Error', response.body)
    
    def test_security_headers_middleware(self):
        """Test security headers middleware"""
        middleware = security_headers_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        # Check that security headers are added
        header_names = [header[0] for header in response.headers]
        self.assertIn('X-Content-Type-Options', header_names)
        self.assertIn('X-Frame-Options', header_names)
        self.assertIn('X-XSS-Protection', header_names)
        self.assertIn('Referrer-Policy', header_names)
    
    def test_simple_middleware(self):
        """Test simple middleware"""
        middleware = simple_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        # Check that custom header is added
        header_names = [header[0] for header in response.headers]
        self.assertIn('X-Custom-Header', header_names)
        self.assertEqual(response.body, 'Test response')
    
    @patch('nexus_server.security.utils.is_suspicious')
    def test_security_monitoring_middleware_clean_request(self, mock_is_suspicious):
        """Test security monitoring middleware with clean request"""
        mock_is_suspicious.return_value = False
        
        middleware = security_monitoring_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        # Should call the handler for clean requests
        self.mock_handler.assert_called_once_with(self.mock_request)
        self.assertEqual(response.body, 'Test response')
    
    @patch('nexus_server.security.utils.is_suspicious')
    def test_security_monitoring_middleware_suspicious_request(self, mock_is_suspicious):
        """Test security monitoring middleware with suspicious request"""
        mock_is_suspicious.return_value = True
        
        middleware = security_monitoring_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        # Should return 400 for suspicious requests
        self.assertEqual(response.status, '400 Bad Request')
        # Should not call the handler for suspicious requests
        self.mock_handler.assert_not_called()
    
    def test_rate_limit_middleware_authenticated_user(self):
        """Test rate limit middleware with authenticated user"""
        # Mock an authenticated request
        self.mock_request.user = {'user_id': 123}
        
        middleware = rate_limit_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        # Should allow the request (not rate limited)
        self.mock_handler.assert_called_once_with(self.mock_request)
        self.assertEqual(response.body, 'Test response')
    
    def test_rate_limit_middleware_unauthenticated_user(self):
        """Test rate limit middleware with unauthenticated user"""
        # Mock an unauthenticated request
        self.mock_request.user = None
        
        middleware = rate_limit_middleware(self.mock_handler)
        response = middleware(self.mock_request)
        
        # Should allow the request (not rate limited)
        self.mock_handler.assert_called_once_with(self.mock_request)
        self.assertEqual(response.body, 'Test response')


if __name__ == '__main__':
    unittest.main()