"""
Curriculum model
================
"""


from django.db import models, IntegrityError
from django.contrib.postgres.fields import ArrayField
from authentication.models import CustomUser
from team.models import Team

class Curriculum(models.Model):
    """
    Curriculum model class
    Attributes:
    ===========
        :param name: name of the curriculum, can't be blank
        :type name: str

        :param description: description of the curriculum
        :type description: str

        :param goals: goals to achieve after completing the curriculum
        :type goals: list

        :param team: id of a team which is studying by the curriculum
        :type name: int

        :param mentors: id of a mentor to control the flow of the curriculum
        :type mentors: int

        param created_at: Describes the date when the curriculum was created, unchangeable
        type created_at: datetime

        param updated_at: Describes the date when the curriculum was modified
        type updated_at: datetime
    """

    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=500, blank=True)
    goals = ArrayField(models.CharField(max_length=20), blank=True)
    teams = models.ManyToManyField(Team, blank=True, related_name='teams')
    mentors = models.ManyToManyField(CustomUser, blank=True, related_name='mentors')
    #To be imported upon the creation of the Assignment model
    #assignments = models.ManyToManyField(Assignment, blank=True, related_name='assignments')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Magic method is redefined to show all information about the Curriculum.
        :return: id, name, description, goals, teams, mentors, created_at, updated_at
        :Example:
         |   "id: 1,
         |   name: reading,
         |   description: shakespeare,
         |   goals: ['B+', 'C1'],
         |   teams: [], mentors: [46],
         |   created: 2017-11-22 21:33:20.089291+00:00,
         |   updated: 2017-11-22 23:51:30.653525+00:00"
        """

        teams = [team.id for team in self.teams.all()] if self.teams else None
        mentors = [mentor.id for mentor in self.mentors.all()] if self.mentors else None

        return('id: {}, name: {}, description: {}, goals: {},'
               'teams: {}, mentors: {}, created: {}, updated: {}').format(self.id,
                                                                          self.name,
                                                                          self.description,
                                                                          self.goals,
                                                                          teams,
                                                                          mentors,
                                                                          self.created_at,
                                                                          self.updated_at)

    def __repr__(self):
        """
        Magic method is redefined to show short information about the Curriculum.
        :return: id, name, goals
        """

        return('id: {}, name: {}, goals: {}').format(self.id, self.name, self.goals)

    @staticmethod
    def get_by_id(curriculum_id):
        """
        :param curriculum_id: id of a curriculum in the DB
        :type curriculum_id: int

        :return: Curriculum object or None
        :Example:
         |   "id: 1,
         |   name: reading,
         |   goals: ['B+', 'C1']"
        """

        try:
            return Curriculum.objects.get(id=curriculum_id)
        except Curriculum.DoesNotExist:
            pass

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
            pass

    @staticmethod
    def delete_by_id(curriculum_id):
        """
        :param curriculum_id: id of a curriculum in the DB
        :type curriculum_id: int

        :return: True or None
        """

        try:
            curriculum = Curriculum.objects.get(id=curriculum_id)
            curriculum.delete()
            return True
        except Curriculum.DoesNotExist:
            pass


    @staticmethod
    def create(name, description=None, goals=None):
        """
        Create a new Curriculum object in the database
        :param name: name of the curriculum
        :type name: str

        :param description: description of the curriculum
        :type description: str

        :param goals: goals of the curriculum
        :type goals: list

        :return: Curriculum object or none
        """
        data = {}
        data['name'] = name
        data['description'] = description if description else ''
        data['goals'] = goals if goals else []
        new_curriculum = Curriculum.objects.create(**data)
        try:
            new_curriculum.save()
            return new_curriculum
        except (IntegrityError, AttributeError):
            pass

    def to_dict(self):
        """
        Make a dict from the Curriculum object
        :return: Curriculum object dictionary
        :Example:
        | {
        |   'id:': 1,
        |   'name:': 'reading',
        |   'description': 'shakespeare',
        |   'goals': ['B+', 'C1'],
        |   'teams': [],
        |   'mentors': [46],
        |   'created': 1511386400,
        |   'updated': 1511394690
        | }
        """

        teams = [team.id for team in self.teams.all()] if self.teams else None
        mentors = [mentor.id for mentor in self.mentors.all()] if self.mentors else None

        return {'id:': self.id,
                'name:': self.name,
                'description': self.description,
                'goals': self.goals,
                'teams': teams,
                'mentors': mentors,
                'created': int(self.created_at.timestamp()),
                'updated': int(self.updated_at.timestamp())
               }


    def update(self, name=None, description=None):
        """
        Updates the curriculum object
        :param name: name for the curiculum object
        :type name: str

        :param description: description for the curiculum object
        :type description: str

        :return: True if updated or None
        """

        if name:
            self.name = name
        if description:
            self.description = description
        try:
            self.save()
            return True
        except (IntegrityError, AttributeError):
            pass


    def update_goals(self, add=None, replace=None, delete=()):
        """
        Updates goals in the Curriculum app
        :param addgoals: new goals to add
        :type addgoals: list

        :param replacegoals: existing goals to be replaced by new ones
        :type replacegoals: dict

        :param deletegoals: existing goals to be deleted
        :type deletegoals: tuple

        :return: True if goals updated or False
        """

        goals = self.goals
        changed = False
        if add:
            self.goals = self.goals + add
            changed = True
        if replace:
            for goal in replace:
                if goal in goals:
                    goal_index = goals.index(goal)
                    goals[goal_index] = replace.get(goal)
                    changed = True
        if delete:
            for goal_to_delete in delete:
                if goal_to_delete in goals:
                    goals.remove(goal_to_delete)
                    changed = True
        try:
            self.save()
            return True if changed else None
        except (IntegrityError, AttributeError):
            pass
