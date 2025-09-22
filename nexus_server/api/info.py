from ..server import json_response, render_template
import time
from ..server import routes, start_time, request_count


def get_routes(request):
    routes_list = []
    for path, handler in routes.items():
        # Exclude the get_routes function itself
        if handler.__name__ != 'get_routes':
            routes_list.append({
                'path': path,
                'handler': handler.__name__
            })
    return json_response({'routes': routes_list})


def get_stats(request):
    uptime = time.time() - start_time
    stats = {
        'uptime': uptime,
        'request_count': request_count
    }
    return json_response(stats)


def get_logs(request):
    from ..server import DEV_MODE
    if DEV_MODE:
        with open('server.log', 'r') as f:
            logs = f.read()
        return json_response({'logs': logs})
    else:
        return json_response({'message': 'Log access is restricted in production mode.'}, status='403 Forbidden')