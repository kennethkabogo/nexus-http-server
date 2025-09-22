from ..server import Response, render_template, DEV_MODE
import traceback
import logging


def error_middleware(handler):
    def middleware_handler(request):
        try:
            return handler(request)
        except Exception as e:
            logging.error("Internal Server Error: %s", e, exc_info=True)
            error_message = render_template('500.html')
            if DEV_MODE:
                error_message += f"<pre>{traceback.format_exc()}</pre>"
            return Response(error_message, '500 Internal Server Error')
    return middleware_handler