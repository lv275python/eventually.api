"""
Views module
===========
"""
from django.http import JsonResponse, HttpResponse
from django.views import View

from authentication.models import CustomUser
from event.models import Event
from team.models import Team
from utils.validators import task_data_validate_update, task_data_validate_create
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
                return HttpResponse(status=404)
            task = task.to_dict()
            return JsonResponse(task, status=200)

        event = Event.get_by_id(event_id)
        if not event:
            return HttpResponse(status=404)
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
        team = Team.get_by_id(team_id)
        event = Event.get_by_id(event_id)

        if not data:
            return HttpResponse(status=400)

        if not team:
            return HttpResponse(status=404)

        if not event:
            return HttpResponse(status=404)

        if not task_data_validate_create(data):
            return HttpResponse('data is not valid', status=400)


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

        return HttpResponse(status=400)


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
            return HttpResponse(status=404)

        team_members = task.event.team.members.all()
        if request.user not in team_members:
            return HttpResponse(status=403)

        data = request.body

        if not task_data_validate_update(data):
            return HttpResponse('data is not valid', status=400)

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
        return HttpResponse(status=204)



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
            return HttpResponse(status=403)
        is_deleted = Task.delete_by_id(task_id)
        if is_deleted:
            return HttpResponse(status=200)

        return HttpResponse(status=400)
