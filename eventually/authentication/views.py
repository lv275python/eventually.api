"""
Views module
============
"""

from django.views.generic.base import View


class UserView(View):
    """UserView view handles GET, POST, PUT, DELETE requests."""


def registration_user():
    """Registration CustomUser"""
