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
from utils.topic_views_functions import find_mentors_topics
from utils.responsehelper import (RESPONSE_200_DELETED,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from authentication.models import CustomUser
from .models import Topic


class TopicView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with topic model.
    """

    def get(self, request, topic_id=None, curriculum_id=None):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: `int`

        :return: the response with the certain topic information when topic_id was transferred or
                 or the full list of certain curriculum topics. If topic_id or curriculum_id does
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

    def put(self, request, curriculum_id=None, topic_id=None):  # pylint: disable=unused-argument
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: 'int'

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: response with status code 200 when topic was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        topic = Topic.get_by_id(topic_id)
        if not topic:
            return RESPONSE_404_OBJECT_NOT_FOUND

        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA

        if user not in topic.mentors.all():
            return RESPONSE_403_ACCESS_DENIED

        if data.get('addMentors'):
            mentors_list = [CustomUser.get_by_id(mentor_id) for mentor_id in data.get('addMentors')]
            topic.add_mentors(mentors_list)

        if data.get('title') or data.get('description'):
            data = {'title': data.get('title'),
                    'description': data.get('description')}
            topic.update(**data)

        return RESPONSE_200_UPDATED

    def delete(self, request, curriculum_id, topic_id):    # pylint: disable=unused-argument
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: `int`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: response with status code 200 when topic was successfully deleted or response with
                 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        topic = Topic.get_by_id(topic_id)
        if not topic:
            return RESPONSE_404_OBJECT_NOT_FOUND
        if user == topic.author:
            is_deleted = Topic.delete_by_id(topic_id)
            if is_deleted:
                return RESPONSE_200_DELETED
            return RESPONSE_400_DB_OPERATION_FAILED
        return RESPONSE_403_ACCESS_DENIED


def mentors_topics(request):
    """
    Method that get all topics where mentor is a certain user.

    :param request: the accepted HTTP request.
    :type request: `HttpRequest object`

    :return: JsonResponse object with topics, that belongs to the certain mentor
    """
    mentor = request.user

    topics = find_mentors_topics(mentor.id)
    data = {'topics': [topic.to_dict() for topic in topics]}
    return JsonResponse(data, status=200)


def is_topic_mentor(request, curriculum_id, topic_id):   # pylint: disable=unused-argument
    """
    Function that handle get request for mentor belonging to the certain topic.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :param topic_id: Id of certain topic.
    :type topic_id: integer.

    :return: JsonResponse with data whether user is a mentor of the certain topic.
    """
    user = request.user
    topic = Topic.get_by_id(topic_id)
    is_mentor = False
    if user in topic.mentors.all():
        is_mentor = True
    return JsonResponse({'is_mentor': is_mentor}, status=200)
