from ..server import json_response, validate_json, log_security_event, SECRET_KEY
import time
import jwt


@validate_json({'username': {'type': 'string'}, 'password': {'type': 'string'}})
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Dummy authentication (replace with actual user lookup and password hashing)
    if username == 'testuser' and password == 'testpassword':
        payload = {
            'user_id': 123,
            'username': username,
            'exp': time.time() + 3600  # Token expires in 1 hour
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return json_response({'token': token})
    else:
        log_security_event("Authentication Failure", f"Failed login attempt for user: {username} from {request.environ.get('REMOTE_ADDR')}", severity='medium')
        return json_response({'message': 'Invalid credentials'}, status='401 Unauthorized')