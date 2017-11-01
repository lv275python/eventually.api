"""

CustomProfile model
===================

This module implements class that represents the users profile.

"""

from django.db import models
from django.db import IntegrityError


class CustomProfile(models.Model):
    """
    .. class:: CustomProfile

    Describing of profile untity.

    Attributes:
    ===========
        :param hobby: Describes what the user likes.
        :type hobby: TextField
        :param photo: User's photo.
        :type photo: CharField
        :param birthday: User's birthday.
        :type birthday: DateField
        :param create_date: The date when the
                            certain profile was created.
        :type: create_date: DateTimeField
        :param update_date: The date when the certain
                            profile was last time edited.
        :type update_date: DateTimeField

    """
    hobby = models.TextField(max_length=1024, blank=True)
    photo = models.CharField(max_length=30, null=True, blank=True)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Magic method that returns string representation of
        profile instance object.
        :return: profile hobby, profile photo, profile birthday
        """

        return "{} {} {}".format(self.name, self.description, self.status)

    @staticmethod
    def create(hobby='', photo='', birthday=''):
        '''
        Static method that create new CustomProfile object

        :param hobby: Describes what the user likes
        :param photo: User photo
        :param birthday: User birthday

        :return: new created field or None

        '''
        profile = CustomProfile()
        profile.hobby = hobby
        profile.photo = photo
        profile.birthday = birthday
        try:
            profile.save()
            return profile
        except (ValueError, IntegrityError):
            pass

    @staticmethod
    def get_by_id(profile_id):
        """
        Static method that returns profile objects
            according to the accepted id.

        :param profile_id: Unique identificator of profile.
        :type profile_id: integer
        :return: profile object or None

        """
        try:
            profile = CustomProfile.objects.get(id=profile_id)
            return profile
        except CustomProfile.DoesNotExist:
            pass

    @staticmethod
    def delete_by_id(profile_id):
        """
        Static method that removes profile object according to the accepted id.
        :param event_id: Unique identificator of profile.
        :type event_id: integer
        :return: profile object or None if profile does not exist
        """
        try:
            profile = CustomProfile.objects.get(id=profile_id)
            profile.delete()
            return profile
        except (CustomProfile.DoesNotExist, AttributeError):
            pass

    def to_dict(self):
        """
        Method that converts profile onject to dictionary.

        :return: dictionary with information about user

        :Example:
        | {
        |    'id': 3,
        |    'hobby': 'boxing',
        |    'photo': 'i am',
        |    'birthday': 1509539867,
        |    'created_at': 1509539867,
        |    'updated_at': 1509539867,
        | }
        """

        return{
            'id': self.id,
            'hobby': self.hobby,
            'photo': self.photo,
            'birthday': self.int(self.birthday.timestamp()),
            'created_at': self.int(self.created_at.timestamp()),
            'updated_at': self.int(self.updated_at.timestamp())
        }

    def update(self, hobby=None, photo=None, birthday=None):
        '''
        Method that update existed CustomProfile object.

        :param hobby:
        :param photo:
        :param birthday:
        :return: updated field

        '''
        if hobby:
            self.hobby = hobby
        if photo:
            self.photo = photo
        if birthday:
            self.birthday = birthday

        self.save()
