"""
Curriculum Views
================
"""
from django.views.generic.base import View
from django.http import JsonResponse
from utils.responsehelper import (RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_DATA,)
from .models import Curriculum


class CurriculumView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with Curriculum model.
    """
    def get(self, request, curriculum_id=None):
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

        if curriculum_id:
            curriculum = Curriculum.get_by_id(curriculum_id)
            data = curriculum.to_dict()
            return JsonResponse(data, status=200)
        curriculums = Curriculum.get_all()
        data = {'curriculums': [curriculum.to_dict() for curriculum in curriculums]}
        return JsonResponse(data, status=200)

    def post(self, request):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: the response with certain topic information when the topic was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object."""

        # author = request.user
        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA

        data = {'name': data.get('title'),
                'description': data.get('description') if data.get('description') else ''}

        curriculum = Curriculum.create(**data)
        if curriculum:
            return JsonResponse(curriculum.to_dict(), status=201)

        return RESPONSE_400_DB_OPERATION_FAILED
