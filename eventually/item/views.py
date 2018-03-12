"""
Item view module
================

The module that provides basic logic for getting, creating, updating and deleting
of item's model objects.
"""

from django.views.generic.base import View
from django.http import JsonResponse
from django.http import HttpResponse
from topic.models import Topic
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
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
                 the full list of certain topic items. If item_id or topic_id does
                 not exist returns the 404 failed status code response.
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
            items = topic.item_set.all()
            data = {'items': [item.to_dict() for item in items]}
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
                'superiors': data.get('superiors') if data.get('superiors') else [],
                'estimation': data.get('estimation') if data.get('estimation') else None}

        item = Item.create(topic=topic, authors=allowed_authors, **data)
        if item:
            return JsonResponse(item.to_dict(), status=201)

        return HttpResponse('not implemented', status=501)
