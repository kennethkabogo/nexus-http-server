# Custom API Endpoint Example

This example shows how to create a custom API endpoint with the Gemini HTTP Server.

## Creating a New Endpoint

To add a new API endpoint, you can use the `@route` decorator:

```python
from gemini_server import route, json_response

@route('/api/custom')
def custom_endpoint(request):
    # Your custom logic here
    data = {
        'message': 'Hello from custom endpoint',
        'method': request.method,
        'timestamp': time.time()
    }
    return json_response(data)
```

## Adding Authentication

To protect your endpoint with JWT authentication:

```python
from gemini_server import route, json_response, require_auth

@route('/api/protected')
@require_auth
def protected_endpoint(request):
    # This endpoint requires authentication
    user = request.user  # JWT payload
    data = {
        'message': f'Hello, {user["username"]}!',
        'user_id': user['user_id']
    }
    return json_response(data)
```

## Adding Input Validation

To validate JSON input:

```python
from gemini_server import route, json_response, validate_json

@route('/api/data')
@validate_json({
    'name': {'type': 'string', 'required': True},
    'age': {'type': 'integer', 'min': 0, 'max': 150},
    'email': {'type': 'string', 'regex': r'^[^@]+@[^@]+\.[^@]+$'}
})
def data_endpoint(request):
    # The request data is automatically validated
    name = request.data['name']
    age = request.data['age']
    email = request.data['email']
    
    # Process the data
    result = process_user_data(name, age, email)
    
    return json_response({'result': result})
```

## Adding Middleware

To add custom middleware:

```python
from gemini_server import middleware

@middleware
def custom_middleware(handler):
    def middleware_handler(request):
        # Pre-processing
        print(f"Processing request to {request.path}")
        
        # Call the next handler
        response = handler(request)
        
        # Post-processing
        response.headers.append(('X-Custom-Header', 'CustomValue'))
        
        return response
    return middleware_handler
```

## Complete Example

Here's a complete example that combines all features:

```python
import time
from gemini_server import route, json_response, require_auth, validate_json, middleware

# Custom middleware
@middleware
def timing_middleware(handler):
    def middleware_handler(request):
        start_time = time.time()
        response = handler(request)
        duration = time.time() - start_time
        response.headers.append(('X-Response-Time', f'{duration:.3f}s'))
        return response
    return middleware_handler

# Custom endpoint with authentication and validation
@route('/api/profile')
@require_auth
@validate_json({
    'first_name': {'type': 'string', 'required': True, 'maxlength': 50},
    'last_name': {'type': 'string', 'required': True, 'maxlength': 50},
    'bio': {'type': 'string', 'maxlength': 500}
})
def update_profile(request):
    user = request.user
    data = request.data
    
    # In a real application, you would save this to a database
    profile = {
        'user_id': user['user_id'],
        'username': user['username'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'bio': data.get('bio', ''),
        'updated_at': time.time()
    }
    
    return json_response({
        'message': 'Profile updated successfully',
        'profile': profile
    })
```

To use this example, save it as `custom_api.py` and import it in your main application file.