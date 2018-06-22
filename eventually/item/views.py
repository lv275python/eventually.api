"""
Item view module
================

The module that provides basic logic for getting, creating, updating and deleting
of item's model objects.
"""

import datetime
from django.views.generic.base import View
from django.http import JsonResponse
from django.http import HttpResponse
from assignment.views import create_assignment_for_new_item
from mentor.models import MentorStudent
from topic.models import Topic
from utils.responsehelper import (RESPONSE_200_DELETED,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from utils.item_views_functions import organized_items_sequence
from .models import Item


class ItemView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with item model.
    """
    def get(self, request, curriculum_id, item_id=None, topic_id=None):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param item_id: ID of the certain item.
        :type item_id: `int`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: the response with the certain item information when item_id was transferred or
                 the full list of certain topic items organized by priority. If item_id or topic_id
                 does not exist returns the 404 failed status code response.
        :rtype: `HttpResponse object.
        """

        if item_id:
            item = Item.get_by_id(item_id)
            if not item:
                return RESPONSE_404_OBJECT_NOT_FOUND

            item = item.to_dict()
            return JsonResponse(item, status=200)

        if topic_id:
            topic = Topic.get_by_id(topic_id)
            if not topic:
                return RESPONSE_404_OBJECT_NOT_FOUND
            items_superiors_dict = {item.get_item_superiors()[0]:item.get_item_superiors()[1]
                                    for item in topic.item_set.all()}
            items_ids = organized_items_sequence(items_superiors_dict)
            data = {'items': [(Item.get_by_id(item)).to_dict() for item in items_ids]}
            return JsonResponse(data, status=200)

    def post(self, request, curriculum_id, topic_id):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: the response with certain item information when the topic was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object."""

        author = request.user
        data = request.body
        topic = Topic.get_by_id(topic_id)

        if not data:
            return RESPONSE_400_INVALID_DATA

        if not topic:
            return RESPONSE_404_OBJECT_NOT_FOUND
        allowed_authors = topic.mentors.all()

        if author not in allowed_authors:
            return RESPONSE_403_ACCESS_DENIED

        data = {'name': data.get('name'),
                'description': data.get('description') if data.get('description') else '',
                'form': data.get('form'),
                'superiors': [Item.get_by_id(item) for item in data.get('superiors')]\
                              if data.get('superiors') else None,
                'estimation': datetime.timedelta(hours=int(data.get('estimation')))\
                              if isinstance(data.get('estimation'), int) else None}

        item = Item.create(topic=topic, authors=allowed_authors, **data)

        if item:
            topic_students = MentorStudent.get_topic_all_students(topic_id)
            if topic_students:
                create_assignment_for_new_item(item)

            return JsonResponse(item.to_dict(), status=201)

        return HttpResponse('not implemented', status=501)

    def put(self, request, curriculum_id=None, topic_id=None, item_id=None):  # pylint: disable=unused-argument
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: 'int'

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :param item_id: ID of the certain item.
        :type item_id: `int`

        :return: response with status code 200 when topic was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        item = Item.get_by_id(item_id)

        if not item:
            return RESPONSE_404_OBJECT_NOT_FOUND

        topic = Topic.get_by_id(topic_id)
        if not topic:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if user not in topic.mentors.all():
            return RESPONSE_403_ACCESS_DENIED

        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA

        data = {'name': data.get('name'),
                'description': data.get('description'),
                'form': data.get('form'),
                'superiors': [Item.get_by_id(item) for item in data.get('superiors')
                              if data.get('superiors')],
                'estimation': datetime.timedelta(hours=int(data.get('estimation')))\
                              if isinstance(data.get('estimation'), int) else None}

        item.update(**data)

        return RESPONSE_200_UPDATED

    def delete(self, request, curriculum_id, topic_id, item_id):    # pylint: disable=unused-argument
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param curriculum_id: ID of the certain curriculum.
        :type curriculum_id: `int`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :param item_id: ID of the certain item.
        :type item_id: `int`

        :return: response with status code 200 when topic was successfully deleted or response with
                 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        item = Item.get_by_id(item_id)
        topic = Topic.get_by_id(topic_id)
        if not topic:
            return RESPONSE_404_OBJECT_NOT_FOUND
        if not item:
            return RESPONSE_404_OBJECT_NOT_FOUND
        if user in topic.mentors.all():
            is_deleted = Item.delete_by_id(item_id)
            if is_deleted:
                return RESPONSE_200_DELETED
            return RESPONSE_400_DB_OPERATION_FAILED
        return RESPONSE_403_ACCESS_DENIED
