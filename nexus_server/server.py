import os
import logging
import re  # Import re for regular expressions
from wsgiref.simple_server import make_server
from string import Template
import traceback
from urllib.parse import parse_qs
import json
from functools import reduce
import time
from collections import defaultdict
import uuid  # Import uuid for correlation IDs

# Import for input sanitization and validation
import bleach
from cerberus import Validator

# Import for cryptographic operations
import secrets
import hashlib

# Import for JWT authentication
import jwt

# Import for password hashing
import bcrypt

# Import our utilities
from .utils import render_template, json_response, redirect, validate_json, guess_type
from .security import (
    sanitize_recursive, sanitize_for_logging, log_security_event,
    is_suspicious, generate_secure_token, generate_correlation_id,
    require_auth
)
from .security.constants import SENSITIVE_HEADERS, PII_PATTERNS, SUSPICIOUS_PATTERNS

logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

routes = {}
middlewares = []
start_time = time.time()
request_count = 0
request_tracker_ip = defaultdict(list)
request_tracker_user = defaultdict(list)

DEV_MODE = True  # Set to False for production
MAX_REQUEST_SIZE = 1024 * 1024  # 1MB

# JWT Secret Key (for demonstration purposes - use environment variable in production)
SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random URL-safe text string, 32 bytes long


def route(path):
    def decorator(func):
        routes[path] = func
        return func
    return decorator


def middleware(func):
    middlewares.append(func)
    return func


# Placeholder for memory-safe data handling
def secure_delete(data):
    """
    Conceptual secure deletion. In pure Python, true memory overwriting is difficult
    due to garbage collection. This function serves as a reminder that sensitive
    data should be handled with extreme care.
    """
    if isinstance(data, (str, bytes)):
        logging.warning("Attempted conceptual secure_delete on sensitive data. "
                        "True memory overwriting is not guaranteed in Python. "
                        "Minimize sensitive data lifetime and use secure storage solutions.")
    # In a real scenario, you might try to overwrite the data if it's a mutable buffer
    # For example, if data is a bytearray:
    # if isinstance(data, bytearray):
    #     for i in range(len(data)):
    #         data[i] = 0  # Overwrite with zeros
    del data  # Allow garbage collector to reclaim memory


class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO')
        self.query_params = parse_qs(environ.get('QUERY_STRING', ''))
        self.headers = self._parse_headers(environ)
        self.data = self._parse_body(environ)
        self.cookies = self._parse_cookies(environ)

    def _parse_headers(self, environ):
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers[header_name] = value
        return headers

    def _parse_body(self, environ):
        content_length = int(environ.get('CONTENT_LENGTH') or 0)
        if content_length > MAX_REQUEST_SIZE:
            raise Exception("Request too large")
        if content_length > 0:
            body = environ['wsgi.input'].read(content_length)
            content_type = environ.get('CONTENT_TYPE', '')

            if 'application/x-www-form-urlencoded' in content_type:
                return parse_qs(body.decode('utf-8'))
            elif 'application/json' in content_type:
                try:
                    return json.loads(body.decode('utf-8'))
                except json.JSONDecodeError:
                    logging.error("JSON Decode Error: Invalid JSON in request body")
                    return None
            # Add other content types like multipart/form-data for file uploads later
        return None

    def _parse_cookies(self, environ):
        cookies = {}
        if 'HTTP_COOKIE' in environ:
            cookie_string = environ['HTTP_COOKIE']
            for cookie in cookie_string.split(';'):
                key, value = cookie.strip().split('=', 1)
                cookies[key] = value
        return cookies

    @property
    def is_ajax(self):
        return self.headers.get('X-Requested-With') == 'XMLHttpRequest'


class Response:
    def __init__(self, body='', status='200 OK', headers=None):
        self.body = body
        self.status = status
        self.headers = headers if headers is not None else [('Content-type', 'text/html')]


def create_app(routes_dict, middlewares_list):
    def application(environ, start_response):
        global request_count
        request_count += 1

        request = Request(environ)

        # Apply input sanitization middleware
        request.data = sanitize_recursive(request.data)
        request.query_params = sanitize_recursive(request.query_params)
        # Note: request.headers are usually controlled by the client and not directly user input
        # but if any custom headers are used for data, they should be sanitized.

        # Normalize path: remove trailing slash unless it's the root
        if request.path != '/' and request.path.endswith('/'):
            request.path = request.path[:-1]

        # Log sanitized request details
        logging.info("Request Method: %s", request.method)
        logging.info("Request Path: %s", request.path)
        logging.info("Request Query Params: %s", sanitize_for_logging(request.query_params))
        logging.info("Request Data: %s", sanitize_for_logging(request.data))
        logging.info("Request Headers: %s", sanitize_for_logging(request.headers))
        logging.info("Routes: %s", routes_dict)

        def handle_request(request):
            # API routes
            if request.path.startswith('/api/'):
                if request.path in routes_dict:
                    status, headers, body = routes_dict[request.path](request)
                    return Response(body, status, headers)
                else:
                    return Response(render_template('404.html'), '404 Not Found')

            # Serve static files from the React build folder
            file_path = request.path.lstrip('/')
            if not file_path:
                file_path = 'index.html'
            
            static_file_path = os.path.join('frontend', 'build', file_path)

            if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
                try:
                    with open(static_file_path, 'rb') as f:
                        headers = [
                            ('Content-type', guess_type(static_file_path)),
                            ('Cache-Control', 'max-age=3600')
                        ]
                        return Response(f.read(), '200 OK', headers)
                except IOError:
                    return Response(render_template('500.html'), '500 Internal Server Error')
            else:
                # Serve index.html for any other path
                index_path = os.path.join('frontend', 'build', 'index.html')
                if os.path.exists(index_path):
                    with open(index_path, 'rb') as f:
                        return Response(f.read(), '200 OK', [('Content-type', 'text/html')])
                else:
                    return Response(render_template('404.html'), '404 Not Found')

        # Chain middlewares
        handler = reduce(lambda h, m: m(h), reversed(middlewares_list), handle_request)

        response = handler(request)

        start_response(response.status, response.headers)
        if isinstance(response.body, bytes):
            return [response.body]
        return [response.body.encode('utf-8')]

    return application


def setup_routes():
    """Setup all application routes"""
    # Import route handlers
    from .api import get_users, get_routes, get_stats, get_logs, echo_data, login
    
    @route('/api/users')
    @require_auth  # Protect this endpoint
    def users_handler(request):
        return get_users(request)

    @route('/api/routes')
    def routes_handler(request):
        return get_routes(request)

    @route('/api/stats')
    def stats_handler(request):
        return get_stats(request)

    @route('/api/logs')
    def logs_handler(request):
        return get_logs(request)

    @route('/api/echo')
    @validate_json({'message': {'type': 'string'}, 'count': {'type': 'integer'}})
    def echo_handler(request):
        return echo_data(request)

    @route('/api/login')
    @validate_json({'username': {'type': 'string'}, 'password': {'type': 'string'}})
    def login_handler(request):
        return login(request)


# Import middleware
from .middleware import (
    error_middleware, authentication_middleware, security_headers_middleware,
    rate_limit_middleware, security_monitoring_middleware, simple_middleware
)

PORT = 8000

if __name__ == '__main__':
    setup_routes()  # Initialize all routes
    logging.info("Routes after setup: %s", routes)
    
    # The error middleware should be the first one to catch all errors
    all_middlewares = [
        error_middleware,
        authentication_middleware,
        security_headers_middleware,
        rate_limit_middleware,
        security_monitoring_middleware,
    ] + middlewares
    
    app = create_app(routes_dict=routes, middlewares_list=all_middlewares)
    httpd = make_server('', PORT, app)
    logging.info("serving at port %s", PORT)
    httpd.serve_forever()