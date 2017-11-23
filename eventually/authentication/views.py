"""
Auth views module
=================
"""

from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from authentication.models import CustomUser
from eventually.settings import FRONT_HOST
from utils.jwttoken import create_token, handle_token
from utils.passwordreseting import send_password_update_letter, send_successful_update_letter
from utils.send_mail import send_email
from utils.validators import (password_validator,
                              email_validator,
                              reset_password_validate,
                              registration_validate,
                              login_validate)



class UserView(View):
    """UserView view handles GET, POST, PUT, DELETE requests."""


def registration(request):
    """Registration CustomUser"""
    if request.method == 'POST':
        data = request.body
        if not data:
            return HttpResponse(status=400)
        if not registration_validate(data):
            return HttpResponse('Data is not valid', status=400)

        user = CustomUser.create(first_name=data.get('first_name'),
                                 last_name=data.get('last_name'),
                                 middle_name=data.get('middle_name'),
                                 email=data['email'].lower().strip(),
                                 password=data['password'])
        if not user:
            return HttpResponse('Email is already exist', status=400)

        ctx = {
            'first_name': user.first_name,
            'domain': FRONT_HOST,
            'token': create_token(data={'email': user.email}, expiration_time=60*60),
        }
        message = 'registration'
        mail_subject = 'Activate account'
        send_email(mail_subject, message, [user.email], 'registration.html', ctx)
        msg = 'Please confirm your email address to complete the registration'
        return HttpResponse(msg, status=201)
    return HttpResponse(status=400)


def activate(request, token):
    """Activation CustomUser"""
    if request.method == 'GET':

        data = handle_token(token)
        if not data:
            return HttpResponse(status=498)
        user = CustomUser.get_by_email(email=data['email'])
        if user:
            user.update(is_active=True)
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    return HttpResponse(status=404)

def login_user(request):
    """
    Login of the existing user. Handles post and get requests.

    :param request: request from the website
    :return: status 200 if login was successful, status 400 if unsuccessful
    """

    if request.method == "POST":
        data = request.body
        if not login_validate(data):
            return HttpResponse(status=400)
        email = data['email'].strip().lower()
        user = authenticate(email=email, password=data['password'])
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

    if request.method == "GET":
        logout(request)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


class ForgetPassword(View):
    """changing password for current CustomUser"""

    def post(self, request):
        """Handles POST request."""
        data = request.body
        if reset_password_validate(data, 'email'):
            email = data.get('email')
            if email_validator(email):
                user = CustomUser.get_by_email(email=email)
                if user:
                    send_password_update_letter(user)
                    return HttpResponse(status=200)
        return HttpResponse(status=400)

    def put(self, request, token=None):
        """Handles PUT request."""
        if token:
            identifier = handle_token(token)
            if identifier:
                user = CustomUser.get_by_id(identifier['user_id'])
                if user:
                    data = request.body
                    if reset_password_validate(data, 'new_password'):
                        new_password = data.get('new_password')
                        if password_validator(new_password):
                            user.set_password(new_password)
                            send_successful_update_letter(user)
                            return HttpResponse(status=200)
            return HttpResponse(status=400)
        return HttpResponse(status=498)
