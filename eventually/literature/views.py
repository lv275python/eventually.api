"""Views"""
from django.http import JsonResponse
from django.views.generic.base import View
from item.models import Item
from utils.responsehelper import (RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_403_ACCESS_DENIED)
from .models import LiteratureItem


class LiteratureItemView(View):
    """LiteratureItem view handles GET, POST, PUT, DELETE requests."""

    def get(self, request, item_id=None, literature_id=None):
        """Handles
        GET request, retrieves literature from the database

        :param
        request: request from the web page
        :type
        request: http Request

        :param
        item_id: id of a item to return.
        :type
        item_id: int

        :param
        literature_id: id of a literature to return.
        :type
        literature_id: int

        :return: if literature_id return dict of literature_item
            |{ 'id': 12,
            |  'title': 'C++',
            |  'description': 'book for students',
            |  'source': 'www.bookonline.com',
            |  'created_at': 1509393505,
            |  'updated_at': 1509402867,
            |  'author': 11,
            |  'item': 7 }
            |}

        :return: if item_id return list of dict with literature
            [{ 'id': 10,
            |  'title': 'Python',
            |  'description': 'book for students',
            |  'source': 'www.bookonline.com',
            |  'created_at': 1509393505,
            |  'updated_at': 1509402867,
            |  'author': 10,
            |  'item': 2 },
            |{ 'id': 15,
            |  'title': 'Java',
            |  'description': 'book for developers',
            |  'source': 'www.bookonline.com',
            |  'created_at': 1509393505,
            |  'updated_at': 1509402867,
            |  'author': 100,
            |  'item': 4 },
            | }]
        :rtype: `HttpResponse object.
        """

        author = request.user
        if literature_id:
            literature = LiteratureItem.get_by_id(literature_id)
            if literature:
                data = literature.to_dict()
                return JsonResponse(data, status=200)
            return RESPONSE_404_OBJECT_NOT_FOUND

        if item_id:
            literature = LiteratureItem.objects.filter(item_id=item_id)
            data = {'literature_list':
                    [literature_item.to_dict() for literature_item in literature]}
            return JsonResponse(data, status=200)

        if not literature_id and not item_id:
            literature = LiteratureItem.objects.filter(author_id=author.id)
            if literature:
                data = {'user_literature_list':
                        [literature_item.to_dict() for literature_item in literature]}
                return JsonResponse(data, status=200)
            return RESPONSE_404_OBJECT_NOT_FOUND

    def post(self, request, item_id=None):
        """
        Handles POST request, create a new literature in database
        :param request: request from the web page
        :type request: http Request
        :Example: incoming JSON request:
        | {
        |   "title": "Javascript",
        |   "description": "Book for JS",
        |   "source": "www.onlinementor.com"
        |}

        :return: status 200 if literature has been created,
                status 400 if literature hasn't been created,
        :rtype: `HttpResponse object.
        """

        author = request.user
        data = request.body
        if not data:
            return RESPONSE_400_EMPTY_JSON
        item = Item.get_by_id(item_id)
        data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'source': data.get('source'),
            'author': author,
            'item': item if item else None,
        }

        literature_item = LiteratureItem.create(**data)
        if literature_item:
            literature_item = literature_item.to_dict()
            return JsonResponse(literature_item, status=201)

        return RESPONSE_400_DB_OPERATION_FAILED

    def put(self, request, item_id=None, literature_id=None): # pylint: disable=unused-argument
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param item_id: id of the certain item.
        :type item_id: `int`

        :param literature_id: id of the certain literature.
        :type literature_id: `int`

        :return: response with status code 204 when event was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object.
        """

        literature = LiteratureItem.get_by_id(literature_id)
        if not literature:
            return RESPONSE_404_OBJECT_NOT_FOUND

        author = request.user
        if author.id is not literature.author_id:
            return RESPONSE_403_ACCESS_DENIED

        data = request.body
        if not data:
            return RESPONSE_400_EMPTY_JSON

        data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'source': data.get('source')
        }

        literature.update(**data)
        return RESPONSE_200_UPDATED

    def delete(self, request, item_id=None, literature_id=None): # pylint: disable=unused-argument
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

         :param item_id: id of the certain item.
        :type item_id: `int`

        :param literature_id: id of the certain literature.
        :type literature_id: `int`

        :return: response with status code 200 when event was successfully deleted or response with
                 400 or 404 failed status code.
        :rtype: `HttpResponse object.
        """

        author = request.user
        literature = LiteratureItem.get_by_id(literature_id)
        if not literature:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if author.id is not literature.author_id:
            return RESPONSE_403_ACCESS_DENIED

        is_deleted = LiteratureItem.delete_by_id(literature_id)
        if is_deleted:
            return RESPONSE_200_DELETED
        return RESPONSE_400_DB_OPERATION_FAILED
