from ..server import Response, request_tracker_user, request_tracker_ip
import time


def rate_limit_middleware(handler):
    def middleware_handler(request):
        now = time.time()
        
        if hasattr(request, 'user') and request.user:
            user_id = request.user.get('user_id')
            # Clean old requests
            request_tracker_user[user_id] = [req_time for req_time in request_tracker_user[user_id]
                                             if now - req_time < 3600]  # 1 hour window
            if len(request_tracker_user[user_id]) >= 1000:  # Increased limit
                return Response('Rate limit exceeded for user', '429 Too Many Requests')
            request_tracker_user[user_id].append(now)
        else:
            ip = request.environ.get('REMOTE_ADDR')
            # Clean old requests
            request_tracker_ip[ip] = [req_time for req_time in request_tracker_ip[ip]
                                      if now - req_time < 3600]  # 1 hour window
            if len(request_tracker_ip[ip]) >= 1000:  # Increased limit
                return Response('Rate limit exceeded for IP', '429 Too Many Requests')
            request_tracker_ip[ip].append(now)
            
        return handler(request)
    return middleware_handler