"""
Event Model Test
================

This module provides complete testing for all Event's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from event.models import Event
from authentication.models import CustomUser
from team.models import Team


TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class EventModelTestCase(TestCase):
    """TestCase for providing Event model testing"""

    def setUp(self):
        """Method that provides preparation before testing Event model's features."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user = CustomUser(id=101,
                                     first_name='john',
                                     last_name='doe',
                                     middle_name='eric',
                                     email='email',
                                     password='123456')
            custom_user.save()

            team = Team(id=101,
                        owner=custom_user,
                        name='barcelona')
            team.save()

            event = Event(id=101,
                          team=team,
                          owner=custom_user,
                          name='football')
            event.save()

            event = Event(id=102,
                          team=team,
                          owner=custom_user,
                          name='football',
                          description='test description',
                          start_at=TEST_TIME,
                          duration=datetime.timedelta(seconds=12000),
                          longitude=-61.523438,
                          latitude=-61.523438,
                          budget=100,
                          status=2)
            event.save()

    def test_event_to_dict(self):
        """Method that tests `to_dict` method of certain Event instance."""

        event = Event.objects.get(id=101)
        expect_event_dict = {
            'id': 101,
            'team': 101,
            'owner': 101,
            'name': 'football',
            'description': '',
            'start_at': None,
            'created_at': 1508044512,
            'updated_at': 1508044512,
            'duration': None,
            'longitude': None,
            'latitude': None,
            'budget': None,
            'status': 0,
        }

        actual_event_dict = event.to_dict()

        self.assertDictEqual(actual_event_dict, expect_event_dict)

    def test_event_all_parameters_to_dict(self):
        """
        Method that tests `to_dict` method of certain Event instance.

        Function tests Event instance with all filled parameters.
        """

        event = Event.objects.get(id=102)
        expected_event_dict = {
            'id': 102,
            'team': 101,
            'owner': 101,
            'name': 'football',
            'description': 'test description',
            'start_at': 1508044512,
            'created_at': 1508044512,
            'updated_at': 1508044512,
            'duration': 12000,
            'longitude': -61.523438,
            'latitude': -61.523438,
            'budget': 100,
            'status': 2,
        }

        actual_event_dict = event.to_dict()

        self.assertDictEqual(actual_event_dict, expected_event_dict)

    def test_event_success_get_by_id(self):
        """Method that tests succeeded `get_by_id` method of Event class object."""

        actual_event = Event.get_by_id(101)
        expected_event = Event.objects.get(id=101)

        self.assertEqual(actual_event, expected_event)

    def test_event_none_get_by_id(self):
        """Method that tests unsucceeded `get_by_id` method of Event class object."""

        actual_event = Event.get_by_id(123)

        self.assertIsNone(actual_event)

    def test_event_success_create(self):
        """Method that tests succeeded `create` method of Event class object."""

        team = Team.objects.get(id=101)
        owner = CustomUser.objects.get(id=101)
        created_event = Event.create(team=team,
                                     owner=owner,
                                     name='test event name')

        self.assertIsInstance(created_event, Event)

    def test_event_none_create(self):
        """Method that tests unsucceeded `create` method of Event class object."""

        team = Team.objects.get(id=101)
        owner = CustomUser.objects.get(id=101)
        created_event = Event.create(team=team,
                                     owner=owner)

        self.assertIsNone(created_event)

    def test_event_update(self):
        """
        Method that tests `update` method of certain Event instance.

        Test for updating only a few attributes.
        """

        actual_event = Event.objects.get(id=101)

        actual_event.update(name='box', description='updated description')
        expected_event = Event.objects.get(id=101)

        self.assertEqual(actual_event, expected_event)

    def test_event_all_update(self):
        """
        Method that tests `update` method of certain Event instance.

        Test for updating all attributes.
        """

        actual_event = Event.objects.get(id=101)
        new_owner = CustomUser.objects.create(id=201,
                                              email='exp@gmail.com',
                                              password='123')
        actual_event.update(owner=new_owner,
                            name='tennis',
                            description='very fun game',
                            start_at=datetime.datetime(2017, 4, 11, 6, 23, 11),
                            duration=datetime.timedelta(seconds=11000),
                            longitude=-61.523438,
                            latitude=-61.525538,
                            budget=10,
                            status=2)

        self.assertEqual(actual_event.owner, new_owner)
        self.assertEqual(actual_event.name, 'tennis')
        self.assertEqual(actual_event.description, 'very fun game')
        self.assertEqual(actual_event.start_at, datetime.datetime(2017, 4, 11, 6, 23, 11))
        self.assertEqual(actual_event.duration, datetime.timedelta(0, 11000))
        self.assertEqual(actual_event.longitude, -61.523438)
        self.assertEqual(actual_event.latitude, -61.525538)
        self.assertEqual(actual_event.budget, 10)
        self.assertEqual(actual_event.status, 2)

    def test_event_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of Event class object."""

        is_event_delete = Event.delete_by_id(101)
        self.assertTrue(is_event_delete)
        self.assertRaises(Event.DoesNotExist, Event.objects.get, pk=101)

    def test_event_none_delete(self):
        """Method that tests unsucceeded `delete_by_id` method of Event class object."""

        is_event_delete = Event.delete_by_id(188)
        self.assertIsNone(is_event_delete)

    def test_event_repr(self):
        """Method that test `__repr__` magic method of Event instance object."""

        event = Event.objects.get(id=101)
        actual_repr = event.__repr__()

        self.assertEqual(actual_repr, 'Event(id=101)')

    def test_event_str(self):
        """Method that test `__str__` magic method of Event instance object."""

        event = Event.objects.get(id=101)
        actual_str = event.__str__()
        expected_str = "'id': 101, " \
                       "'team': 101, " \
                       "'name': 'football', " \
                       "'owner': 101, " \
                       "'description': '', " \
                       "'start_at': None, " \
                       "'created_at': 1508044512, " \
                       "'updated_at': 1508044512, " \
                       "'duration': None, " \
                       "'longitude': None, " \
                       "'latitude': None, " \
                       "'budget': None, " \
                       "'status': 0"

        self.assertMultiLineEqual(actual_str, expected_str)
