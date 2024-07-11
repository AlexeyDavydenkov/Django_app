import time
from django.http import HttpResponseForbidden

REQUEST_THROTTLING_DELAY = 0

last_request_time = {}


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        current_time = time.time()

        if ip_address in last_request_time:
            elapsed_time = current_time - last_request_time[ip_address]
            if elapsed_time < REQUEST_THROTTLING_DELAY:
                return HttpResponseForbidden('Too many requests. Try later.')

        last_request_time[ip_address] = current_time
        response = self.get_response(request)
        return response
