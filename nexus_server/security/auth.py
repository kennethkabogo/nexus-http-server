from ..server import json_response


def require_auth(func):
    """
    Decorator to protect API endpoints with JWT authentication.
    Assumes that the authentication_middleware has already run.
    """
    def wrapper(request):
        if not hasattr(request, 'user') or not request.user:
            return json_response({'message': 'Authentication required'}, status='401 Unauthorized')
        return func(request)
    return wrapper