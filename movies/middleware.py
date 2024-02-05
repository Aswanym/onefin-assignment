from django.core.cache import cache


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # increment request_count for each requests.
        request_count = cache.incr("request_count", 1)
        request.request_count = request_count

        response = self.get_response(request)

        return response
