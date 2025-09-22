"""
Configuration module for the Gemini HTTP Server.
"""
import os
import secrets

class Config:
    """Base configuration class."""
    
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    DEV_MODE = os.environ.get('DEV_MODE', 'False').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8000))
    MAX_REQUEST_SIZE = int(os.environ.get('MAX_REQUEST_SIZE', 1024 * 1024))  # 1MB default
    
    # Rate limiting settings
    RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW', 3600))  # 1 hour
    RATE_LIMIT_REQUESTS_IP = int(os.environ.get('RATE_LIMIT_REQUESTS_IP', 1000))
    RATE_LIMIT_REQUESTS_USER = int(os.environ.get('RATE_LIMIT_REQUESTS_USER', 1000))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    SECURITY_LOG_LEVEL = os.environ.get('SECURITY_LOG_LEVEL', 'WARNING')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEV_MODE = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEV_MODE = False
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEV_MODE = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}