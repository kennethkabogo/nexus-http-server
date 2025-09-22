# Gemini HTTP Server Documentation

Welcome to the comprehensive documentation for the Gemini HTTP Server.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [API Reference](#api-reference)
4. [Security Features](#security-features)
5. [Middleware System](#middleware-system)
6. [Deployment](DEPLOYMENT.md)
7. [Examples](../examples/)
8. [Contributing](../CONTRIBUTING.md)

## Getting Started

### Installation

```bash
pip install gemini-http-server
```

### Quick Start

```python
from gemini_server import create_app, route, json_response

@route('/api/hello')
def hello(request):
    return json_response({'message': 'Hello, World!'})

app = create_app()
# Run the server
```

## Core Concepts

### Routing

Gemini uses a decorator-based routing system:

```python
@route('/api/users')
def get_users(request):
    return json_response({'users': [...]})
```

### Requests

The `Request` object contains all HTTP request information:

- `request.method`: HTTP method (GET, POST, etc.)
- `request.path`: Request path
- `request.query_params`: Query parameters
- `request.headers`: HTTP headers
- `request.data`: Parsed request body

### Responses

Use helper functions for common response types:

- `json_response(data)`: JSON response
- `redirect(url)`: HTTP redirect

### Middleware

Middleware functions can process requests and responses:

```python
@middleware
def custom_middleware(handler):
    def middleware_handler(request):
        # Process request
        response = handler(request)
        # Process response
        return response
    return middleware_handler
```

## API Reference

### Core Functions

#### `create_app(routes_dict, middlewares_list)`
Creates a WSGI application.

#### `@route(path)`
Decorator to register API endpoints.

#### `@middleware`
Decorator to register middleware functions.

#### `json_response(data, status='200 OK')`
Helper to create JSON responses.

#### `redirect(url, status='302 Found')`
Helper to create HTTP redirects.

#### `@validate_json(schema)`
Decorator for JSON input validation.

#### `@require_auth`
Decorator for JWT authentication protection.

### Request Object

#### Properties
- `method`: HTTP method
- `path`: Request path
- `query_params`: Query parameters
- `headers`: HTTP headers
- `data`: Parsed request body
- `cookies`: Parsed cookies

#### Methods
- `is_ajax`: Check if request is AJAX

### Response Object

#### Properties
- `body`: Response body
- `status`: HTTP status
- `headers`: HTTP headers

## Security Features

### Input Sanitization
All user inputs are automatically sanitized to prevent:
- XSS attacks
- SQL injection
- Path traversal

### Authentication
JWT-based authentication system with:
- Secure token generation
- Token expiration
- Claims validation

### Rate Limiting
Built-in rate limiting by:
- IP address
- Authenticated user

### Security Headers
Automatic addition of security headers:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Referrer-Policy

### Logging
Separate security logging with:
- PII redaction
- Suspicious activity detection
- Correlation IDs

## Middleware System

### Built-in Middleware

1. **Error Middleware**: Handles exceptions
2. **Authentication Middleware**: Processes JWT tokens
3. **Security Headers Middleware**: Adds security headers
4. **Rate Limit Middleware**: Implements rate limiting
5. **Security Monitoring Middleware**: Detects suspicious activity

### Custom Middleware

Create custom middleware by decorating a function:

```python
@middleware
def logging_middleware(handler):
    def middleware_handler(request):
        print(f"Request: {request.method} {request.path}")
        response = handler(request)
        print(f"Response: {response.status}")
        return response
    return middleware_handler
```

### Middleware Chain

Middleware is processed in order:
1. First added → Last executed
2. Error middleware should be first
3. Authentication middleware early
4. Custom middleware in desired order

## Deployment

See [Deployment Guide](DEPLOYMENT.md) for production deployment instructions.

## Examples

See the [examples](../examples/) directory for practical usage examples.