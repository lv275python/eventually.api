"""
CustomProfile model
===================

This module implements class that represents the users profile.
"""

from django.db import models, IntegrityError
from authentication.models import CustomUser


class CustomProfile(models.Model):
    """
    Describing of profile untity.

    Attributes:
    ===========
        :param hobby: Describes what the user likes.
        :type hobby: string

        :param photo: User's photo.
        :type photo: string

        :param birthday: User's birthday.
        :type birthday: Date

        :param create_date: The date when the certain profile was created.
        :type: create_date: Date

        :param update_date: The date when the certain profile was last time edited.
        :type update_date: Date
    """
    user = models.OneToOneField(CustomUser, null=True)
    hobby = models.CharField(max_length=1024, blank=True)
    photo = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomProfile.

        :return: profile id, profile user, profile hobby, profile photo,
                 profile birthday, create date, update date
        """

        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomProfile object.

        :return: class, id
        """

        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def create(user, hobby='', photo='', birthday=None):
        '''
        Static method that create new CustomProfile object

        :param hobby: Describes what the user likes
        :type hobby: string

        :param photo: User photo
        :type photo: string

        :param birthday: User birthday
        :type birthday: Date

        :param user:  Certain CustomUser object. Is required.
        :type user: CustomUser model.

        :return: new created field or None

        '''
        profile = CustomProfile()
        profile.user = user
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
        Static method that returns profile objects according to the accepted id.

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

        :param profile_id: PrimaryKey.
        :type profile_id: integer

        :return: profile object or None if profile does not exist
        """
        try:
            profile = CustomProfile.objects.get(id=profile_id)
            profile.delete()
            return True
        except (CustomProfile.DoesNotExist, AttributeError):
            pass

    def to_dict(self):
        """
        Method that converts profile onject to dictionary.

        :return: dictionary with information about user

        :Example:
        | {
        |    'id': 3,
        |    'user': 3,
        |    'hobby': 'boxing',
        |    'photo': 'i am',
        |    'birthday': 2010-7-6,
        |    'created_at': 1509539867,
        |    'updated_at': 1509539867,
        | }
        """

        return {'id': self.id,
                'user': self.user.id,
                'hobby': self.hobby[:30],
                'photo': self.photo,
                'birthday': str(self.birthday) if self.birthday else None,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp())}

    def update(self, hobby=None, photo=None, birthday=None):
        '''
        Method that update existed CustomProfile object.

        :param hobby: Describes what the user likes
        :type hobby: string

        :param photo: User photo
        :type photo: string

        :param birthday: User birthday
        :type birthday: Date

        :return: profile object or None if profile have not created
        '''

        if hobby:
            self.hobby = hobby
        if photo:
            self.photo = photo
        if birthday:
            self.birthday = birthday

        self.save()
