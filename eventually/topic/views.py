"""
Topic view module
================

The module that provides basic logic for getting, creating, updating and deleting
of topic's model objects.
"""
from django.views.generic.base import View
from django.http import JsonResponse
from django.http import HttpResponse
from curriculum.models import Curriculum
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from .models import Topic


class TopicView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with topic model.
    """

    def get(self, request, topic_id=None, curriculum_id=None,):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: `int`

        :return: the response with the certain topic information when topic_id was transferred or
                 the full list of certain curriculum topics. If topic_id or curriculum_id does
                 not exist returns the 404 failed status code response.
        :rtype: `HttpResponse object.
        """

        if topic_id:
            topic = Topic.get_by_id(topic_id)
            if not topic:
                return RESPONSE_404_OBJECT_NOT_FOUND

            topic = topic.to_dict()
            return JsonResponse(topic, status=200)

        if curriculum_id:
            curriculum = Curriculum.get_by_id(curriculum_id)
            if not curriculum:
                return RESPONSE_404_OBJECT_NOT_FOUND
            topics = curriculum.topic_set.all()
            data = {'topics': [topic.to_dict() for topic in topics]}
            return JsonResponse(data, status=200)

    def post(self, request, curriculum_id):
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
        curriculum = Curriculum.get_by_id(curriculum_id)

        if not data:
            return RESPONSE_400_INVALID_DATA

        if not curriculum:
            return RESPONSE_404_OBJECT_NOT_FOUND

        data = {'title': data.get('title'),
                'description': data.get('description') if data.get('description') else '',
                'mentors': data.get('mentors') if data.get('mentors') else []}

        topic = Topic.create(curriculum, author, **data)
        if topic:
            return JsonResponse(topic.to_dict(), status=201)

        return HttpResponse('not implemented', status=501)

    def put(self, request, curriculum_id=None, topic_id=None):
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: 'int'

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: response with status code 204 when event was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object."""


def is_topic_mentor(request, curriculum_id, topic_id):
    """
    Function that handle get request for mentor belonging to the certain topic.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :param topic_id: Id of certain topic.
    :type topic_id: integer.

    :return: Boolean
    """
    user = request.user
    topic = Topic.get_by_id(topic_id)
    is_mentor = False
    if user in topic.mentors.all():
        is_mentor = True
    return JsonResponse({'is_mentor': is_mentor}, status=200)