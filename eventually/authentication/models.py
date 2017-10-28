from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.dateformat import format

class customUser(AbstractBaseUser):
    """
        This class represents a basic user, containing only the essential information about the user.\n
        1. first, last and middle names: all Char with maximum length of 20 chars.
        2. email: email field of max length 20 chars
        3. password: charfield of max length 128 symbols
        4. updated_at & created_at fields: DateTimeField. created_at can't be changed once created
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
        :return: creation date in form of a timestamp
        """
        return format(self.created_at, u'U')

    #'FIXME: add methods to work with the object'