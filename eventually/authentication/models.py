"""
This file contains models for the postgresql database.
"""

#pylint: disable=W0223
#The pylint comment above is for ignoring the error below
#Method 'get_full_name' is abstract in class 'AbstractBaseUser'/'get_short_name'
#but is not overridden (abstract-method)

from django.db import models, IntegrityError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager



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
        :return: id, first_name, middle_name, last_name,
        email, password, updated_at, created_at, is_active
        """

        return "id: {}, first name:{}, middle name:{}, last name:{},"\
        " email:{}, updated:{}, created:{}, is_active: {}".format(self.id,
                                                                  self.first_name,
                                                                  self.middle_name,
                                                                  self.last_name,
                                                                  self.email,
                                                                  self.updated_at,
                                                                  self.created_at,
                                                                  self.is_active)

    def __repr__(self):
        """
        This magic method is redefined to show first, last name and id of the CustomUser object.
        :return: id, first_name, last_name, is_active
        """

        return 'id: {}, first name: {}, last name: {}, active: {}'.format(
            self.id, self.first_name, self.last_name, self.is_active)

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """

        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str

        :return: user object or None if a user with such ID does not exist
        """

        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            pass

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
            return True
        except CustomUser.DoesNotExist:
            pass

    @staticmethod
    def create(email, password, first_name='', middle_name='', last_name=''):
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

        user = CustomUser(first_name=first_name,
                          last_name=last_name,
                          middle_name=middle_name,
                          email=email)
        user.set_password(password)
        try:
            user.save()
            return user
        except (IntegrityError, AttributeError):
            pass

    def to_dict(self):
        """
        :return: manually-defined attributes of the object. Inherited attributes aren't shown.
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
            'is_active': self.is_active
            }

    def update(self, first_name=None, last_name=None, middle_name=None, email=None, password=None):
        """
        Updates user profile in the database with the specified parameters.\n
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

        :return: returns True if object updated, False if parameters were incorrect
        """

        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if middle_name:
            self.middle_name = middle_name
        if email:
            self.email = email
        if password:
            self.set_password(password)

        self.save()
