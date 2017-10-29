from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.dateformat import format
from  datetime import datetime

class customUser(AbstractBaseUser):
    """
        This class represents a basic user, containing only the essential information about the user.\n
        1. first, last and middle names: all Char with maximum length of 20 chars.
        2. email: email field of max length 20 chars
        3. password: charfield of max length 128 symbols
        4. updated_at & created_at fields: DateTimeField.
           created_at can't be changed once created
    """

    #id - already exists
    first_name = models.CharField(('first name'), max_length = 20)
    middle_name = models.CharField(('middle name'), max_length=20)
    last_name = models.CharField(('second name'), max_length=20)
    email = models.EmailField(('email address'), max_length = 40, unique = True)
    password = models.CharField(('password'), max_length = 128)
    updated_at = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add = True, editable = False)

    def __str__(self):
        """
            This magic method is redefined to show first and last name of the customUser object.
        """
        return self.first_name + ' - ' + self.last_name

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: the id of a user which should be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return customUser.objects.get(id=user_id)
        except customUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :return: user object if it existed in the db or Error message
        """
        try:
            user = customUser.get_by_id(user_id)
            user.delete()
            return user

        except AttributeError:
            return 'Error: User with id %s does not exist' % user_id

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
        user = customUser(first_name=first_name,
                          last_name=last_name,
                          middle_name=middle_name,
                          email=email,
                          password=password)
        user.save()
        return user

    #'FIXME: remove 4 methods below? They aren't needed anymore'
    def get_full_name(self):
        """
        :return: first, middle and last name of the created user
        """

        return ('%s, %s, %s') % (self.first_name, self.middle_name, self.last_name)

    def get_email(self):
        """
        :return: email of the user.
        """
        return self.email

    def get_updated_at(self):
        """
        :return: returns last update date in form of a timestamp
        """
        date = format(self.updated_at, u'U')
        return date

    def get_created_at(self):
        """
        :return: creation date of a user record in form of a timestamp
        """
        return format(self.created_at, u'U')

    #'FIXME: which of these to remove? to_dict or myattr_to_dict ?'
    def to_dict(self):
        """
        :return: Returns an object in form of a dictionary. Methods inherited from the parent object are also shown
        """
        return self.__dict__

    def myattr_to_dict(self):
        """
        :return: manually-defined attributes of the object. Inherited attributes aren't shown.
        """
        return {
                'id': self.id,
                'first_name': self.first_name,
                'middle_name': self.middle_name,
                'last_name': self.last_name,
                'email': self.email,
                'password': self.password,
                'created_at': format(self.created_at, u'U'),
                'updated_at': format(self.updated_at, u'U')
                }

    def update(self, **kwargs):
        """
        Updates user profile in the database with the specified parameters. \n
        :param kwargs: takes a list of parameters to be changed but no more than 5.
        :return: returns an updated object
        """
        if len(kwargs) == 0:
            return "Error, no attributes to change, were specified"
        if len(kwargs) > 5:
            return "Error, you specified too many arguments"
        else:
            user = customUser.get_by_id(self.id)
            if 'first_name' in kwargs: user.first_name = kwargs['first_name']
            if 'middle_name' in kwargs: user.middle_name = kwargs['middle_name']
            if 'last_name' in kwargs: user.last_name = kwargs['last_name']
            if 'email' in kwargs: user.email = kwargs['email']
            if 'password' in kwargs: user.password = kwargs['password']
            user.updated_at = datetime.now()
            user.save()
            return user

