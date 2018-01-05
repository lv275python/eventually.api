"""
Online status
=============
The module that provides functionality for online status checking.
"""
from utils.redishelper import redisHelper


class OnlineStatusMiddleware():  # pylint: disable=too-few-public-methods
    """
    The class that represents logic for setting user id in redis db
    """

    def __init__(self, get_response):
        """Constructor method that creates middleware instance."""

        self.get_response = get_response

    def __call__(self, request):
        """
        Method that makes middleware instance callable and implements setting user id in redis db
        """
        user = request.user
        if user.is_authenticated():
            redisHelper.set(user.id, user.email)
        response = self.get_response(request)
        return response
