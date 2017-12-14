"""
Abstract model
===========

This module implements abstract class.
"""
from abc import abstractmethod
from django.db import models
from utils.utils import LOGGER


class AbstractModel(models.Model):
    """Model that describes abstract entity."""

    class Meta:
        abstract = True

    def __str__(self):
        """
        Show all information about object.

        :return: all info about object

        """
        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        Show class and id of object.

        :return: class, id

        """
        return f'{self.__class__.__name__}(id={self.id})'

    @classmethod
    def get_by_id(cls, obj_id):
        """
        Return object, found by id.

        :param obj_id: object's id
        :type obj_id: integer

        :return: object instance or None if object does not exist

        """
        try:
            obj = cls.objects.get(id=obj_id)
            return obj
        except cls.DoesNotExist as err:
            LOGGER.error(f'Certain {cls.__name__} with id={obj_id} does not exist. {err}')

    @classmethod
    def delete_by_id(cls, obj_id):
        """
        Delete object, found by id.

        :param obj_id: - object's id
        :type obj_id: integer

        :return: True if object seccessfully deleted or
                 None if object does not exist

        """
        try:
            obj = cls.objects.get(id=obj_id)
            obj.delete()
            return True
        except (cls.DoesNotExist, AttributeError) as err:
            LOGGER.error(f'Certain {cls.__name__} with id={obj_id} does not exist. {err}')

    @staticmethod
    @abstractmethod
    def create(*args, **kwargs):
        """Create object."""

    @abstractmethod
    def update(self, **kwargs):
        """Update objects parameters."""

    @abstractmethod
    def to_dict(self):
        """Return dictionary with object's info."""
