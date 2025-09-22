import re
import bleach
from .constants import SUSPICIOUS_PATTERNS, PII_PATTERNS, SENSITIVE_HEADERS


def sanitize_recursive(data):
    """
    Recursively sanitizes data to prevent XSS, SQL injection, and path traversal.
    Uses bleach for HTML sanitization and basic string cleaning.
    """
    if isinstance(data, dict):
        return {k: sanitize_recursive(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_recursive(item) for item in data]
    elif isinstance(data, str):
        # Sanitize HTML content (XSS prevention)
        sanitized_string = bleach.clean(data, tags=[], attributes={}, strip=True)
        # Basic path traversal prevention
        sanitized_string = sanitized_string.replace('../', '').replace('..\\', '')
        # Aggressive sanitization for suspicious patterns
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern.search(sanitized_string.lower()):
                return ""  # Return empty string if suspicious pattern is found
        return sanitized_string
    else:
        return data


def sanitize_for_logging(data):
    """
    Redacts sensitive information from data structures for logging purposes.
    Handles dictionaries and strings.
    """
    if isinstance(data, dict):
        sanitized_data = {}
        for key, value in data.items():
            if key.lower() in SENSITIVE_HEADERS:
                sanitized_data[key] = '[REDACTED]'
            else:
                sanitized_data[key] = sanitize_for_logging(value)  # Recurse for nested dicts
        return sanitized_data
    elif isinstance(data, str):
        sanitized_string = data
        for pattern in PII_PATTERNS:
            sanitized_string = pattern.sub('[REDACTED_PII]', sanitized_string)
        return sanitized_string
    else:
        return data  # Return as is for other types (int, bool, etc.)


def is_suspicious(request):
    """
    Checks if a request contains suspicious patterns indicative of an attack.
    """
    request_content = f"{request.path} {request.query_params} {request.data} {request.headers}"
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.search(request_content.lower()):
            return True
    return False