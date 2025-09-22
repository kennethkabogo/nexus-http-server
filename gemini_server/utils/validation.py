from cerberus import Validator
from .responses import json_response


def validate_json(schema):
    def decorator(func):
        def wrapper(request):
            if not request.data:
                return json_response({'error': 'Request body is empty'}, status='400 Bad Request')
            
            v = Validator(schema)
            if not v.validate(request.data):
                return json_response({'error': v.errors}, status='400 Bad Request')
            
            return func(request)
        return wrapper
    return decorator