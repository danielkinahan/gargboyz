import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        username = user.username if user.is_authenticated else 'Anonymous'
        logger.info(
            f"{request.user} - {request.method} {request.path}")
        response = self.get_response(request)
        return response
