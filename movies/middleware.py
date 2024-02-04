from django.core.cache import cache


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        cache.set("request_count", 0, timeout=None)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # increment request_count for each requests.
        request_count = cache.incr("request_count")
        request.request_count = request_count

        response = self.get_response(request)

        return response
