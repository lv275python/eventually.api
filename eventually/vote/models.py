"""
Vote & Answer models
====================

This module implements class that represents the vote and answer models
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from event.models import Event
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Vote(AbstractModel):
    """
        Create Vote model

        Attributes:
        ===========

            :param event: foreign key on model Event
            :type event:integer

            :param is_active: active vote or end
            :type is_active: boolean

            :param is_extended: opportunity write your own variant
            :type is_extended: boolean

            :param title: title of vote
            :type title: string

            :param vote_type: type of vote - we can choose one answer or many
            :type vote_type: string

            :param create_at: The date when the ertain event was created
            :type create_at: datetime

            :param update_at: The date when the certain event was last time edited
            :type update_at: datetime
    """

    MULTI_CHOICES = (
        (0, 'One'),
        (1, 'Multi'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_extended = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    vote_type = models.IntegerField(choices=MULTI_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that return Vote object in dictionary

        :return:models-fields in dictionary

        :Example:
         | {
         |     'id': 13,
         |     'event':1,
         |     'is_active': True,
         |     'is_extended': True,
         |     'title': 'Title of vote',
         |     'type': 0,
         |     'created_at': 1509540116,
         |     'updated_at': 1509540116,
         | }
        """
        return {
            'id': self.id,
            'event': self.event.id,
            'is_active': self.is_active,
            'is_extended': self.is_extended,
            'title': self.title,
            'vote_type': self.vote_type,
            'create_at': int(self.create_at.timestamp()),
            'update_at': int(self.update_at.timestamp()),
        }


    @staticmethod
    def create(event, is_active=True, is_extended=True, title="", vote_type=1):
        """
        Static method that create new Vote object

        :param event: foreign key on model Event. Is required
        :type event: integer

        :param is_active: active vote or end
        :type is_active: boolean

        :param is_extended: opportunity write your own variant
        :type is_extended: boolean

        :param title: title of vote
        :type title: string

        :param vote_type: type of vote - we can choose one answer or many
        :type vote_type: integer

        :return: new created object or None
        """
        vote = Vote(event=event,
                    is_active=is_active,
                    is_extended=is_extended,
                    title=title,
                    vote_type=vote_type)

        try:
            vote.save()
            return vote
        except (ValueError, IntegrityError):
            LOGGER.error('Value or integrity error error was raised')

    def update(self, is_active=None, is_extended=None, title=None, vote_type=None):
        """
        Method that update existed Vote object

        :param is_active: active vote or end
        :type is_active: boolean

        :param is_extended:
        :type is_extended: boolean

        :param title: title of vote
        :type title: string

        :param vote_type: type of vote - we can choose one answer or many
        :type vote_type: string

        :return: none
        """

        if is_active:
            self.is_active = is_active
        if is_extended:
            self.is_extended = is_extended
        if title:
            self.title = title
        if vote_type:
            self.vote_type = vote_type

        self.save()

class Answer(AbstractModel):
    """
        Create Answer model, that has variants to choose in Vote

        Attributes:
        ===========

        :param vote: foreign key of vote
        :type vote: integer

        :param text: variant to choose in vote
        :type text: string

        :param members: Describing relations between team and members of team.
        :type members: integer

        :param create_at: The date when the ertain event was created
        :type create_at: datetime

        :param update_at: The date when the certain event was last time edited
        :type update_at: datetime
    """
    vote = models.ForeignKey(Vote, null=True)
    text = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that return Answer object in dictionary

        :return:models-fields in dictionary

        :Example:
         | {
         |     'id': 12,
         |     'vote': 13,
         |     'text': 'My text',
         |     'members' : [1, 3],
         |     'created_at': 1509540116,
         |     'updated_at': 1509540116,
         | }
        """
        return {
            'id': self.id,
            'vote': self.vote.id,
            'text': self.text,
            'members': [members.id for members in self.members.all()] if self.members else [],
            'create_at': int(self.create_at.timestamp()),
            'update_at': int(self.create_at.timestamp()),
        }

    @staticmethod
    def create(members, vote, text=''):
        """
        Static method that create new Answer object

        :param members: id of members
        :type members: list of integers

        :param vote: foreign key of vote
        :type vote: integer

        :param text: variant to choose in vote
        :type text: string

        :return: new created object or None
        """
        answer = Answer()
        answer.vote = vote
        answer.text = text

        try:
            answer.save()
            answer.members.add(*members)
            return answer
        except (ValueError, IntegrityError, TypeError):
            LOGGER.error('Value or integrity error error was raised')

    def update(self, members=None, text=None):
        """
        Method that update existed Answer object

        :param members: id of members
        :type members: list of integers

        :param text: variant to choose in vote
        :type text: string

        :return: none
        """
        if members is not None:
            self.members = members
        if text:
            self.text = text
        self.save()
