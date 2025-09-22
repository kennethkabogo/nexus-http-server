from ..server import logging


def simple_middleware(handler):
    def middleware_handler(request):
        logging.info(f"Middleware: Processing request for {request.path}")
        response = handler(request)
        # Example: Add a custom header
        response.headers.append(('X-Custom-Header', 'Processed-by-Middleware'))
        return response
    return middleware_handler