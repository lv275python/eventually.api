"""
Curriculum model
================
"""
# pylint: disable=arguments-differ

import pickle
from authentication.models import CustomUser
from django.db import models, IntegrityError
from django.conf import settings
from django.core.cache import cache
from django.contrib.postgres.fields import ArrayField
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER

CACHE_TTL = settings.CACHE_TTL

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

        :param created_at: Describes the date when the curriculum was created
        :type created_at: datetime

        :param updated_at: Describes the date when the curriculum was modified
        :type updated_at: datetime
    """
    name = models.CharField(max_length=50, unique=True, blank=False)
    goals = ArrayField(models.CharField(max_length=30, blank=False), size=8, null=True)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)

    @staticmethod
    def get_by_name(curriculum_name):
        """
        :param curriculum_name: name of a curriculum in the DB
        :type curriculum_id: str
        :return: Curriculum object or None
        """
        redis_key = 'curriculum_by_name_{0}'.format(curriculum_name)
        if redis_key in cache:
            curriculum = pickle.loads(cache.get(redis_key))
            return curriculum
        try:
            curriculum = Curriculum.objects.get(name=curriculum_name)
        except Curriculum.DoesNotExist:
            LOGGER.error("Curriculum does not exist")
            return None
        cached_curriculum = pickle.dumps(curriculum)
        cache.set(redis_key, cached_curriculum, CACHE_TTL)
        return curriculum

    @staticmethod
    def create(name, owner, description='', goals=()):
        """
        Create a new Curriculum object in the database

        :param name: name of the curriculum
        :type name: str

        :param description: description of the curriculum
        :type description: str

        :param goals: list of goals to be achieved during the curriculum
        :type goals: list

        :param owner: Certain CustomUser's object. Is required.
        :type owner: CustomUser model

        :return: Curriculum object or None
        """
        new_curriculum = Curriculum()
        new_curriculum.name = name
        new_curriculum.description = description
        new_curriculum.owner = owner
        new_curriculum.goals = goals

        try:
            new_curriculum.save()
            if "all_curriculums" in cache:
                cache.delete("all_curriculums")
            return new_curriculum
        except (ValueError, IntegrityError):
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
        |   'owner': 1,
        |   'created': 1511386400,
        |   'updated': 1511394690
        | }
        """

        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'goals': self.goals,
                'created': int(self.created_at.timestamp()),
                'updated': int(self.updated_at.timestamp()),
                'owner': self.owner.id
               }

    def update(self, owner, name=None, description=None):
        """
        Updates the curriculum object

        :param name: name for the curriculum object
        :type name: str

        :param owner: Certain CustomUser's object. Is required.
        :type owner: CustomUser model

        :param description: description for the curriculum object
        :type description: str

        :return: True if updated or None
        """

        if name:
            self.name = name
        if description:
            self.description = description
        if owner:
            self.owner = owner
        try:
            self.save()
            redis_key = 'curriculum_by_id_{0}'.format(self.id)
            if redis_key in cache:
                cache.delete(redis_key)
            if "all_curriculums" in cache:
                cache.delete("all_curriculums")
            return True

        except (IntegrityError, AttributeError):
            LOGGER.error("Inappropriate values or relational integrity error")

    @staticmethod
    def get_all():
        """
        returns data for json request with querysets of all curriculums
        """
        redis_key = "all_curriculums"
        if redis_key in cache:
            all_curriculums = cache.get(redis_key)
            all_curriculums = pickle.loads(all_curriculums)
            return all_curriculums
        all_curriculums = Curriculum.objects.all()
        cached_curriculums = pickle.dumps(all_curriculums)
        cache.set(redis_key, cached_curriculums, CACHE_TTL)
        return all_curriculums

    @staticmethod
    def get_by_id(curriculum_id):
        """
        returns object of Curriculum by id
        """
        redis_key = 'curriculum_by_id_{0}'.format(curriculum_id)
        if redis_key in cache:
            curriculum = pickle.loads(cache.get(redis_key))
            return curriculum
        try:
            curriculum = Curriculum.objects.get(id=curriculum_id)
        except Curriculum.DoesNotExist:
            return None
        cached_curriculum = pickle.dumps(curriculum)
        cache.set(redis_key, cached_curriculum, CACHE_TTL)
        return curriculum
