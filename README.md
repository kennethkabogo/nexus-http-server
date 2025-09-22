# Nexus HTTP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Build Status](https://github.com/kennethkabogo/nexus-http-server/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/kennethkabogo/nexus-http-server/actions)
[![codecov](https://codecov.io/gh/kennethkabogo/nexus-http-server/branch/main/graph/badge.svg)](https://codecov.io/gh/kennethkabogo/nexus-http-server)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](docs/)

Nexus HTTP Server: A lightweight, security-focused Python HTTP server with integrated React frontend. Built with cybersecurity best practices including JWT authentication, rate limiting, input sanitization, and intrusion detection.

## Why Nexus?

Nexus offers developers a secure, batteries-included HTTP server that's perfect for:
- Rapid prototyping of web applications
- Educational purposes (understanding HTTP servers and security)
- Small to medium-scale production deployments
- Learning best practices in web security

## Features

### Core Server Capabilities

*   **Lightweight WSGI Server:** Built on Python's `wsgiref.simple_server` for efficient request handling.
*   **Decorator-based Routing:** Define API endpoints easily using the `@route` decorator.
*   **Middleware Support:** Extend server functionality with a flexible `@middleware` system to process requests and responses.
*   **Static File Serving:** Seamlessly serves static assets from the `frontend/build` directory, ideal for single-page applications.
*   **Templating:** Simple HTML template rendering for dynamic content (e.g., error pages).
*   **JSON Responses:** Helper function for convenient JSON data serialization in API responses.
*   **Redirection:** Utility for performing HTTP redirects.
*   **Automatic Request Parsing:** Handles parsing of request methods, paths, query parameters, headers, and JSON/form-urlencoded bodies.
*   **MIME Type Guessing:** Automatically determines content types for served files.
*   **Comprehensive Logging:** Records server activity and errors to `server.log`.

### Cybersecurity and Data Privacy Enhancements

*   **Security Headers Middleware:** Automatically adds crucial HTTP security headers to all responses:
    *   `X-Content-Type-Options: nosniff`
    *   `X-Frame-Options: DENY`
    *   `X-XSS-Protection: 1; mode=block`
    *   `Referrer-Policy: no-referrer-when-downgrade`
    *   `Content-Security-Policy` (configurable)
*   **JWT Authentication:** Secure token-based authentication system for API endpoints.
*   **Input Sanitization:** Recursive sanitization of all user inputs to prevent XSS, SQL injection, and path traversal attacks.
*   **Rate Limiting:** IP and user-based rate limiting to prevent abuse.
*   **PII Redaction:** Automatic redaction of personally identifiable information (SSN, emails) in logs.
*   **Intrusion Detection:** Pattern matching to detect and block common attack vectors.
*   **Security Logging:** Dedicated security event logging to `security.log`.
*   **Restricted Log Access:** The `/api/logs` endpoint is restricted to development mode (`DEV_MODE = True`) to prevent sensitive log information from being exposed in production.
*   **Input Validation Decorator:** Includes a `validate_json` decorator for schema validation of incoming JSON request bodies, enhancing data integrity and security.

### Developer Experience

*   **Package Installation:** Installable via pip for easy integration into existing projects.
*   **Docker Support:** Ready-to-use Docker configuration for containerized deployments.
*   **Comprehensive Error Handling:** Graceful error pages with detailed debugging information in development mode.
*   **API Documentation:** Built-in endpoint discovery through `/api/routes`.
*   **Server Statistics:** Monitor server performance with `/api/stats`.
*   **Extensible Architecture:** Modular design that's easy to extend with custom functionality.

## API Endpoints

*   `GET /api/users`: Returns a sample list of user data (protected).
*   `GET /api/routes`: Lists all registered API routes on the server.
*   `GET /api/stats`: Provides server uptime and total request count.
*   `GET /api/logs`: Accesses server logs (development mode only).
*   `POST /api/echo`: Demonstrates JSON input validation by echoing back a validated JSON payload.
*   `POST /api/login`: JWT authentication endpoint.
*   `POST /api/encrypt`: Encrypts data with end-to-end encryption.
*   `POST /api/decrypt`: Decrypts data with end-to-end encryption.
*   `POST /api/dp/count`: Differentially private count of items.
*   `POST /api/dp/mean`: Differentially private mean calculation.
*   `POST /api/encrypt`: Encrypts data with end-to-end encryption.
*   `POST /api/decrypt`: Decrypts data with end-to-end encryption.
*   `POST /api/dp/count`: Differentially private count of items.
*   `POST /api/dp/mean`: Differentially private mean calculation.

## Quick Start

### Using pip (Recommended)

```bash
# Install the package
pip install nexus-http-server

# Run the server
nexus-server
```

### From Source

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kennethkabogo/nexus-http-server.git
    cd nexus-http-server
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Build the React frontend:**
    ```bash
    cd frontend
    npm install
    npm run build
    cd ..
    ```

4.  **Run the server:**
    ```bash
    python main.py
    ```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t nexus-server .
docker run -p 8000:8000 nexus-server
```

## Usage

*   Access the React frontend by navigating to `http://localhost:8000` in your web browser.
*   Interact with the API endpoints using tools like `curl` or Postman, or through the frontend application.

Example API calls:
```bash
# Get server statistics
curl http://localhost:8000/api/stats

# Login to get a JWT token
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword"}'

# Use the token to access protected endpoints
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/api/users
```

## Development

### Running Tests

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

### Linting

```bash
# Run code linting
make lint
```

### Documentation

Full documentation is available in the [docs](docs/) directory.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Kenneth Kabogo](https://github.com/kennethkabogo) - Initial work

## Acknowledgments

*   Built with Python's standard library for maximum portability
*   React frontend for modern user interfaces
*   Security features inspired by OWASP best practices
