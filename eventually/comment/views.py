"""
Views module
============
"""

from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from authentication.models import CustomUser
from utils.validators import string_validator, required_keys_validator
from utils.utils import json_loads
from event.models import Event
from task.models import Task
from team.models import Team
from vote.models import Vote
from .models import Comment




class CommentView(View):
    """Comment view handles GET, POST, PUT, DELETE requests."""

    def get(self, request, team_id=None, event_id=None, task_id=None, vote_id=None,
            comment_id=None):
        """
        Handle GET request.


        """
        team = Team.get_by_id(team_id)
        if not team:
            return HttpResponse(status=404)

        event = Event.get_by_id(event_id)
        task = Task.get_by_id(task_id)
        vote = Vote.get_by_id(vote_id)

        if comment_id:
            comment = Comment.get_by_id(comment_id)
            if comment:
                if comment.team == team and \
                   comment.event == event and \
                   comment.task == task and \
                   comment.vote == vote:
                        comment = comment.to_dict()

                        return JsonResponse(comment, status=200)

                return HttpResponse(status=400)

            return HttpResponse(status=404)

        # comments = Comment.get_all()
        # data = [comment.to_dict() for comment in comments]
        #
        # return JsonResponse(data, status=200)
        return HttpResponse(status=400)

    def post(self, request, team_id=None, event_id=None, task_id=None, vote_id=None):
        """Handle POST request."""
        data = json_loads(request.body)

        if not data:
            return HttpResponse(status=400)

        if not required_keys_validator(data, ["author", "text"]):
            return HttpResponse(status=400)

        if not string_validator(data.get("text")):
            return HttpResponse(status=400)

        team = Team.get_by_id(team_id)
        if not team:
            return HttpResponse(status=404)

        if event_id:
            event = Event.get_by_id(event_id)
            if not event:
                return HttpResponse(status=404)
            if event.team != team:
                return HttpResponse(status=400)
        else:
            event = None

        if task_id:
            task = Task.get_by_id(task_id)
            if not task:
                return HttpResponse(status=404)
            if task.team != team and task.event != event:
                return HttpResponse(status=400)
        else:
            task = None

        if vote_id:
            vote = Vote.get_by_id(vote_id)
            if not vote:
                return HttpResponse(status=404)
            if vote.team != team and vote.event != event:
                return HttpResponse(status=400)
        else:
            vote = None

        author = CustomUser.get_by_id(data.get("author"))
        if not author:
            return HttpResponse(status=404)

        comment = Comment.create(team=team,
                                 author=author,
                                 text=data.get("text"),
                                 event=event,
                                 task=task_id,
                                 vote=vote)
        comment = comment.to_dict()

        return JsonResponse(comment, status=201)

    def put(self, request, team_id=None, event_id=None, task_id=None, vote_id=None,
            comment_id=None):
        """Handle PUT request."""
        data = json_loads(request.body)

        if not data:
            return HttpResponse(status=400)

        if not required_keys_validator(data, ["author", "text"]):
            return HttpResponse(status=400)

        if not string_validator(data.get("text")):
            return HttpResponse(status=400)

        team = Team.get_by_id(team_id)
        if not team:
            return HttpResponse(status=404)

        if event_id:
            event = Event.get_by_id(event_id)
            if not event:
                return HttpResponse(status=404)
            if event.team != team:
                return HttpResponse(status=400)
        else:
            event = None

        if task_id:
            task = Task.get_by_id(task_id)
            if not task:
                return HttpResponse(status=404)
            if task.team != team and task.event != event:
                return HttpResponse(status=400)
        else:
            task = None

        if vote_id:
            vote = Vote.get_by_id(vote_id)
            if not vote:
                return HttpResponse(status=404)
            if vote.team != team and vote.event != event:
                return HttpResponse(status=400)
        else:
            vote = None

        author = CustomUser.get_by_id(data.get("author"))
        if not author:
            return HttpResponse(status=404)

        if comment_id:
            comment = Comment.get_by_id(comment_id)
            if comment:
                if (
                    comment.team == team and comment.event == event and
                    comment.task == task and comment.vote == vote
                   ):
                    comment.update(text=data.get("text"))
                    comment = comment.to_dict()

                    return JsonResponse(comment, status=200)

                return HttpResponse(status=400)

            return HttpResponse(status=404)

        return HttpResponse(status=400)

    def delete(self, request, team_id=None, event_id=None, task_id=None, vote_id=None,
               comment_id=None):
        """Handle DELETE request."""
        team = Team.get_by_id(team_id)
        if not team:
            return HttpResponse(status=404)

        if event_id:
            event = Event.get_by_id(event_id)
            if not event:
                return HttpResponse(status=404)
            if event.team != team:
                return HttpResponse(status=400)
        else:
            event = None

        if task_id:
            task = Task.get_by_id(task_id)
            if not task:
                return HttpResponse(status=404)
            if task.team != team and task.event != event:
                return HttpResponse(status=400)
        else:
            task = None

        if vote_id:
            vote = Vote.get_by_id(vote_id)
            if not vote:
                return HttpResponse(status=404)
            if vote.team != team and vote.event != event:
                return HttpResponse(status=400)
        else:
            vote = None

        if comment_id:
            comment = Comment.get_by_id(comment_id)
            if comment:
                if (
                    comment.team == team and comment.event == event and
                    comment.task == task and comment.vote == vote
                   ):
                    is_deleted = Comment.delete_by_id(comment_id)
                    if is_deleted:
                        return HttpResponse("OK", status=200)

                return HttpResponse(status=400)

            return HttpResponse(status=404)

        return HttpResponse(status=400)
