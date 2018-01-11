"""
Comment model
===========

This module implements class that represents the comment entity.
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from event.models import Event
from task.models import Task
from team.models import Team
from vote.models import Vote
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Comment(AbstractModel):
    """
    Comment model that describes comment entity.

    The main idea is to document
    the class with

    :param text: text of comment
    :type text: string with max_length = 1024 symbols

    :param created_at: date of comment's create
    :type  created_at: datetime

    :param updated_at: date of comment's update
    :type updated_at: datetime

    :param team: ForeignKey on the certain Team Model
    :type team: integer

    :param event: ForeignKey on the certain Event Model
    :type event: integer

    :param task: ForeignKey on the certain Task Model
    :type task: integer

    :param vote: ForeignKey on the certain Vote Model
    :type vote: integer

    :param author: ForeignKey on the certain CustomUser Model
    :type author: integer

    :param receiver: ForeignKey on the certain CustomUser Model
    :type receiver: integer

    """

    text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, null=True)
    event = models.ForeignKey(Event, null=True)
    task = models.ForeignKey(Task, null=True)
    vote = models.ForeignKey(Vote, null=True)
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL,
                               related_name='comment_author')
    receiver = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL,
                                 related_name='comment_receiver')

    def to_dict(self):
        """
        Return dictionary with comment's info.

        :return: comment id, comment text, comment create date, comment update date,
                 comment team, comment event, comment task, comment vote, comment author,
                 comment receiver.

        :Example:
        | {
        |     "id": 1,
        |     "text": "simple commit",
        |     "created_at": 1509540116,
        |     "updated_at": 1509540116,
        |     "team": 1,
        |     "event": 22,
        |     "task": 12,
        |     "vote": 11,
        |     "author": 12
        |     "receiver":14
        | }
        """
        return {
            "id": self.id,
            "text": self.text,
            "created_at": int(self.created_at.timestamp()),
            "updated_at": int(self.updated_at.timestamp()),
            "team": self.team.id if self.team else None,
            "event": self.event.id if self.event else None,
            "task": self.task.id if self.task else None,
            "vote": self.vote.id if self.vote else None,
            "author": self.author.id,
            "receiver": self.receiver.id if self.receiver else None
        }

    @staticmethod
    def create(author, text=None, team=None, event=None, task=None, vote=None,
               receiver=None):
        """
        Create comment.

        :param team: Certain's Team's object.
        :type team: Team object

        :param event: Certain's Event's object.
        :type event: Event object

        :param author: Certain's CustomUser object. Is required.
        :type author: CustomUser object

        :param text: text of comment.
        :type text: string

        :param task: Certain's Task object.
        :type task: Task object

        :param vote: Certain's Vote object.
        :type vote: Vote object

        :param receiver: Certain's CustomUser object.
        :type receiver: CustomUser object

        :return: Comment object instance

        """
        comment = Comment()
        comment.team = team
        comment.event = event
        comment.author = author
        comment.text = text
        comment.task = task
        comment.vote = vote
        comment.receiver = receiver
        try:
            comment.save()
            return comment
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def update(self, text=None):
        """
        Update comment's text.

        :param text: - text of comment
        :type text: string

        """
        if text:
            self.text = text

        self.save()
