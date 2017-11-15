"""
Views module
============
"""

from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from authentication.models import CustomUser
from utils.utils import json_loads
from utils.passwordreseting import send_reseting_letter, reset_pasword
from utils.validators import password_validator, email_validator, data_validator
from utils.jwttoken import handle_token


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


class ForgetPassword(View):
    """changing password for current CustomUser"""

    def post(self, request):
        """Handles POST request."""
        data = json_loads(data=request.body)
        if data_validator(data, 'email'):
            email = data.get('email')
            if email_validator(email):
                user = CustomUser.get_by_email(email=email)
                if user:
                    return send_reseting_letter(user)
        return HttpResponse(status=404)

    def put(self, request, token=None):
        """Handles PUT request."""
        if token:
            identifier = handle_token(token)
            if identifier:
                user = CustomUser.get_by_id(identifier['user_id'])
                if user:
                    data = json_loads(data=request.body)
                    if data_validator(data, 'new_password'):
                        new_password = data.get('new_password')
                        passwor_valid = password_validator(new_password)
                        if passwor_valid:
                            return reset_pasword(user, new_password)
        return HttpResponse(status=404)
