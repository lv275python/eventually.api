"""
Event model
===========

This module implements class that represents the event entity.
"""

from django.db import models
from django.db import IntegrityError


class Event(models.Model):
    """
    Describing of event entity.

    Attributes:
    ===========

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
        :type longitude: decimal

        :param latitude: The latitude coordinates
                         of event's location.
        :type latitude: decimal

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
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField(null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    budget = models.IntegerField(null=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    def __str__(self):
        """
        Magic method that returns string representation of
        event instance object.

        :return: event name, event description, event status
        """

        return "{} {} {}".format(self.name, self.description, self.status)

    def to_dict(self):
        """
        Method that converts event object to dictionary.

        :return: dictionary with event's information

        :Example:

        | {
        |    'id': 4,
        |    'name': 'example',
        |    'description': 'decsp',
        |    'start_at': 1509539867,
        |    'created_at': 1509539867,
        |    'updated_at': 1509539867,
        |    'longitude': 7.03125,
        |    'latitude': 21.105,
        |    'budget': 100,
        |    'status': 0
        | }
        """

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_at': int(self.start_at.timestamp()),
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'duration': self.duration,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'budget': self.budget,
            'status': self.status
        }

    @staticmethod
    def get_by_id(event_id):
        """
        Static method that returns event objects according to the accepted id.

        :param event_id: Unique identificator of event.
        :type event_id: integer

        :return: event object or None if event does not exist
        """

        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            pass

    @staticmethod
    def create(name=None, description='', start_at=None, duration=None,
               longitude=None, latitude=None, budget=None, status=0):
        """
        Static method that creates instance of Event class and creates database
        row with the accepted info.

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
        :type longitude: decimal

        :param latitude: The latitude coordinates
                         of event's location.
        :type latitude: decimal

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
            event.save()
            return event
        except (ValueError, IntegrityError):
            pass

    def update(self, name=None, description=None, start_at=None, duration=None,
               longitude=None, latitude=None, budget=None, status=None):
        """
        Method that updates event object according to the accepted info.

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
        :type longitude: decimal

        :param latitude: The latitude coordinates
                         of event's location.
        :type latitude: decimal

        :param budget: The money amount required for the event.
        :type budget: integer

        :param status: The number that points to the certain.
                       stage of the event processing.
        :type status: integer

        :return: None
        """

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

    @staticmethod
    def delete_by_id(event_id):
        """
        Static method that removes event object according to the accepted id.

        :param event_id: Unique identificator of event.
        :type event_id: integer

        :return: event object or None if event does not exist
        """

        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return True
        except (Event.DoesNotExist, AttributeError):
            pass
