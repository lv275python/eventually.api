"""
Event view module
=================

The module that provides basic logic for getting, creating, updating and deleting
of event's model objects.
"""

import datetime
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from utils.validators import event_data_validate
from team.models import Team
from .models import Event


class EventView(View):
    """
    Event view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with event model.
    """

    def get(self, request, team_id=None, event_id=None):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :return: the response with the certain event information when event_id was transferred or
                 the full list of certain team events. If event or team does not exist returns
                 the 404 failed status code response.
        :rtype: `HttpResponse object.
        """

        if event_id:
            event = Event.get_by_id(event_id)
            if not event:
                return HttpResponse(status=404)

            event = event.to_dict()
            return JsonResponse(event, status=200)

        team = Team.get_by_id(team_id)
        if team:
            events = team.event_set.all()
            data = {'events': [event.to_dict() for event in events]}
            return JsonResponse(data, status=200)

        return HttpResponse(status=404)

    def post(self, request, team_id=None):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :return: the response with certain event information when the event was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        data = request.body

        if not data:
            return HttpResponse(status=400)

        if not event_data_validate(data, required_keys=['name']):
            return HttpResponse(status=400)

        team = Team.get_by_id(team_id)
        if not team:
            return HttpResponse(status=404)

        start_at = data.get('start_at')
        start_at = datetime.datetime.fromtimestamp(start_at) if start_at else None
        duration = data.get('duration')
        duration = datetime.timedelta(seconds=duration) if duration else None
        data = {'owner': user,
                'name': data.get('name'),
                'description': data.get('description') if data.get('description') else '',
                'start_at': start_at,
                'duration': duration,
                'longitude': data.get('longitude'),
                'latitude': data.get('latitude'),
                'budget': data.get('budget'),
                'status': data.get('status')}

        event = Event.create(team, **data)
        if event:
            return JsonResponse(event.to_dict(), status=201)

        return HttpResponse(status=400)

    def put(self, request, team_id, event_id=None):  # pylint: disable=unused-argument
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :return: response with status code 204 when event was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        event = Event.get_by_id(event_id)
        if not event:
            return HttpResponse(status=404)

        if user.id is not event.owner.id:
            return HttpResponse(status=403)

        data = request.body
        if not data:
            return HttpResponse(status=400)

        if not event_data_validate(data, required_keys=[]):
            return HttpResponse(status=400)

        start_at = data.get('start_at')
        start_at = datetime.datetime.fromtimestamp(start_at) if start_at else None
        duration = data.get('duration')
        duration = datetime.timedelta(seconds=duration) if duration else None
        data = {'owner': data.get('owner'),
                'name': data.get('name'),
                'description': data.get('description'),
                'start_at': start_at,
                'duration': duration,
                'longitude': data.get('longitude'),
                'latitude': data.get('latitude'),
                'budget': data.get('budget'),
                'status': data.get('status')}

        event.update(**data)
        return HttpResponse(status=204)

    def delete(self, request, team_id, event_id=None):  # pylint: disable=unused-argument
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param team_id: ID of the certain team.
        :type team_id: `int`

        :param event_id: ID of the certain event.
        :type event_id: `int`

        :return: response with status code 200 when event was successfully deleted or response with
                 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        event = Event.get_by_id(event_id)
        if not event:
            return HttpResponse(status=404)

        if user.id is not event.owner.id:
            return HttpResponse(status=403)

        is_deleted = Event.delete_by_id(event_id)
        if is_deleted:
            return HttpResponse(status=200)

        return HttpResponse(status=400)
