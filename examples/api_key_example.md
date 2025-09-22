# Nexus HTTP Server Examples

This directory contains example applications demonstrating various features of the Nexus HTTP Server.

## API Key Authentication Example

This example shows how to use API key authentication with the Nexus HTTP Server.

### Setup

1. Start the server:
   ```bash
   python main.py
   ```

2. Create an API key (requires admin authentication):
   ```bash
   curl -X POST http://localhost:8000/api/admin/api-keys \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"action": "create"}'
   ```

3. Use the API key to access protected endpoints:
   ```bash
   # Using header
   curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8000/api/some-protected-endpoint
   
   # Using query parameter
   curl http://localhost:8000/api/some-protected-endpoint?api_key=YOUR_API_KEY
   ```

### Environment Setup

To use API keys, set the NEXUS_API_KEYS environment variable with comma-separated keys:
```bash
export NEXUS_API_KEYS="key1,key2,key3"
```

### Code Implementation

In your route handlers, you can check for API key authentication:
```python
from nexus_server.server import route

@route('/api/protected-endpoint')
def protected_handler(request):
    if not request.api_key_authenticated:
        return json_response({'error': 'API key required'}, status='401 Unauthorized')
    
    # Your protected endpoint logic here
    return json_response({'message': 'Access granted with API key'})
```