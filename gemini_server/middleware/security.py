def security_headers_middleware(handler):
    def middleware_handler(request):
        response = handler(request)
        # Add security headers
        response.headers.append(('X-Content-Type-Options', 'nosniff'))
        response.headers.append(('X-Frame-Options', 'DENY'))
        response.headers.append(('X-XSS-Protection', '1; mode=block'))
        response.headers.append(('Referrer-Policy', 'no-referrer-when-downgrade'))
        # Consider Content-Security-Policy (CSP) - more complex, might need to be dynamic
        # response.headers.append(('Content-Security-Policy', "default-src 'self'"))
        return response
    return middleware_handler