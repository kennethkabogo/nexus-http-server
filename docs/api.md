# Nexus HTTP Server API Documentation

## Overview

The Nexus HTTP Server provides a RESTful API for interacting with the server's functionality. All API endpoints are prefixed with `/api/`.

## Authentication

Most API endpoints require authentication. The server supports two authentication methods:

1. **JWT Token Authentication**: Include the token in the `Authorization` header:
   ```
   Authorization: Bearer YOUR_JWT_TOKEN
   ```

2. **API Key Authentication**: Include the API key in the `X-API-Key` header or as a query parameter:
   ```
   X-API-Key: YOUR_API_KEY
   ```
   or
   ```
   GET /api/endpoint?api_key=YOUR_API_KEY
   ```

## API Endpoints

### User Authentication

#### POST /api/login
Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string"
}
```

### User Management

#### GET /api/users
Get a list of users (requires authentication).

**Response:**
```json
{
  "users": [
    {
      "id": "integer",
      "name": "string"
    }
  ],
  "authenticated_user": "object"
}
```

### System Information

#### GET /api/routes
Get a list of all registered API routes.

**Response:**
```json
{
  "routes": [
    {
      "path": "string",
      "handler": "string"
    }
  ]
}
```

#### GET /api/stats
Get server statistics.

**Response:**
```json
{
  "uptime": "number",
  "request_count": "integer"
}
```

#### GET /api/logs
Get server logs (development mode only).

**Response:**
```json
{
  "logs": "string"
}
```

### Data Validation

#### POST /api/echo
Echo back validated JSON data.

**Request Body:**
```json
{
  "message": "string",
  "count": "integer"
}
```

**Response:**
```json
{
  "received_data": "object"
}
```

### API Key Management

#### POST /api/admin/api-keys
Manage API keys (requires admin authentication).

**Request Body:**
```json
{
  "action": "string" // "create" or "revoke"
  // For revoke action:
  // "api_key": "string"
}
```

**Response (create):**
```json
{
  "api_key": "string"
}
```

**Response (revoke):**
```json
{
  "message": "string"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "error": "string"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Rate Limiting

The server implements rate limiting to prevent abuse:
- 1000 requests per hour per IP address
- 1000 requests per hour per authenticated user

Exceeding these limits will result in a 429 Too Many Requests response.

## Security Features

The server includes several built-in security features:
- Input sanitization to prevent XSS, SQL injection, and path traversal
- PII redaction in logs
- Intrusion detection for common attack patterns
- Security headers in all responses
- Restricted log access in production mode

## Examples

### Authentication
```bash
# Login to get a JWT token
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword"}'

# Use the token to access protected endpoints
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/api/users
```

### API Key Usage
```bash
# Using header
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8000/api/some-protected-endpoint

# Using query parameter
curl http://localhost:8000/api/some-protected-endpoint?api_key=YOUR_API_KEY
```

### Data Validation
```bash
# Valid request
curl -X POST http://localhost:8000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!", "count": 5}'

# Invalid request (missing required fields)
curl -X POST http://localhost:8000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!"}'  # Missing 'count'
```