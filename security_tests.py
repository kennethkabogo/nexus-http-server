import requests
import time

def get_auth_token():
    """Logs in and returns an authentication token."""
    try:
        resp = requests.post('http://localhost:8000/api/login', json={'username': 'testuser', 'password': 'testpassword'})
        resp.raise_for_status()
        return resp.json().get('token')
    except requests.exceptions.RequestException as e:
        print(f"Failed to get auth token: {e}")
        return None

def test_rate_limiting(token):
    """Tests rate limiting for both authenticated and unauthenticated requests."""
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    # Hammer the server with 150 requests
    for i in range(150):
        try:
            resp = requests.get('http://localhost:8000/api/users', headers=headers, timeout=2)
            if resp.status_code == 429:
                print(f"Rate limiting kicked in at request {i} for {'authenticated' if token else 'unauthenticated'} user.")
                return  # Exit after rate limit is hit
            # Add a small delay to avoid overwhelming the server too quickly
            time.sleep(0.05)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
    print("Rate limiting test completed without hitting the limit.")

def test_xss_detection():
    """Tests for XSS vulnerabilities by sending malicious payloads."""
    payloads = [
        '<script>alert(1)</script>',
        'javascript:alert(1)',
        '<img src=x onerror=alert(1)>'
    ]
    for payload in payloads:
        try:
            # The endpoint expects 'message' and 'count'
            resp = requests.post('http://localhost:8000/api/echo', json={'message': payload, 'count': 1})
            print(f"XSS test with payload '{payload}': {resp.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"XSS test failed for payload '{payload}': {e}")

def test_sql_injection():
    """Tests for SQL injection vulnerabilities."""
    payloads = [
        "'; DROP TABLE users; --",
        "1' UNION SELECT * FROM users--",
        "admin'/**/OR/**/1=1#"
    ]
    for payload in payloads:
        try:
            # The endpoint expects 'message' and 'count'
            resp = requests.post('http://localhost:8000/api/echo', json={'message': payload, 'count': 1})
            print(f"SQL injection test with payload '{payload}': {resp.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"SQL injection test failed for payload '{payload}': {e}")

if __name__ == "__main__":
    auth_token = get_auth_token()

    print("--- Testing Rate Limiting (Unauthenticated) ---")
    test_rate_limiting(None)
    time.sleep(1) # Pause between tests

    if auth_token:
        print("\n--- Testing Rate Limiting (Authenticated) ---")
        test_rate_limiting(auth_token)
        time.sleep(1)

    print("\n--- Testing XSS Detection ---")
    test_xss_detection()
    time.sleep(1)

    print("\n--- Testing SQL Injection ---")
    test_sql_injection()