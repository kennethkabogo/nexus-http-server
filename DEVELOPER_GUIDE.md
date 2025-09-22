# Developer Guide for Nexus HTTP Server

Welcome to the Nexus HTTP Server developer guide! This document will help you understand the project structure, how to contribute, and how to extend the server's functionality.

## Project Structure

The Nexus HTTP Server follows a modular architecture:

```
nexus-http-server/
├── nexus_server/           # Main Python package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Entry point
│   ├── server.py           # Core server implementation
│   ├── api/                # API route handlers
│   ├── middleware/         # Middleware functions
│   ├── security/           # Security-related functions
│   ├── utils/              # Utility functions
│   └── config.py           # Configuration settings
├── templates/              # HTML templates
├── frontend/               # React frontend application
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
├── examples/               # Example applications
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── README.md              # Project overview
├── CONTRIBUTING.md        # Contribution guidelines
├── DEVELOPER_GUIDE.md     # This file
└── LICENSE                # License information
```

## Adding New API Endpoints

To add a new API endpoint:

1. Create a new handler function in the appropriate file in `nexus_server/api/`
2. Use the `@route` decorator to register the endpoint
3. Add any necessary validation using the `@validate_json` decorator
4. Protect endpoints that require authentication with the `@require_auth` decorator

Example:
```python
# In nexus_server/api/example.py
from ..server import route, json_response
from ..utils import validate_json

@route('/api/example')
@validate_json({'name': {'type': 'string', 'required': True}})
def example_handler(request):
    name = request.data.get('name')
    return json_response({'message': f'Hello, {name}!'})
```

## Adding Middleware

To add new middleware:

1. Create a new middleware function in `nexus_server/middleware/`
2. Use the `@middleware` decorator to register it
3. Add it to the middleware chain in `nexus_server/main.py`

Example:
```python
# In nexus_server/middleware/example.py
from ..server import middleware

@middleware
def example_middleware(handler):
    def middleware_handler(request):
        # Pre-processing
        print("Before request")
        
        # Call the next handler
        response = handler(request)
        
        # Post-processing
        print("After request")
        
        return response
    return middleware_handler
```

## Security Considerations

The Nexus HTTP Server includes several built-in security features:

- Input sanitization for all user data
- JWT-based authentication
- Rate limiting
- Security headers
- Intrusion detection
- PII redaction in logs

When adding new functionality, always consider:
- Input validation and sanitization
- Authentication requirements
- Rate limiting implications
- Logging of security events

## Running Tests

To run the test suite:

```bash
# Run unit tests
make test

# Run tests with coverage
make coverage

# Run security tests
make security-test

# Run all tests
make all-tests
```

## Building and Deployment

To build the package:

```bash
# Build the package
make build

# Install in development mode
pip install -e .

# Run the server
nexus-server
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Getting Help

If you need help with development, please:
1. Check the existing documentation
2. Look at the example applications in the `examples/` directory
3. Open an issue on GitHub