"""
Views module
============
"""

from utils.utils import json_loads
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


class UserView(View):
    """UserView view handles GET, POST, PUT, DELETE requests."""


def registration_user():
    """Registration CustomUser"""

def login_user(request):
    """
    Login of the existing user. Handles post and get requests.

    :param request: request from the website
    :return: status 302 if login was successful, status 401 if unsuccessful
    """

    if request.method == "POST":
        data = json_loads(request.body)
        if data:
            user = authenticate(email=data['email'], password=data['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponse(status=200)
    return HttpResponse(status=400)


def logout_user(request):
    """
    Logout of the existing user. Handles post and get requests.
    :param request: request from the website
    :return: status 200
    """

    if request.method == "POST":
        logout(request)
        return HttpResponse(status=200)
    return HttpResponse(status=400)
