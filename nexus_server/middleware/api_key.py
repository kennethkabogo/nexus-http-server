import os
import secrets
from ..server import middleware
from ..utils import json_response

# In a production environment, you would store this in a database or secure configuration
# For demonstration purposes, we're using an environment variable
VALID_API_KEYS = set()

# Load initial API keys from environment variable
api_keys_env = os.environ.get('NEXUS_API_KEYS', '')
if api_keys_env:
    VALID_API_KEYS.update(api_keys_env.split(','))

def generate_api_key():
    """Generate a new API key"""
    return secrets.token_urlsafe(32)

def add_api_key(api_key):
    """Add a new API key to the valid set"""
    VALID_API_KEYS.add(api_key)

def remove_api_key(api_key):
    """Remove an API key from the valid set"""
    VALID_API_KEYS.discard(api_key)

@middleware
def api_key_middleware(handler):
    """
    Middleware to check for API key authentication.
    Looks for X-API-Key header or api_key query parameter.
    """
    def middleware_handler(request):
        # Check for API key in header
        api_key = request.headers.get('X-Api-Key')
        
        # If not in header, check query parameters
        if not api_key and request.query_params:
            api_key = request.query_params.get('api_key', [None])[0]
        
        # If we have an API key, validate it
        if api_key:
            if api_key in VALID_API_KEYS:
                request.api_key_authenticated = True
                request.api_key = api_key
            else:
                return json_response({'error': 'Invalid API key'}, status='401 Unauthorized')
        else:
            request.api_key_authenticated = False
            
        return handler(request)
    return middleware_handler

# API endpoint to manage API keys
def create_api_key_handler(request):
    """Create a new API key"""
    # This endpoint should be protected by admin authentication
    new_key = generate_api_key()
    add_api_key(new_key)
    return json_response({'api_key': new_key})

def revoke_api_key_handler(request):
    """Revoke an API key"""
    # This endpoint should be protected by admin authentication
    api_key = request.data.get('api_key') if request.data else None
    if not api_key:
        return json_response({'error': 'Missing api_key parameter'}, status='400 Bad Request')
    
    remove_api_key(api_key)
    return json_response({'message': 'API key revoked'})