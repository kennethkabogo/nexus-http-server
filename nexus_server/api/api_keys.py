from ..server import route, require_auth
from ..utils import json_response, validate_json
from ..middleware.api_key import create_api_key_handler, revoke_api_key_handler

@route('/api/admin/api-keys')
@require_auth  # Only authenticated admin users can manage API keys
@validate_json({'action': {'type': 'string', 'required': True}})
def manage_api_keys(request):
    """Manage API keys (create, revoke)"""
    action = request.data.get('action')
    
    if action == 'create':
        return create_api_key_handler(request)
    elif action == 'revoke':
        return revoke_api_key_handler(request)
    else:
        return json_response({'error': 'Invalid action. Use "create" or "revoke"'}, status='400 Bad Request')