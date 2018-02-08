"""
Views module
===========
"""
from django.http import JsonResponse
from django.views import View
from authentication.models import CustomUser
from event.models import Event
from utils.validators import task_data_validate_update, task_data_validate_create
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_400_EMPTY_JSON)
from .models import Task


def get_users(users_id):
    """
     Function that have to find users in database.

    :param users_id: List with User or users id.
    :type users_id: List

    :return: list with users.
    """


    users = []
    for user_id in users_id:
        user = CustomUser.get_by_id(user_id)
        if user:
            users.append(user)
    return users


class TaskView(View):
    """Task view handles GET, POST, PUT, DELETE requests"""

    def get(self, request, team_id=None, event_id=None, task_id=None):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :param task_id: ID of the certain event.
        :type task_id: `int`

        :return: the response with the certain task information.
                 If task does not exist returns the 404 failed status code response.
            E.G.
            |    {
            |        "id": 4,
            |        "event": 2,
            |        "title": "Hello",
            |        "description": "i`m description",
            |        "created_at": 1510669962,
            |        "updated_at": 1510669962,
            |        "users": [
            |            1, 4
            |        ]
            |    }
        :rtype: `HttpResponse object.
        """


        if task_id:
            task = Task.get_by_id(task_id)
            if not task:
                return RESPONSE_404_OBJECT_NOT_FOUND
            data = task.to_dict()
            if request.GET.get('full_name', None):
                members = [user.to_dict() for user in task.users.all()]
                data['users_id'] = members
            return JsonResponse(data, status=200)

        event = Event.get_by_id(event_id)
        if not event:
            return RESPONSE_404_OBJECT_NOT_FOUND
        tasks = event.task_set.all()
        data = {'tasks': [task.to_dict() for task in tasks]}
        return JsonResponse(data, status=200)


    def post(self, request, team_id=None, event_id=None):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :return: the response with certain task information when the task was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object.
        """

        data = request.body
        event = Event.get_by_id(event_id)

        if not data:
            return RESPONSE_400_EMPTY_JSON

        if not event:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not task_data_validate_create(data):
            return RESPONSE_400_INVALID_DATA

        data = {
            'event': event,
            'title': data.get('title'),
            'description': data.get('description'),
            'status': data.get('status'),
            'users': get_users(data.get('users')) if data.get('users') else [],
        }
        task = Task.create(**data)
        if task:
            task = task.to_dict()
            return JsonResponse(task, status=201)

        return RESPONSE_400_DB_OPERATION_FAILED


    def put(self, request, team_id=None, event_id=None, task_id=None): # pylint: disable=unused-argument
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :param task_id_id: ID of the certain event.
        :type task_id: `int`

        :return: response with status code 204 when event was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object.
        """


        task = Task.get_by_id(task_id)
        if not task:
            return RESPONSE_404_OBJECT_NOT_FOUND

        team_members = task.event.team.members.all()
        if request.user not in team_members:
            return RESPONSE_403_ACCESS_DENIED

        data = request.body

        if not task_data_validate_update(data):
            return RESPONSE_400_INVALID_DATA

        users = get_users(data.get('add_users')) if data.get('add_users') else []
        if users:
            task.add_users(users)

        users = get_users(data.get('remove_users')) if data.get('remove_users') else []
        if users:
            task.remove_users(users)

        data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'status': data.get('status')
        }

        task.update(**data)
        return RESPONSE_200_UPDATED



    def delete(self, request, team_id=None, event_id=None, task_id=None): # pylint: disable=unused-argument
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :return: response with status code 200 when task was successfully deleted or response with
                 403 or 404 failed status code.
        :rtype: `HttpResponse object."""


        team_members = Task.get_by_id(task_id).event.team.members.all()
        if not request.user in team_members:
            return RESPONSE_403_ACCESS_DENIED
        is_deleted = Task.delete_by_id(task_id)
        if is_deleted:
            return RESPONSE_200_DELETED

        return RESPONSE_400_DB_OPERATION_FAILED
