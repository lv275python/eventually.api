"""
CustomProfile view module
=================
The module that provides basic logic for getting, updating and deleting
of profile's model objects.
"""

import datetime
from django.contrib.auth import logout
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from authentication.models import CustomUser
from utils.validators import (profile_data_validator)


class CustomProfileView(View):
    """
    CustomProfile view that handles GET, PUT, DELETE requests and provides appropriate
    operations with profile model.
    """

    def get(self, request, user_id):
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
                return HttpResponse(status=404)

        profile = user.customprofile
        profile = profile.to_dict()
        user = user.to_dict()
        information = user.copy()
        information.update(profile)
        return JsonResponse(information, status=200)

    def put(self, request, user_id):
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: response with status code 201 when profile was successfully updated
                 or response with 400 or 403 or 404 failed status code.

        :rtype: `HttpResponse object."""
        print(request.body)
        userreq = request.user
        user = CustomUser.get_by_id(user_id)
        if not user:
            return HttpResponse(status=404)

        if not userreq.id == user.id:
            return HttpResponse(status=403)

        data = request.body
        if not profile_data_validator(data):
            return HttpResponse(status=400)

        birth = datetime.date.fromtimestamp(data.get('birthday')) if data.get('birthday') else None
        data = {'hobby': data.get('hobby'),
                'photo': data.get('photo'),
                'birthday': birth}
        profile = user.customprofile
        profile.update(**data)
        profile = profile.to_dict()
        return JsonResponse(profile, status=201)

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
        return HttpResponse(status=200)
