import secrets
import uuid


def generate_secure_token(length=32):
    """
    Generates a cryptographically secure random token.
    """
    return secrets.token_urlsafe(length)


def generate_correlation_id():
    """
    Generates a unique correlation ID for requests.
    """
    return str(uuid.uuid4())[:8]