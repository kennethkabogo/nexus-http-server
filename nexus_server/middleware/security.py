def security_headers_middleware(handler):
    def middleware_handler(request):
        response = handler(request)
        # Add comprehensive security headers
        response.headers.append(('X-Content-Type-Options', 'nosniff'))
        response.headers.append(('X-Frame-Options', 'DENY'))
        response.headers.append(('X-XSS-Protection', '1; mode=block'))
        response.headers.append(('Referrer-Policy', 'no-referrer-when-downgrade'))
        
        # Enhanced security headers
        response.headers.append(('X-Permitted-Cross-Domain-Policies', 'none'))
        response.headers.append(('Clear-Site-Data', '"cache" "cookies" "storage"'))
        response.headers.append(('Cross-Origin-Embedder-Policy', 'require-corp'))
        response.headers.append(('Cross-Origin-Opener-Policy', 'same-origin'))
        response.headers.append(('Cross-Origin-Resource-Policy', 'same-origin'))
        
        # Content Security Policy (adjust based on your frontend requirements)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "child-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers.append(('Content-Security-Policy', csp))
        
        # Strict Transport Security (only if served over HTTPS in production)
        # Uncomment the following line when deploying with HTTPS
        # response.headers.append(('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload'))
        
        return response
    return middleware_handler