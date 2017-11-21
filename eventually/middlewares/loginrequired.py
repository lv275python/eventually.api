"""
Middleware
==========
The module that provides custom application's middlewares and and provides custom JSON check.
"""

import json
from json.decoder import JSONDecodeError
from django.http import HttpResponse

ANONYMOUS_USERS_PATHS = ['/api/v1/user/login/',
                         '/api/v1/user/register/',
                         '/api/v1/user/activate/',
                         '/api/v1/user/forget_password/']
ENCODING = "utf-8"


class LoginRequiredMiddleware():  # pylint: disable=too-few-public-methods
    """
    The class that represents the middleware that permits only a few available paths
    for anonymous users and provides custom JSON check.
    """

    def __init__(self, get_response):
        """Constructor method that creates middleware instance."""

        self.get_response = get_response

    def __call__(self, request):
        """
        Method that makes the middleware instance callable and implements authentication
        verification and provides custom JSON check.
        """

        if request.method == 'POST' or request.method == 'PUT':
            try:
                request._body = json.loads(request.body.decode(ENCODING))  # pylint: disable=W0212
            except (SyntaxError, JSONDecodeError):
                return HttpResponse('invalid JSON', status=400)
                # dont forget about loger
        for current_path in ANONYMOUS_USERS_PATHS:
            if request.path_info.startswith(current_path):

                if request.user.is_authenticated():
                    return HttpResponse(status=400)

                response = self.get_response(request)
                return response

        if not request.user.is_authenticated():
            return HttpResponse(status=403)

        response = self.get_response(request)
        return response
