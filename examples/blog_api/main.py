#!/usr/bin/env python3
"""
Example Blog API using Nexus HTTP Server
"""

import os
import sys

# Add the parent directory to Python path to import nexus_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_server.server import setup_routes
from nexus_server.main import main
from nexus_server.server import routes
from nexus_server.utils import json_response
from examples.blog_api.blog_api import (
    get_posts, get_post_by_id, create_post_handler,
    update_post_handler, delete_post_handler
)

# Import route decorator
from nexus_server.server import route

def setup_blog_routes():
    """Setup blog API routes"""
    # Register the blog API routes
    routes['/api/posts'] = get_posts
    routes['/api/posts/<int:post_id>'] = get_post_by_id
    
    # For POST, PUT, DELETE we need to handle method routing differently
    # This is a simplified approach - in a real application you might want
    # to implement proper method routing in the server

if __name__ == '__main__':
    # Setup the blog routes
    setup_blog_routes()
    
    # Run the main server
    main()