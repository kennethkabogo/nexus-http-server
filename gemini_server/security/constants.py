import re


# Privacy-First Request Parsing Constants
SENSITIVE_HEADERS = ['authorization', 'cookie', 'x-api-key']

# Basic PII patterns: SSN (XXX-XX-XXXX), Email
PII_PATTERNS = [
    re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),  # SSN
    re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')  # Email
]

# Intrusion Detection Patterns
SUSPICIOUS_PATTERNS = [
    re.compile(r'<script[^>]*>.*?</script>'),  # XSS
    re.compile(r'<\w+\s+on\w+.*?>'),  # XSS
    re.compile(r'javascript:'),  # XSS
    re.compile(r'union\s+select', re.IGNORECASE),  # SQL Injection
    re.compile(r'drop\s+table', re.IGNORECASE),  # SQL Injection
    re.compile(r'--'),  # SQL Injection
    re.compile(r'#'),  # SQL Injection
    re.compile(r'/\*.*\*/'),  # SQL Injection
    re.compile(r'\.\./|\\.\\|%2e%2e/|%2e%2e\\'),  # Directory Traversal
    re.compile(r'eval\(.*\)', re.IGNORECASE),  # Code Injection
    re.compile(r'system\(.*\)', re.IGNORECASE),  # Code Injection
    re.compile(r'exec\(.*\)', re.IGNORECASE),  # Code Injection
]