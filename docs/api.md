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

### Privacy-Preserving Endpoints

#### POST /api/encrypt
Encrypt data with end-to-end encryption.

**Request Body:**
```json
{
  "data": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "encrypted_data": "string",
  "salt": "string"
}
```

#### POST /api/decrypt
Decrypt data with end-to-end encryption.

**Request Body:**
```json
{
  "encrypted_data": "string",
  "salt": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "decrypted_data": "string"
}
```

#### POST /api/dp/count
Get a differentially private count of items.

**Request Body:**
```json
{
  "values": "array",
  "epsilon": "number"
}
```

**Response:**
```json
{
  "noisy_count": "number",
  "epsilon": "number"
}
```

#### POST /api/dp/mean
Get a differentially private mean of values.

**Request Body:**
```json
{
  "values": "array of numbers",
  "epsilon": "number"
}
```

**Response:**
```json
{
  "noisy_mean": "number",
  "epsilon": "number"
}
```

### Decentralized Identity Endpoints

#### GET /api/did/generate
Generate a new DID key pair for self-sovereign identity.

**Response:**
```json
{
  "message": "string",
  "did": "string",
  "public_key": "string",
  "instructions": "string"
}
```

#### POST /api/did/document
Create a DID document.

**Request Body:**
```json
{
  "did": "string",
  "public_key": "string"
}
```

**Response:**
```json
{
  "message": "string",
  "did_document": "object"
}
```

#### POST /api/did/credential/issue
Issue a verifiable credential.

**Request Body:**
```json
{
  "issuer_did": "string",
  "subject_did": "string",
  "claims": "object",
  "expiration_days": "integer"
}
```

**Response:**
```json
{
  "message": "string",
  "credential": "object"
}
```

#### POST /api/did/credential/verify
Verify a verifiable credential.

**Request Body:**
```json
{
  "credential": "object"
}
```

**Response:**
```json
{
  "verification_result": "object"
}
```

#### GET /api/did/document/<did>
Get a DID document.

**Response:**
```json
{
  "did_document": "object"
}
```

### Homomorphic Encryption Endpoints

#### GET /api/he/generate-keys
Generate homomorphic encryption keys.

**Response:**
```json
{
  "message": "string",
  "public_key": "string",
  "instructions": "string"
}
```

#### POST /api/he/encrypt/int
Encrypt an integer value.

**Request Body:**
```json
{
  "value": "integer",
  "public_key": "string"
}
```

**Response:**
```json
{
  "message": "string",
  "encrypted_value": "object"
}
```

#### POST /api/he/encrypt/float
Encrypt a float value.

**Request Body:**
```json
{
  "value": "float",
  "public_key": "string"
}
```

**Response:**
```json
{
  "message": "string",
  "encrypted_value": "object"
}
```

#### POST /api/he/decrypt
Decrypt a homomorphically encrypted value.

**Request Body:**
```json
{
  "encrypted_value": "object",
  "private_key": "string"
}
```

**Response:**
```json
{
  "message": "string",
  "decrypted_value": "number"
}
```

#### POST /api/he/add
Perform homomorphic addition on two encrypted values.

**Request Body:**
```json
{
  "encrypted_a": "object",
  "encrypted_b": "object"
}
```

**Response:**
```json
{
  "message": "string",
  "result": "object"
}
```

#### POST /api/he/multiply
Perform homomorphic multiplication of an encrypted value by a scalar.

**Request Body:**
```json
{
  "encrypted_value": "object",
  "scalar": "number"
}
```

**Response:**
```json
{
  "message": "string",
  "result": "object"
}
```

### AI Privacy Endpoints

#### POST /api/ai/opt-out
Set AI training data opt-out preference.

**Request Body:**
```json
{
  "opt_out": "boolean"
}
```

**Response:**
```json
{
  "message": "string",
  "opt_out": "boolean",
  "timestamp": "number"
}
```

#### GET /api/ai/opt-out/status
Get AI training data opt-out status.

**Response:**
```json
{
  "user_id": "string",
  "opt_out": "boolean",
  "set_at": "number",
  "status": "string"
}
```

#### POST /api/ai/training-job
Start an AI model training job with privacy controls.

**Request Body:**
```json
{
  "job_id": "string",
  "model_type": "string",
  "data_sources": "array"
}
```

**Response:**
```json
{
  "message": "string",
  "job_info": "object"
}
```

#### GET /api/ai/training-jobs
Get information about all AI training jobs.

**Response:**
```json
{
  "training_jobs": "object"
}
```

#### GET /api/ai/privacy-report
Get AI privacy report for the authenticated user.

**Response:**
```json
{
  "user_id": "string",
  "opt_out_status": "object",
  "ai_interactions": "object",
  "protection_status": "string",
  "report_generated_at": "number"
}
```

### Privacy Budget Management Endpoints

#### GET /api/privacy/budget
Get current privacy budget status for the authenticated user.

**Response:**
```json
{
  "total_epsilon": "number",
  "consumed_epsilon": "number",
  "remaining_epsilon": "number",
  "usage_percentage": "number",
  "queries": "array",
  "created_at": "timestamp"
}
```

#### GET /api/privacy/budget/history
Get privacy budget usage history for the authenticated user.

**Response:**
```json
{
  "history": "array"
}
```

#### POST /api/privacy/budget/suggest
Get suggestions for epsilon values based on remaining budget.

**Request Body:**
```json
{
  "sensitivity": "number" // Optional, default: 1.0
}
```

**Response:**
```json
{
  "suggestions": {
    "conservative": "number",
    "moderate": "number",
    "liberal": "number"
  },
  "remaining_budget": "number",
  "explanation": "string"
}
```

#### POST /api/privacy/budget/reset
Reset privacy budget for the authenticated user.

**Response:**
```json
{
  "message": "string",
  "status": "string"
}
```

#### POST /api/privacy/budget/consume
Manually consume a portion of the privacy budget.

**Request Body:**
```json
{
  "epsilon": "number",
  "query_type": "string"
}
```

**Response (success):**
```json
{
  "message": "string",
  "remaining_budget": "number",
  "status": "string"
}
```

**Response (insufficient budget):**
```json
{
  "error": "string",
  "requested": "number",
  "available": "number",
  "total": "number"
}
```

### Data Expiration Endpoints

#### GET /api/data/expiration
Get information about all expiring data items.

**Response:**
```json
{
  "expiring_data": "object"
}
```

#### GET /api/data/expiration/<data_id>
Get expiration information for a specific data item.

**Response:**
```json
{
  "created_at": "timestamp",
  "expires_at": "timestamp",
  "ttl_seconds": "number",
  "time_remaining": "number",
  "is_expired": "boolean"
}
```

#### POST /api/data/expiration/<data_id>/cancel
Cancel expiration for a data item.

**Response:**
```json
{
  "message": "string",
  "status": "string"
}
```

#### POST /api/data/expiration/<data_id>/extend
Extend expiration time for a data item.

**Request Body:**
```json
{
  "additional_seconds": "integer"
}
```

**Response:**
```json
{
  "message": "string",
  "expiration_info": "object",
  "status": "string"
}
```

### Federated Learning Endpoints

#### POST /api/fl/initialize
Initialize the global federated learning model.

**Request Body:**
```json
{
  "model_structure": "object"
}
```

**Response:**
```json
{
  "message": "string",
  "model_structure": "object"
}
```

#### POST /api/fl/start-round
Start a new federated learning round.

**Request Body:**
```json
{
  "round_id": "string"
}
```

**Response:**
```json
{
  "message": "string",
  "round_info": "object"
}
```

#### POST /api/fl/submit-update
Submit a client's model update for a training round.

**Request Body:**
```json
{
  "client_id": "string",
  "round_id": "string",
  "model_update": "object"
}
```

**Response:**
```json
{
  "message": "string",
  "client_id": "string",
  "round_id": "string"
}
```

#### POST /api/fl/aggregate
Aggregate client updates to improve the global model.

**Request Body:**
```json
{
  "round_id": "string",
  "aggregation_method": "string" // Optional, default: "fedavg"
}
```

**Response:**
```json
{
  "message": "string",
  "updated_model": "object",
  "aggregation_method": "string"
}
```

#### POST /api/fl/round-status
Get the status of a federated learning round.

**Request Body:**
```json
{
  "round_id": "string"
}
```

**Response:**
```json
{
  "round_id": "string",
  "status": "object"
}
```

#### GET /api/fl/client-stats
Get statistics about client participation.

**Response:**
```json
{
  "client_statistics": "object"
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