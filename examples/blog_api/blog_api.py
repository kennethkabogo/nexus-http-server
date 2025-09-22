from nexus_server.server import route, require_auth
from nexus_server.utils import json_response, validate_json
from datetime import datetime

# Simple in-memory storage for blog posts
# In a real application, you would use a database
posts = {}
next_id = 1

# Validation schema for blog posts
POST_SCHEMA = {
    'title': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 200},
    'content': {'type': 'string', 'required': True, 'minlength': 1}
}

def get_post(post_id):
    """Get a post by ID"""
    return posts.get(post_id)

def create_post(title, content, author):
    """Create a new post"""
    global next_id
    post_id = next_id
    next_id += 1
    
    post = {
        'id': post_id,
        'title': title,
        'content': content,
        'author': author,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    posts[post_id] = post
    return post

def update_post(post_id, title, content):
    """Update an existing post"""
    if post_id not in posts:
        return None
        
    post = posts[post_id]
    post['title'] = title
    post['content'] = content
    post['updated_at'] = datetime.now().isoformat()
    
    return post

def delete_post(post_id):
    """Delete a post"""
    return posts.pop(post_id, None)

@route('/api/posts')
def get_posts(request):
    """Get all blog posts"""
    # Return posts as a list, sorted by creation date (newest first)
    posts_list = list(posts.values())
    posts_list.sort(key=lambda x: x['created_at'], reverse=True)
    return json_response({'posts': posts_list})

@route('/api/posts/<int:post_id>')
def get_post_by_id(request, post_id):
    """Get a specific blog post"""
    post = get_post(post_id)
    if not post:
        return json_response({'error': 'Post not found'}, status='404 Not Found')
    return json_response({'post': post})

@route('/api/posts')
@require_auth
@validate_json(POST_SCHEMA)
def create_post_handler(request):
    """Create a new blog post"""
    title = request.data['title']
    content = request.data['content']
    author = request.user.get('username', 'Anonymous')
    
    post = create_post(title, content, author)
    return json_response({'post': post, 'message': 'Post created successfully'})

@route('/api/posts/<int:post_id>')
@require_auth
@validate_json(POST_SCHEMA)
def update_post_handler(request, post_id):
    """Update an existing blog post"""
    # Check if post exists
    if post_id not in posts:
        return json_response({'error': 'Post not found'}, status='404 Not Found')
    
    # Check if user is authorized to update this post
    # In a real application, you would check ownership or permissions
    title = request.data['title']
    content = request.data['content']
    
    post = update_post(post_id, title, content)
    return json_response({'post': post, 'message': 'Post updated successfully'})

@route('/api/posts/<int:post_id>')
@require_auth
def delete_post_handler(request, post_id):
    """Delete a blog post"""
    # Check if post exists
    if post_id not in posts:
        return json_response({'error': 'Post not found'}, status='404 Not Found')
    
    # Check if user is authorized to delete this post
    # In a real application, you would check ownership or permissions
    
    deleted_post = delete_post(post_id)
    return json_response({'post': deleted_post, 'message': 'Post deleted successfully'})

# Add a few sample posts for demonstration
create_post("Welcome to Nexus Blog", "This is a sample blog post to demonstrate the Nexus HTTP Server.", "Admin")
create_post("Getting Started with Nexus", "Learn how to build powerful web applications with Nexus HTTP Server.", "Admin")