"""
Team model
=======================

This module implements class that represents the team entity.
"""
# pylint: disable=arguments-differ
import pickle
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, models
from authentication.models import CustomUser
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER

CACHE_TTL = settings.CACHE_TTL

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
            if "all_teams" in cache:
                cache.delete("all_teams")
            return team
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def add_users(self, members_add):
        """Method that adds members to team"""
        if members_add:
            self.members.add(*members_add)
            redis_key = 'team_by_id_{0}'.format(self.id)
            if redis_key in cache:
                cache.delete(redis_key)
            if "all_teams" in cache:
                cache.delete("all_teams")

    def del_users(self, members_del):
        """Method that removes members from team"""
        if members_del:
            self.members.remove(*members_del)
            redis_key = 'team_by_id_{0}'.format(self.id)
            if redis_key in cache:
                cache.delete(redis_key)
            if "all_teams" in cache:
                cache.delete("all_teams")

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
        redis_key = 'team_by_id_{0}'.format(self.id)
        if redis_key in cache:
            cache.delete(redis_key)
        if "all_teams" in cache:
            cache.delete("all_teams")
        self.save()

    @staticmethod
    def get_all():
        """
        returns querysets of all teams
        """
        redis_key = "all_teams"
        if redis_key in cache:
            all_teams = cache.get(redis_key)
            all_teams = pickle.loads(all_teams)
            return all_teams
        all_teams = Team.objects.all()
        cached_teams = pickle.dumps(all_teams)
        cache.set(redis_key, cached_teams, CACHE_TTL)
        return all_teams

    @staticmethod
    def get_by_id(team_id):
        """
        returns object of Team by id
        """
        redis_key = 'team_by_id_{0}'.format(team_id)
        if redis_key in cache:
            team = pickle.loads(cache.get(redis_key))
            return team
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return None
        cached_team = pickle.dumps(team)
        cache.set(redis_key, cached_team, CACHE_TTL)
        return team
