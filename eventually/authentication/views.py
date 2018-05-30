"""
Auth views module
=================
"""

from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from authentication.models import CustomUser
from customprofile.models import CustomProfile
from eventually.settings import FRONT_HOST
from utils.jwttoken import create_token, handle_token
from utils.passwordreseting import send_password_update_letter, send_successful_update_letter
from utils.send_mail import send_email
from utils.responsehelper import (RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_UPDATED, RESPONSE_200_DELETED,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_400_EXISTED_EMAIL,
                                  RESPONSE_400_INVALID_HTTP_METHOD,
                                  RESPONSE_498_INVALID_TOKEN,
                                  RESPONSE_200_ACTIVATED,
                                  RESPONSE_400_INVALID_EMAIL,
                                  RESPONSE_400_INVALID_EMAIL_OR_PASSWORD,
                                  RESPONSE_200_OK)
from utils.validators import (updating_password_validate,
                              updating_email_validate,
                              registration_validate,
                              login_validate,
                              string_validator,
                              password_validator)

TTL_SEND_PASSWORD_TOKEN = 60 * 60
USER_TTL_NOTIFICATOR = TTL_SEND_PASSWORD_TOKEN / 60
TTL_USER_ID_COOKIE = 60 * 60 * 24 * 14

class UserView(View):
    """    A class to handle GET, PUT and DELETE operations    """

    def get(self, request, user_id):
        """
        Handles GET request, retrieves a user profile from the database
        :param request: request from the web page
        :type request: HttpRequest

        :param user_id: id of a user to return.
        :type user_id: int

        :return: User profile Json and Status 200 if user exists, otherwise Status 404
        :Example: user profile Json
        |  {
        |   "id": 24,
        |   "first_name": "TechGG76",
        |   "middle_name": "Postgres",
        |   "last_name": "Jr.",
        |   "email": "postman424@co.uk",
        |   "created_at": 1509831239,
        |   "updated_at": 1509835437
        |  }
        """

        user = CustomUser.get_by_id(user_id=user_id)
        if user:
            user = user.to_dict()
            return JsonResponse(user, status=200)
        return RESPONSE_404_OBJECT_NOT_FOUND

    def put(self, request, user_id):
        """
        Handles PUT request, modifies the user profile in the database.
        If user first_name or middle_name or last_name length is less than 3 than it's not updated

        :param request: request from the web page with a json containing changes to be applied
        :type request: HttpRequest
        :Example: incoming JSON request:
        | {
        |   "first_name":"Jamie",
        |   "last_name":"Ariana"
        | }

        :param user_id: id of a user which has to be changed
        :type user_id: str

        :return: status 200 if user has been updated,
                 status 404 if user hasn't been found,
        """

        new_attrs = request.body

        user = CustomUser.get_by_id(user_id)
        if not user:
            return RESPONSE_404_OBJECT_NOT_FOUND

        first_name = new_attrs.get('first_name')
        last_name = new_attrs.get('last_name')
        middle_name = new_attrs.get('middle_name')

        if not string_validator(first_name, 3):
            first_name = False
        if not string_validator(last_name, 3):
            last_name = False
        if not string_validator(middle_name, 3):
            middle_name = False

        new_password = new_attrs.get('password')
        if new_password and not password_validator(new_password):
            return RESPONSE_400_INVALID_DATA

        user.update(first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    password=new_password)
        return RESPONSE_200_UPDATED

    def delete(self, request, user_id):
        """
        Handles delete request

        :param user_id: id of a user to delete
        :type user_id: str

        :return: status 200 if user deleted,
                 status 404 if user not found
        """

        user = CustomUser.get_by_id(user_id)
        if not user:
            return RESPONSE_404_OBJECT_NOT_FOUND
        if user.id == request.user.id:
            if CustomUser.delete_by_id(user_id):
                return RESPONSE_200_DELETED
        return RESPONSE_403_ACCESS_DENIED


def registration(request):
    """Registration CustomUser"""
    if request.method == 'POST':
        data = request.body
        if not data:
            return RESPONSE_400_EMPTY_JSON
        if not registration_validate(data):
            return RESPONSE_400_INVALID_DATA

        user = CustomUser.create(first_name=data.get('first_name'),
                                 last_name=data.get('last_name'),
                                 middle_name=data.get('middle_name'),
                                 email=data['email'].lower().strip(),
                                 password=data['password'])
        if not user:
            return RESPONSE_400_EXISTED_EMAIL

        ctx = {
            'first_name': user.first_name,
            'domain': FRONT_HOST,
            'token': create_token(data={'email': user.email},
                                  expiration_time=TTL_SEND_PASSWORD_TOKEN),
            'time_left': USER_TTL_NOTIFICATOR,
        }
        message = 'registration'
        mail_subject = 'Activate account'
        send_email(mail_subject, message, [user.email], 'registration.html', ctx)
        msg = 'Please confirm your email address to complete the registration'
        return HttpResponse(msg, status=201)
    return RESPONSE_400_INVALID_HTTP_METHOD


def activate(request, token):
    """Activation CustomUser"""
    if request.method == 'GET':

        data = handle_token(token)
        if not data:
            return RESPONSE_498_INVALID_TOKEN
        user = CustomUser.get_by_email(email=data['email'])
        if user:
            user.update(is_active=True)
            CustomProfile.create(user)
            return RESPONSE_200_ACTIVATED
        return RESPONSE_400_INVALID_EMAIL
    return RESPONSE_400_INVALID_HTTP_METHOD


def login_user(request):
    """
    Login of the existing user. Handles post and get requests.

    :param request: request from the website
    :return: status 200 if login was successful, status 400 if unsuccessful
    """

    if request.method == "POST":
        data = request.body
        if not login_validate(data):
            return RESPONSE_400_INVALID_DATA
        email = data['email'].strip().lower()
        user = authenticate(email=email, password=data['password'])
        if user and user.is_active:
            login(request, user)
            response = RESPONSE_200_OK
            response.set_cookie('user_id', user.id, max_age=TTL_USER_ID_COOKIE)
            return response
        return RESPONSE_400_INVALID_EMAIL_OR_PASSWORD
    return RESPONSE_400_INVALID_HTTP_METHOD


def logout_user(request):
    """
    Logout of the existing user. Handles post and get requests.
    :param request: request from the website
    :return: status 200
    """

    if request.method == "GET":
        logout(request)
        response = RESPONSE_200_OK
        response.delete_cookie('user_id')
        return response
    return RESPONSE_400_INVALID_HTTP_METHOD


class ForgetPassword(View):
    """changing password for current CustomUser"""

    def post(self, request):
        """Handles POST request."""
        data = request.body
        if updating_email_validate(data, 'email'):
            email = data.get('email')
            user = CustomUser.get_by_email(email=email)
            if user:
                arg = {'user_id': user.id}
                token = create_token(data=arg, expiration_time=TTL_SEND_PASSWORD_TOKEN)
                send_password_update_letter(user, token)
                return RESPONSE_200_OK
        return RESPONSE_400_INVALID_DATA

    def put(self, request, token=None):
        """Handles PUT request."""
        if token:
            identifier = handle_token(token)
            if not identifier:
                return RESPONSE_498_INVALID_TOKEN
            user = CustomUser.get_by_id(identifier['user_id'])
            if not user:
                return RESPONSE_404_OBJECT_NOT_FOUND
            data = request.body
            if updating_password_validate(data, 'new_password'):
                new_password = data.get('new_password')
                if not user.check_password(new_password):
                    user.update(password=new_password)
                    send_successful_update_letter(user)
                    return RESPONSE_200_OK
        return RESPONSE_400_INVALID_DATA

def get_all_users(request):
    """
    returns JSON response with all users querysets
    """
    if request.method == "GET":
        users = CustomUser.get_all()
        data = {'users': [user.to_dict() for user in users]}
        return JsonResponse(data, status=200)
    return RESPONSE_400_INVALID_HTTP_METHOD
