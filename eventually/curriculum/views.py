"""
Curriculum Views
================
"""
from django.views.generic.base import View
from django.http import JsonResponse
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_403_ACCESS_DENIED)
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

        data = request.body
        owner = request.user
        if not data:
            return RESPONSE_400_INVALID_DATA

        data = {'name': data.get('title'), 'owner': owner,
                'description': data.get('description') if data.get('description') else ''}

        curriculum = Curriculum.create(**data)
        if curriculum:
            return JsonResponse(curriculum.to_dict(), status=201)

        return RESPONSE_400_DB_OPERATION_FAILED

    def put(self, request, curriculum_id):
        """
        Method that handles PUT request.
        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`
        :param curriculum_id: ID of the certain curriculumn.
        :type curriculum_id: `int`
        :return: response with status code 200 when curriculumn was successfully updated
                 or response with 400 or 403 or 404 failed status code.
        :rtype: `HttpResponse object."""
        user = request.user
        curriculum = Curriculum.get_by_id(curriculum_id)

        if not curriculum:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not user == curriculum.owner:
            return RESPONSE_403_ACCESS_DENIED

        curriculum_data = request.body
        if not curriculum_data:
            return RESPONSE_400_INVALID_DATA

        curriculum_data = {'name': curriculum_data.get('name'),
                           'description': curriculum_data.get('description'),
                           'owner': curriculum_data.get('owner')}

        curriculum.update(**curriculum_data)
        return RESPONSE_200_UPDATED

    def delete(self, request, curriculum_id):
        """
        Method that handles DELETE request.
        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`
        :param curriculum_id: ID of the certain curriculumn.
        :type curriculum_id: `int`
        :return: response with status code 200 when curriculumn was successfully deleted
                 or response with 400 or 403 or 404 failed status code.
        :rtype: `HttpResponse object."""
        user = request.user
        curriculum = Curriculum.get_by_id(curriculum_id)

        if not curriculum:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not user == curriculum.owner:
            return RESPONSE_403_ACCESS_DENIED

        is_deleted = Curriculum.delete_by_id(curriculum_id)
        if is_deleted:
            return RESPONSE_200_DELETED

        return RESPONSE_400_DB_OPERATION_FAILED
