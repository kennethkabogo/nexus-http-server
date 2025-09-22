from ..server import Response, sanitize_recursive, is_suspicious, log_security_event


def security_monitoring_middleware(handler):
    def middleware_handler(request):
        if request.data:
            request.data = sanitize_recursive(request.data)
        if request.query_params:
            request.query_params = sanitize_recursive(request.query_params)
            
        if is_suspicious(request):
            log_security_event("Intrusion Attempt", f"Suspicious request from {request.environ.get('REMOTE_ADDR')} to {request.path}", severity='high')
            return Response('Bad Request', '400 Bad Request')  # Or 403 Forbidden
        return handler(request)
    return middleware_handler