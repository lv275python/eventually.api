"""Model for describe Comment entity."""


from django.db import models, IntegrityError
from authentication.models import CustomUser
from event.models import Event
from task.models import Task
from team.models import Team
from vote.models import Vote


class Comment(models.Model):
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
    :type team: integer

    :param task: ForeignKey on the certain Task Model
    :type task: integer

    :param vote: ForeignKey on the certain Vote Model
    :type team: integer

    :param author: ForeignKey on the certain CustomUser Model
    :type team: integer

    """

    text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True)
    task = models.ForeignKey(Task, null=True)
    vote = models.ForeignKey(Vote, null=True)
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """
        Return string value of model's parametrs in understandible format.

        :return: id, text, create date, update date

        """
        return "id: {}, text: {}, created_at: {}, updated_at: {}, " \
               "team_id: {}, event_id: {}, task_id: {}, vote_id: {}, " \
               "author_id: {}".format(self.id,
                                      self.text,
                                      self.created_at,
                                      self.updated_at,
                                      self.team.id,
                                      self.event.id if self.event else None,
                                      self.task.id if self.task else None,
                                      self.vote.id if self.vote else None,
                                      self.author.id)

    def __repr__(self):
        """
        Return string value of model's parametrs in understandible format.

        :return: id, text, create date, update date

        """
        return "{} {}".format(self.id, self.text)

    def to_dict(self):
        """
        Return dictionary with comment's info.

        :return: dictionary with comment's info

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
        | }
        """
        return {
            "id": self.id,
            "text": self.text,
            "created_at": int(self.created_at.timestamp()),
            "updated_at": int(self.updated_at.timestamp()),
            "team": self.team.id,
            "event": self.event.id if self.event else None,
            "task": self.task.id if self.task else None,
            "vote": self.vote.id if self.vote else None,
            "author": self.author.id
        }

    @staticmethod
    def get_by_id(comment_id):
        """
        Return comment, found by id.

        :param comment_id: comment's id
        :type comment_id: integer

        :return: Comment object instance or None if object does not exist

        """
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment
        except Comment.DoesNotExist:
            pass

    @staticmethod
    def create(team, author, text=None, event=None, task=None, vote=None):
        """
        Create comment.

        :param team: Certain's Team's object. Is required.
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

        :return: Comment object instance

        """
        comment = Comment()
        comment.team = team
        comment.event = event
        comment.author = author
        comment.text = text
        comment.task = task
        comment.vote = vote
        try:
            comment.save()
            return comment
        except (ValueError, IntegrityError):
            pass

    def update(self, text=None):
        """
        Update comment's text.

        :param text: - text of comment
        :type text: string

        """
        if text:
            self.text = text

        self.save()

    @staticmethod
    def delete_by_id(comment_id):
        """
        Delete comment, found by id.

        :param comment_id: - comment's id
        :type comment_id: integer

        :return: True if comment seccessfully deleted or
                 None if object does not exist

        """
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return True
        except (Comment.DoesNotExist, AttributeError):
            pass
