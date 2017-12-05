"""
Team model
=======================

This module implements class that represents the team entity.
"""
from django.db import models, IntegrityError
from authentication.models import CustomUser


class Team(models.Model):

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

    def __str__(self):
        """
        Magic method that returns string representation of
        team instance object.

        :return: string with team's information
        """

        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        Magic method that returns representation of
        team instance object.

        :return: string with team's information
        """

        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        Method that converts team object to dictionary.

        :return: dictionary with team's information

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
    def get_by_id(team_id):
        """
        Static method that returns team objects according to the accepted id.
        Return comment, found by id.

        :param team_id: team's id
        :type team_id: int

        :return: Team object instance or None if object does not exist
        """

        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            pass

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
            pass

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
    def delete_by_id(team_id):
        """
        Static method that removes team object according to the accepted id.

        :param team_id: team's id
        :type team_id: int

        :return: True if object succseffull deleted or
                            None if object isnt found
        """
        try:
            team = Team.objects.get(id=team_id)
            team.delete()
            return True
        except (Team.DoesNotExist, AttributeError):
            pass
