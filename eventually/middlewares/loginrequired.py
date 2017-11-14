"""
Middleware
==========
The module that provides custom application's middlewares.
"""

from django.http import HttpResponse

ANONYMOUS_USERS_PATHS = ['/api/v1/login/',
                         '/api/v1/registration/',
                         '/api/v1/activate/',
                         '/api/v1/forget_password/']


class LoginRequiredMiddleware(): # pylint: disable=too-few-public-methods
    """
    The class that represents the middleware that permits only a few available paths
    for anonymous users.
    """

    def __init__(self, get_response):
        """Constructor method that creates middleware instance."""

        self.get_response = get_response

    def __call__(self, request):
        """
        Method that makes the middleware instance callable and implements authentication
        verification.
        """

        for current_path in ANONYMOUS_USERS_PATHS:
            if request.path_info.startswitch(current_path):

                if request.user.is_authenticated():
                    return HttpResponse(status=400)

                response = self.get_response(request)
                return response

        if not request.user.is_authenticated():
            return HttpResponse(status=403)

        response = self.get_response(request)
        return response
