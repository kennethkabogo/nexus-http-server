from ..server import Response
import jwt


def authentication_middleware(handler):
    def middleware_handler(request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                from ..server import SECRET_KEY
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                request.user = payload
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                request.user = None
        else:
            request.user = None
        return handler(request)
    return middleware_handler