"""
Views module
============
"""

from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from utils.validators import comment_data_validator
from event.models import Event
from task.models import Task
from team.models import Team
from vote.models import Vote
from .models import Comment


class CommentView(View):
    """Comment view handles GET, POST, PUT, DELETE requests."""

    def get(self, request, team_id=None, event_id=None, task_id=None, # pylint: disable=unused-argument
                           vote_id=None, comment_id=None): # pylint: disable=unused-argument
        """
        Handle GET request.

        :param request: client HttpRequest. Is required
        :type request: HttpRequest

        :param comment_id: id of Comment model
        :type comment_id: int

        :return: return JsonResponse within comment data with status 200 if parameters are good or
                        HttpRequest with error if parameters are bad

        """

        if comment_id:
            comment = Comment.get_by_id(comment_id)
            if comment:
                comment = comment.to_dict()
                return JsonResponse(comment, status=200)
            return HttpResponse(status=404)

        commented = None
        if task_id:
            commented = Task.get_by_id(task_id)
        elif vote_id:
            commented = Vote.get_by_id(vote_id)
        elif event_id:
            commented = Event.get_by_id(event_id)
        else:
            commented = Team.get_by_id(team_id)

        comments = commented.comment_set.all()
        data = {'comments': [comment.to_dict() for comment in comments]}
        return JsonResponse(data, status=200)


    def post(self, request, team_id=None, event_id=None, task_id=None, vote_id=None): # pylint: disable=unused-argument

        """
        Handle POST request.

        :param request: client HttpRequest. Is required
        :type request: HttpRequest

        :param team_id: id of Team model
        :type team_id: int

        :param event_id: id of Event model
        :type event_id: int

        :param task_id: id of Task model
        :type task_id: int

        :param vote_id: id of Vote model
        :type vote_id: int

        :return: return JsonResponse within comment data with status 201 if comment was created
                 or HttpRequest with error if parameters are bad

        """

        task = Task.get_by_id(task_id)
        vote = Vote.get_by_id(vote_id)
        event = Event.get_by_id(event_id)
        team = Team.get_by_id(team_id)

        if not (task or vote or event or team):
            return HttpResponse(status=404)

        data = request.body
        if not comment_data_validator(data):
            return HttpResponse(status=400)

        comment = Comment.create(author=request.user,
                                 text=data.get("text"),
                                 team=team,
                                 event=event,
                                 task=task,
                                 vote=vote)
        if comment:
            return JsonResponse(comment.to_dict(), status=201)
        return HttpResponse(status=400)

    def put(self, request, team_id=None, event_id=None, task_id=None, # pylint: disable=unused-argument
                           vote_id=None, comment_id=None): # pylint: disable=unused-argument
        """
        Handle PUT request.

        :param request: client HttpRequest. Is required
        :type request: HttpRequest

        :param comment_id: id of Comment model
        :type comment_id: int

        :return: return JsonResponse within comment data with status 200 if parameters are good or
                        HttpRequest with error if parameters are bad
        """
        data = request.body
        if not comment_data_validator(data):
            return HttpResponse(status=400)

        comment = Comment.get_by_id(comment_id)
        if comment:
            if request.user == comment.author:
                comment.update(text=data.get("text"))
                comment = comment.to_dict()
                return JsonResponse(comment, status=200)
            return HttpResponse(status=403)
        return HttpResponse(status=404)

    def delete(self, request, team_id=None, event_id=None, task_id=None, # pylint: disable=unused-argument
                              vote_id=None, comment_id=None): # pylint: disable=unused-argument
        """
        Handle DELETE request.

        :param request: client HttpRequest. Is required
        :type request: HttpRequest

        :param comment_id: id of Comment model
        :type comment_id: int

        :return: return JsonResponse within comment data with status 200 if parameters are good or
                        HttpRequest with error if parameters are bad

        """
        comment = Comment.get_by_id(comment_id)
        if comment:
            if request.user == comment.author:
                return HttpResponse(status=200)
            return HttpResponse(status=403)
        return HttpResponse(status=404)
