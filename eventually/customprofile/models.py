"""
CustomProfile model
===================

This module implements class that represents the users profile.
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class CustomProfile(AbstractModel):
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
            LOGGER.error('Inappropriate value or relational integrity fail')

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
