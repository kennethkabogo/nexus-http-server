"""
Gemini HTTP Server - A lightweight, security-focused HTTP server with React frontend integration.

This package provides:
- A WSGI-compliant HTTP server
- Built-in security features (XSS, SQLi, path traversal protection)
- JWT authentication
- Rate limiting
- Request sanitization
- Security logging
- Static file serving for React frontends
- API routing with decorators
- Middleware support
"""

__version__ = "1.0.0"
__author__ = "Kenneth Kabogo"
__email__ = "kennethkabogo2@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/your-username/gemini-http-server"

# Import main components for easy access
from .gemini_server.server import create_app, route, middleware, json_response, redirect, validate_json

__all__ = [
    "create_app",
    "route",
    "middleware",
    "json_response",
    "redirect",
    "validate_json",
]