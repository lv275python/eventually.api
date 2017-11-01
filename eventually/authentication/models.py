"""
This file contains models for the postgresql database.
"""

#pylint: disable=W0223
#The pylint comment above is for ignoring the error below
#Method 'get_full_name' is abstract in class 'AbstractBaseUser'/'get_short_name'
#but is not overridden (abstract-method)

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n
        1. first_name: Char with maximum length of 20 chars.
        2. last_name: Char with maximum length of 20 chars.
        3. middle_name: Char with maximum length of 20 chars.
        4. email: email field of max length 20 chars
        5. password: charfield of max length 128 symbols
        6. created_at: DateTimeField. Can't be changed once created
        7. updated_at: DateTimeField

    """

    first_name = models.CharField('first_name', max_length=20)
    middle_name = models.CharField('middle_name', max_length=20)
    last_name = models.CharField('second_name', max_length=20)
    email = models.EmailField('email_address', max_length=40, unique=True)
    password = models.CharField('password', max_length=128)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        """
            This magic method is redefined to show first, last name and id of the CustomUser object.
        """
        return '{} {} {}'.format(self.first_name, self.last_name, self.id)

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
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            pass

    @staticmethod
    def create(first_name, middle_name, last_name, email, password):
        """
        :param first_name: first name of a user
        :param middle_name: middle name of a user
        :param last_name: last name of a user
        :param email: email of a user
        :param password: password of a user
        :return: a new user object which is also written into the DB
        """
        user = CustomUser(first_name=first_name,
                          last_name=last_name,
                          middle_name=middle_name,
                          email=email,
                          password=password)
        try:
            user.save()
        except CustomUser.OperationalError():
            pass
        return user

    def myattr_to_dict(self):
        """
        :return: manually-defined attributes of the object. Inherited attributes aren't shown.
        :example: {'id': 8, 'first_name': 'fn', 'middle_name': 'mn',
            'last_name': 'ln', 'email': 'ln@mail.com', 'password': '2',
            'created_at': '1509393504', 'updated_at': '1509402866'}

        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'created_at': int(self.created_at.timestamp()), #not multiplying by 1000
            'updated_at': int(self.updated_at.timestamp())
            }

    #'FIXME: rewrite docs'
    def update(self,
               first_name=False,
               last_name=False,
               middle_name=False,
               email=False,
               password=False):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: <str> User's first name
        :param last_name: <str> User's last name
        :param middle_name: <str> User's middle
        :param email: <str> User's  email
        :param password: <str> User's password
        :return: returns True if object updated or False if parameters were incorrect
        """
        user = CustomUser.get_by_id(self.id)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.first_name = last_name
        if middle_name:
            user.middle_name = middle_name
        if email:
            user.email = email
        if password:
            user.password = password
        user.save()
        return True
