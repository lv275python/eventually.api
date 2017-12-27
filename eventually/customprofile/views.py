"""
CustomProfile view module
=========================
The module that provides basic logic for getting, updating and deleting
of profile's model objects.
"""

import datetime
from django.contrib.auth import logout
from django.views.generic.base import View
from django.http import JsonResponse
from authentication.models import CustomUser
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_403_ACCESS_DENIED)
from utils.validators import (profile_data_validator)


class CustomProfileView(View):
    """
    CustomProfile view that handles GET, PUT, DELETE requests and provides appropriate
    operations with profile model.
    """

    def get(self, request, user_id=None):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param user_id: ID of the certain user.
        :type user_id: `int`

        :return: the response with certain profile information when the profile was successfully
                 created or response with 404 failed status code.

        :rtype: `HttpResponse object`.
        """
        user = request.user

        if user_id:
            user = CustomUser.get_by_id(user_id)
            if not user:
                return RESPONSE_404_OBJECT_NOT_FOUND

        profile = user.customprofile
        profile = profile.to_dict()
        user = user.to_dict()
        information = user.copy()
        information.update(profile)
        return JsonResponse(information, status=200)

    def put(self, request, user_id=None):
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: response with status code 200 when profile was successfully updated
                 or response with 400 or 403 or 404 failed status code.

        :rtype: `HttpResponse object."""
        user = CustomUser.get_by_id(user_id)

        if not request.user == user:
            return RESPONSE_403_ACCESS_DENIED

        data = request.body

        if not profile_data_validator(data):
            return RESPONSE_400_INVALID_DATA

        data_profile = {'hobby': data.get('hobby'),
                        'photo': data.get('photo'),
                        'birthday': datetime.datetime.fromtimestamp(data.get('birthday'))}
        data_user = {'first_name': data.get('first_name'),
                     'middle_name': data.get('middle_name'),
                     'last_name': data.get('last_name')}

        profile = user.customprofile

        user.update(**data_user)
        profile.update(**data_profile)

        return RESPONSE_200_UPDATED

    def delete(self, request):
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: response with status code 200 when profile was successfully deactivated
        :rtype: `HttpResponse object."""
        user = request.user
        user.update(is_active=False)
        logout(request)
        return RESPONSE_200_DELETED
