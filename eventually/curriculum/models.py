"""
Curriculum model
================
"""
# pylint: disable=arguments-differ

from authentication.models import CustomUser
from django.db import models, IntegrityError
from django.contrib.postgres.fields import ArrayField
from team.models import Team
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Curriculum(AbstractModel):
    """
    Curriculum model class
    Attributes:
    ===========
        :param name: name of the curriculum, can't be blank
        :type name: str

        :param goals: list of goals to be achieved during the curriculum
        :type goals: list

        :param description: description of the curriculum
        :type description: str

        :param mentors: id of mentors to control the flow of the curriculum
        :type mentors: int

        :param team: id of teams which are studying by the curriculum
        :type name: int

        :param created_at: Describes the date when the curriculum was created
        :type created_at: datetime

        :param updated_at: Describes the date when the curriculum was modified
        :type updated_at: datetime
    """

    name = models.CharField(max_length=50, unique=True, blank=False)
    goals = ArrayField(models.CharField(max_length=30, blank=False), size=8, null=True)
    description = models.TextField(max_length=500, blank=True)
    mentors = models.ManyToManyField(CustomUser, blank=False, related_name='mentors')
    team = models.ForeignKey(Team, null=True, related_name='team')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_by_name(curriculum_name):
        """
        :param curriculum_name: name of a curriculum in the DB
        :type curriculum_id: str
        :return: Curriculum object or None
        """

        try:
            return Curriculum.objects.get(name=curriculum_name)
        except Curriculum.DoesNotExist:
            LOGGER.error("Curriculum does not exist")


    @staticmethod
    def create(name, description='', goals=(), team=None, mentors=()):
        """
        Create a new Curriculum object in the database

        :param name: name of the curriculum
        :type name: str

        :param description: description of the curriculum
        :type description: str

        :param goals: list of goals to be achieved during the curriculum
        :type goals: list

        :param team: id of teams which study the curriculum
        :type team: list

        :param mentors: one or more mentors to direct the curriculum
        :type mentors: list

        :return: Curriculum object or none
        """

        try:
            new_curriculum = Curriculum.objects.create(name=name,
                                                       description=description,
                                                       goals=goals,
                                                       team=team)
            new_curriculum.save()
            new_curriculum.mentors.add(*mentors)
            return new_curriculum
        except IntegrityError:
            LOGGER.error("Relational integrity error")


    def to_dict(self):
        """
        Make a dict from the Curriculum object
        :return: Curriculum object dictionary
        :Example:
        | {
        |   'id:': 1,
        |   'name:': 'reading',
        |   'description': 'shakespeare',
        |   'goals': ['Be a Senior dev'],
        |   'team': 'Team(id=1)',
        |   'mentors': [46, 54],
        |   'created': 1511386400,
        |   'updated': 1511394690
        | }
        """

        mentors = sorted([mentor.id for mentor in self.mentors.all()] if self.mentors else None)

        return {'id:': self.id,
                'name:': self.name,
                'description': self.description,
                'goals': self.goals,
                'team': self.team,
                'mentors': mentors,
                'created': int(self.created_at.timestamp()),
                'updated': int(self.updated_at.timestamp())
               }


    def update(self, name=None, description=None, team=None, mentors=()):
        """
        Updates the curriculum object

        :param name: name for the curriculum object
        :type name: str

        :param description: description for the curriculum object
        :type description: str

        :param team: id of teams which study the curriculum
        :type team: list

        :param mentors: one or more mentors to add to the curriculum
        :type mentors: tuple

        :return: True if updated or None
        """

        if name:
            self.name = name
        if description:
            self.description = description
        if team:
            self.team = team
        if mentors:
            self.mentors.add(*mentors) # Add method to delete mentors
        try:
            self.save()
            return True
        except (IntegrityError, AttributeError):
            LOGGER.error("Inappropriate values or relational integrity error")
