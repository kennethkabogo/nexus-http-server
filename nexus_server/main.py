#!/usr/bin/env python3
"""
Main entry point for the Nexus HTTP Server.
"""
import os
import logging
import sys
from wsgiref.simple_server import make_server

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .server import create_app, setup_routes
from .middleware import (
    error_middleware, authentication_middleware, security_headers_middleware,
    rate_limit_middleware, security_monitoring_middleware, simple_middleware
)
from .security import (
    add_encryption_routes, add_differential_privacy_routes, add_zero_knowledge_routes,
    add_privacy_budget_routes, add_data_expiration_routes, add_federated_learning_routes,
    add_decentralized_identity_routes, add_homomorphic_encryption_routes, add_ai_privacy_routes,
    add_ai_privacy_middleware
)

# Setup logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Main entry point for the Nexus HTTP Server."""
    # Setup routes
    setup_routes()
    
    # Add security routes
    add_encryption_routes()
    add_differential_privacy_routes()
    add_zero_knowledge_routes()
    add_privacy_budget_routes()
    add_data_expiration_routes()
    add_federated_learning_routes()
    add_decentralized_identity_routes()
    add_homomorphic_encryption_routes()
    add_ai_privacy_routes()
    
    # Setup middleware chain
    # The error middleware should be the first one to catch all errors
    all_middlewares = [
        error_middleware,
        authentication_middleware,
        security_headers_middleware,
        rate_limit_middleware,
        security_monitoring_middleware,
        add_ai_privacy_middleware,  # Add AI privacy middleware
        simple_middleware,
    ]
    
    # Import routes from server
    from .server import routes
    
    # Create the WSGI application
    app = create_app(routes_dict=routes, middlewares_list=all_middlewares)
    
    # Get port from environment or default to 8000
    port = int(os.environ.get('PORT', 8000))
    
    # Create and start the server
    httpd = make_server('', port, app)
    logging.info("Starting Nexus HTTP Server on port %s", port)
    print(f"Nexus HTTP Server running on http://localhost:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    main()