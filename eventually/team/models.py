"""
Team model
=======================

This module implements class that represents the team entity.
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Team(AbstractModel):

    """
    Describing of team entity.
    Attributes:
    ===========

        :param name: Name of the certain team.
        :type name: string

        :param description: Describing core information of the team.
        :type description: string

        :param image: Describing link to image of the team.
        :type description: string

        :param create_date: The date when the certain team was created.
        :type: create_date: datetime

        :param update_date: The date when the certain team was last time edited.
        :type: create_date: datetime

        :param owner: Describing relation between team and owner of team.
        :type owner: int

        :param members: Describing relations between team and members of team.
        :type members: list
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1024, blank=True)
    image = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(CustomUser, related_name='teams')

    def to_dict(self):
        """
        Method that converts team object to dictionary.

        :return: team id, team name, team description, team image,
                 team create date, team update date
                 team owner, team members

        :Example:
            | {
            |   'id': 1,
            |   'name': 'name',
            |   'description': 'desc',
            |   'image': 'img',
            |   'created_at': 1509539536196,
            |   'updated_at': 1509539536196,
            |   'owner': 2,
            |   'members': [1, 4]
            | }
        """

        members = [user.id for user in self.members.all()] if self.members else []

        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'image': self.image,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'owner_id': self.owner.id if self.owner else None,
                'members_id': members}

    @staticmethod
    def create(owner, members, name=None, description='', image=''):
        """
        Static method that creates instance of Team class and creates databes
        row with the accepted info.

        :param owner: team's owner
        :type owner: CustomUser object

        :param members: team's members
        :type members: list

        :param name: team's name
        :type name: str

        :param description: team's description
        :type description: str

        :param image: team's image
        :type image: str

        :return: Team object instance or None if object does not exist
        """

        team = Team()
        team.name = name
        team.description = description
        team.image = image
        team.owner = owner
        try:
            team.save()
            team.members.add(*members)
            return team
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def add_users(self, members_add):
        """Method that adds members to team"""
        if members_add:
            self.members.add(*members_add)

    def del_users(self, members_del):
        """Method that removes members from team"""
        if members_del:
            self.members.remove(*members_del)

    def update(self, owner=None,
               members_del=None,
               members_add=None,
               name=None,
               description=None,
               image=None):
        """
        Method that updates team object according to the accepted info.

        :param owner: team's owner
        :type owner: CustomUser object

        :param members: team's members
        :type members: list

        :param name: team's name
        :type name: str

        :param description: team's description
        :type description: str

        :param image: team's image
        :type image: str
        :return: None
        """
        if owner:
            self.owner = owner
        if members_add:
            self.add_users(members_add)
        if members_del:
            self.del_users(members_del)
        if name:
            self.name = name
        if description:
            self.description = description
        if image:
            self.image = image
        self.save()

    @staticmethod
    def get_all():
        """
        returns querysets of all teams
        """
        all_teams = Team.objects.all()
        return all_teams
