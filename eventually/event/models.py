"""
Event model
===========

This module implements class that represents the event entity.
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from team.models import Team
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Event(AbstractModel):
    """
    Describing of event entity.

    Attributes:
    ===========

        :param team: Foreign key on the certain Team model.
        :type team: integer

        :param owner: Foreign key on the certain CustomUser model.
        :type owner: integer

        :param name: Name of the certain event.
        :type name: string

        :param description: Describing core concepts and
                            goals of the event.
        :type description: string

        :param start_at: The date and the time
                         when the event will occur.
        :type start_at: datetime

        :param create_date: The date when the
                            certain event was created.
        :type: create_date: datetime

        :param update_date: The date when the certain
                            event was last time edited.
        :type update_date: datetime

        :param duration: The period of time while event will be occur.
        :type duration: timedelta

        :param longitude: The longitude coordinates
                          of event's location.
        :type longitude: float

        :param latitude: The latitude coordinates
                         of event's location.
        :type latitude: float

        :param budget: The money amount required for the event.
        :type budget: integer

        :param status: The number that points to the certain.
                       stage of the event processing.
        :type status: integer
    """

    STATUS_CHOICES = (
        (0, 'draft'),
        (1, 'published'),
        (2, 'going'),
        (3, 'finished')
    )

    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField(null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    budget = models.IntegerField(null=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)


    def to_dict(self):
        """
        Method that converts event object to dictionary.

        :return: dictionary with event's information

        :Example:

        | {
        |    'id': 4,
        |    'team': 23,
        |    'owner': 12
        |    'name': 'example',
        |    'description': 'description',
        |    'start_at': 1509539867,
        |    'created_at': 1509539867,
        |    'updated_at': 1509539867,
        |    'duration': 124234,
        |    'longitude': 7.03125,
        |    'latitude': 21.105,
        |    'budget': 100,
        |    'status': 0,
        | }
        """

        return {
            'id': self.id,
            'team': self.team.id,
            'name': self.name,
            'owner': self.owner.id if self.owner else None,
            'description': self.description,
            'start_at': int(self.start_at.timestamp()) if self.start_at else None,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'duration': self.duration.seconds if self.duration else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'latitude': float(self.latitude) if self.latitude else None,
            'budget': self.budget,
            'status': self.status
        }


    @staticmethod
    def create(team, owner, name=None, description='', start_at=None,
               duration=None, longitude=None, latitude=None, budget=None,
               status=0):
        """
        Static method that creates instance of Event class and creates database
        row with the accepted info.

        :param team: Certain Team's object. Is required.
        :type team: Team model

        :param owner: Certain CustomUser's object. Is required.
        :type owner: CustomUser model

        :param name: Name of the certain event.
        :type name: string

        :param description: Describing core concepts and
                            goals of the event.
        :type description: string

        :param start_at: The date and the time
                         when the event will occur.
        :type start_at: datetime

        :param duration: The period of time while event will be occur.
        :type duration: timedelta

        :param longitude: The longitude coordinates
                          of event's location.
        :type longitude: float

        :param latitude: The latitude coordinates
                         of event's location.
        :type latitude: float

        :param budget: The money amount required for the event.
        :type budget: integer

        :param status: The number that points to the certain.
                       stage of the event processing.
        :type status: integer

        :return: event object or None if event have not created
        """

        event = Event()
        event.name = name
        event.description = description
        event.start_at = start_at
        event.duration = duration
        event.longitude = longitude
        event.latitude = latitude
        event.budget = budget
        event.status = status

        try:
            event.team = team
            event.owner = owner
            event.save()
            return event
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def update(self, owner=None, name=None, description=None, start_at=None,
               duration=None, longitude=None, latitude=None, budget=None,
               status=None):
        """
        Method that updates event object according to the accepted info.

        :param name: Name of the certain event.
        :type name: string

        :param owner: Certain CustomUser's object. Is required.
        :type owner: CustomUser model

        :param description: Describing core concepts and
                            goals of the event.
        :type description: string

        :param start_at: The date and the time
                         when the event will occur.
        :type start_at: datetime

        :param duration: The period of time while event will be occur.
        :type duration: timedelta

        :param longitude: The longitude coordinates
                          of event's location.
        :type longitude: float

        :param latitude: The latitude coordinates
                         of event's location.
        :type latitude: float

        :param budget: The money amount required for the event.
        :type budget: integer

        :param status: The number that points to the certain.
                       stage of the event processing.
        :type status: integer

        :return: None
        """

        if owner:
            self.owner = owner
        if name:
            self.name = name
        if description:
            self.description = description
        if start_at:
            self.start_at = start_at
        if duration:
            self.duration = duration
        if longitude:
            self.longitude = longitude
        if latitude:
            self.latitude = latitude
        if budget:
            self.budget = budget
        if status:
            self.status = status

        self.save()
