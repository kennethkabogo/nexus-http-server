# Nexus HTTP Server Example Application

This example demonstrates how to create a simple blog API using the Nexus HTTP Server.

## Features Demonstrated

1. Custom API endpoints
2. Data validation
3. JWT authentication
4. Database integration (using a simple in-memory store)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python main.py
   ```

3. Test the API endpoints (see below)

## API Endpoints

### Public Endpoints

- `GET /api/posts` - Get all blog posts
- `GET /api/posts/{id}` - Get a specific blog post

### Protected Endpoints

- `POST /api/posts` - Create a new blog post (requires authentication)
- `PUT /api/posts/{id}` - Update a blog post (requires authentication)
- `DELETE /api/posts/{id}` - Delete a blog post (requires authentication)

## Example Usage

### Get all posts
```bash
curl http://localhost:8000/api/posts
```

### Create a new post (requires authentication)
```bash
# First, get a JWT token
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword"}'

# Use the token to create a post
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "My First Post", "content": "This is the content of my first post."}'
```

## Implementation

The example implements a simple blog API with the following components:

1. **Data Model**: A simple in-memory storage for blog posts
2. **API Routes**: Endpoints for CRUD operations on blog posts
3. **Validation**: Input validation for post data
4. **Authentication**: JWT-based authentication for protected endpoints

## Extending the Example

To extend this example:

1. Add more complex data models
2. Implement database persistence
3. Add more sophisticated validation
4. Implement additional security measures
5. Add pagination for large datasets