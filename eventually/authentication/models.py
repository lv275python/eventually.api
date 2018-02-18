"""
This file contains models for the postgresql database.
"""

#pylint: disable=W0223
#The pylint comment above is for ignoring the error below
#Method 'get_full_name' is abstract in class 'AbstractBaseUser'/'get_short_name'
#but is not overridden (abstract-method)

import pickle
from django.conf import settings
from django.core.cache import cache
from django.db import models, IntegrityError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from utils.utils import LOGGER

CACHE_TTL = settings.CACHE_TTL

class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n

        Attributes:
        -----------
        param first_name: Describes first name of the user
        type first_name: str

        param last_name: Describes last name of the user
        type last_name: str

        param middle_name: Describes middle name of the user
        type middle_name: str

        param email: Describes the email of the user
        type email: str

        param password: Describes the password of the user
        type password: str

        param created_at: Describes the date when the user was created. Can't be changed.
        type created_at: int

        param updated_at: Describes the date when the user was modified
        type updated_at: int
    """

    first_name = models.CharField(blank=True, max_length=20)
    middle_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        """
        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        redis_key = 'custom_user_by_id_{0}'.format(user_id)
        if redis_key in cache:
            user = cache.get(redis_key)
            return user
        try:
            user = CustomUser.objects.get(id=user_id)
            cache.set(redis_key, user, CACHE_TTL)
            return user
        except CustomUser.DoesNotExist:
            LOGGER.error("User does not exist")

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str

        :return: user object or None if a user with such ID does not exist
        """
        redis_key = 'custom_user_by_email_{0}'.format(email)
        if redis_key in cache:
            user = cache.get(redis_key)
            return user
        try:
            user = CustomUser.objects.get(email=email)
            cache.set(redis_key, user, CACHE_TTL)
            return user
        except CustomUser.DoesNotExist:
            LOGGER.error("User does not exist")

    @staticmethod
    def delete_by_id(_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """

        try:
            user = CustomUser.objects.get(id=_id)
            user.delete()
            redis_key = 'custom_user_by_id_{0}'.format(_id)
            if redis_key in cache:
                cache.delete(redis_key)
            if "all_users" in cache:
                cache.delete("all_users")
            return True
        except CustomUser.DoesNotExist:
            LOGGER.error("User does not exist")

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str

        :param middle_name: middle name of a user
        :type middle_name: str

        :param last_name: last name of a user
        :type last_name: str

        :param email: email of a user
        :type email: str

        :param password: password of a user
        :type password: str

        :return: a new user object which is also written into the DB
        """

        data = {}
        data['first_name'] = first_name if first_name else ''
        data['last_name'] = last_name if last_name else ''
        data['middle_name'] = middle_name if middle_name else ''
        data['email'] = email
        user = CustomUser(**data)
        user.set_password(password)
        try:
            user.save()
            if "all_users" in cache:
                cache.delete("all_users")
            return user
        except (IntegrityError, AttributeError):
            LOGGER.error("Wrong attributes or relational integrity error")

    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'middle_name': 'mn',
        |   'last_name': 'ln',
        |   'email': 'ln@mail.com',
        |   'created_at': 1509393504,
        |   'updated_at': 1509402866,
        |   'is_active:' True
        | }
        """

        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'is_active': self.is_active}

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               is_active=None):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str

        :param middle_name: middle name of a user
        :type middle_name: str

        :param last_name: last name of a user
        :type last_name: str

        :param password: password of a user
        :type password: str

        :param is_active: activation state
        :type is_active: bool

        :return: None
        """

        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if middle_name:
            self.middle_name = middle_name
        if password:
            self.set_password(password)
        if is_active is not None:
            self.is_active = is_active
        self.save()
        if "all_users" in cache:
            cache.delete("all_users")
        redis_key = 'custom_user_by_id_{0}'.format(self.id)
        if redis_key in cache:
            cache.delete(redis_key)

    @staticmethod
    def get_all():
        """
        returns data for json request with querysets of all users
        """
        redis_key = "all_users"
        if redis_key in cache:
            all_users = cache.get(redis_key)
            all_users = pickle.loads(all_users)
            return all_users
        all_users = CustomUser.objects.all()
        cached_all_users = pickle.dumps(all_users)
        cache.set(redis_key, cached_all_users, CACHE_TTL)
        return all_users
