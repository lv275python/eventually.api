"""
SuggestedTopics view module
================

The module that provides basic logic for getting, creating, updating and deleting
of SuggestedTopics's model objects.
"""

from django.views.generic.base import View
from django.http import JsonResponse
from django.http import HttpResponse
from utils.validators import required_keys_validator
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_DB_OPERATION_FAILED,)
from .models import SuggestedTopics


class SuggestedTopicsView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with SuggestedTopics model.
    """

    def get(self, request):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param suggested_topic_id: ID of the certain suggested topic.
        :type suggested_topic_id: `int`

        :return: the response with the certain suggested topic information. If suggested_topic_id
                 does not exist returns the 404 failed status code response.
        :rtype: `HttpResponse object.
        """

        suggested_topics = SuggestedTopics.objects.all()
        data = {'suggested_topics': [topic.to_dict() for topic in suggested_topics]}
        return JsonResponse(data, status=200)

    def post(self, request):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: `int`

        :return: the response with certain topic information when the topic was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object."""

        author = request.user
        data = request.body

        if not data:
            return RESPONSE_400_EMPTY_JSON
        keys_required = ['name', 'description']
        if not required_keys_validator(data, keys_required, False):
            return RESPONSE_400_INVALID_DATA
        suggested_topic = SuggestedTopics.create(author, **data)
        if suggested_topic:
            return JsonResponse(suggested_topic.to_dict(), status=201)
        return HttpResponse('not implemented', status=501)

    def put(self, request, suggested_topic_id=None):
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param suggested_topic_id: ID of the certain suggested topic.
        :type suggested_topic_id: `int`

        :return: response with status code 204 when event was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        suggested_topic = SuggestedTopics.get_by_id(suggested_topic_id)

        if not suggested_topic:
            return RESPONSE_404_OBJECT_NOT_FOUND
        data = request.body
        if not data:
            return RESPONSE_400_EMPTY_JSON
        suggested_topic.update(**data)
        return RESPONSE_200_UPDATED

    def delete(self, request, suggested_topic_id):
        """
        Method that handles DELETE request

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param suggested_topic_id: ID of the certain suggested topic.
        :type suggested_topic_id: `int`

        :return: response with status code 200 when event was successfully deleted
                 400 or 403 failed status code.
        :rtype: `HttpResponse object.
        """
        user = request.user
        if user == request.user:
            is_deleted = SuggestedTopics.delete_by_id(suggested_topic_id)
            if is_deleted:
                return RESPONSE_200_DELETED
            return RESPONSE_400_DB_OPERATION_FAILED
        return RESPONSE_403_ACCESS_DENIED
