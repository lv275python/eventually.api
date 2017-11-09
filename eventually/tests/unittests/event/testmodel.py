"""
Event Model Test
================

This module provides complete testing for all Event's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from django.db import transaction
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

            self.custom_user1 = CustomUser(id=101,
                                           first_name='john',
                                           last_name='doe',
                                           middle_name='eric',
                                           email='email',
                                           password='123456')
            self.custom_user1.save()
            self.custom_user2 = CustomUser(id=102,
                                           first_name='andy',
                                           last_name='smith',
                                           middle_name='mor',
                                           email='exmpl@gmail.com',
                                           password='456789')
            self.custom_user2.save()
            self.custom_user3 = CustomUser(id=103,
                                           first_name='max',
                                           last_name='lenon',
                                           middle_name='poul',
                                           email='test@gmail.com',
                                           password='147258')
            self.custom_user3.save()

            self.team1 = Team(id=101, name='barcelona')
            self.team1.save()
            self.team2 = Team(id=102, name='chelsea')
            self.team2.save()
            self.event1 = Event(id=101,
                                team=self.team1,
                                owner=self.custom_user1,
                                name='football')
            self.event1.save()
            self.event2 = Event(id=102,
                                team=self.team2,
                                owner=self.custom_user2,
                                name='party',
                                description='test party description',
                                duration=datetime.timedelta(seconds=10800),
                                start_at=datetime.datetime(2015, 11, 8, 2, 45, 12),
                                latitude=-151.523438,
                                budget=100,
                                status=2)
            self.event2.save()
            self.event3 = Event(id=103,
                                team=self.team2,
                                owner=self.custom_user3,
                                name='python meetup',
                                description='test python meetup description',
                                start_at=TEST_TIME,
                                longitude=52.994950,
                                budget=123,
                                status=3)
            self.event3.save()
            self.event4 = Event(id=104,
                                team=self.team1,
                                owner=self.custom_user2,
                                name='opera',
                                start_at=datetime.datetime(2017, 1, 18, 12, 5, 56),
                                duration=datetime.timedelta(seconds=97200),
                                longitude=10.195313,
                                latitude=133.242188)
            self.event4.save()

    def test_event_to_dict(self):
        """Method that tests `to_dict` method of certain Event instance."""

        test_event_dict1 = {
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

        test_event_dict2 = {
            'id': 102,
            'team': 102,
            'owner': 102,
            'name': 'party',
            'description': 'test party description',
            'start_at': 1446943512,
            'created_at': 1508044512,
            'updated_at': 1508044512,
            'duration': datetime.timedelta(0, 10800),
            'longitude': None,
            'latitude': -151.523438,
            'budget': 100,
            'status': 2,
        }

        test_event_dict3 = {
            'id': 103,
            'team': 102,
            'owner': 103,
            'name': 'python meetup',
            'description': 'test python meetup description',
            'start_at': 1508044512,
            'created_at': 1508044512,
            'updated_at': 1508044512,
            'duration': None,
            'longitude': 52.994950,
            'latitude': None,
            'budget': 123,
            'status': 3,
        }

        test_event_dict4 = {
            'id': 104,
            'team': 101,
            'owner': 102,
            'name': 'opera',
            'description': '',
            'start_at': 1484733956,
            'created_at': 1508044512,
            'updated_at': 1508044512,
            'duration': datetime.timedelta(1, 10800),
            'longitude': 10.195313,
            'latitude': 133.242188,
            'budget': None,
            'status': 0,
        }

        self.assertEqual(self.event1.to_dict(), test_event_dict1)
        self.assertEqual(self.event2.to_dict(), test_event_dict2)
        self.assertEqual(self.event3.to_dict(), test_event_dict3)
        self.assertEqual(self.event4.to_dict(), test_event_dict4)

    def test_event_get_by_id(self):
        """Method that tests `get_by_id` method of Event class object."""

        self.assertEqual(Event.get_by_id(101), self.event1)
        self.assertEqual(Event.get_by_id(102), self.event2)
        self.assertEqual(Event.get_by_id(103), self.event3)
        self.assertEqual(Event.get_by_id(104), self.event4)

    def test_event_create(self):
        """Method that tests `create` method of Event class object."""

        event_success1 = Event.create(self.team2,
                                      self.custom_user1,
                                      name='test',
                                      description='test description')
        event_success2 = Event.create(self.team2,
                                      self.custom_user3,
                                      name='test2',
                                      description='test2 description',
                                      start_at=TEST_TIME,
                                      status=1)
        with transaction.atomic():
            event_error1 = Event.create(self.team1, self.custom_user1)
        with transaction.atomic():
            event_error2 = Event.create(self.team1, self.custom_user2)

        self.assertTrue(event_success1)
        self.assertTrue(event_success2)
        self.assertFalse(event_error1)
        self.assertFalse(event_error2)

        with self.assertRaises(TypeError):
            Event.create(self.team1, name='test')
        with self.assertRaises(TypeError):
            Event.create(self.custom_user3, name='test')
        with self.assertRaises(TypeError):
            Event.create(self.custom_user3)
        with self.assertRaises(TypeError):
            Event.create(self.team1)

    def test_event_update(self):
        """Method that tests `update` method of certain Event instance."""

        event = Event.get_by_id(101)

        event.update(name='box', description='updated description')
        self.assertTupleEqual((event.name, event.description, event.budget),
                              ('box', 'updated description', None))

        event.update(owner=self.custom_user3, name='swimming', start_at=TEST_TIME)
        self.assertTupleEqual((event.owner, event.name, event.start_at, event.duration),
                              (self.custom_user3, 'swimming', TEST_TIME, None))

        event.update(owner=self.custom_user2,
                     name='test',
                     budget=1,
                     status=0,
                     duration=datetime.timedelta(seconds=10800))
        self.assertTupleEqual((event.owner, event.name, event.budget, event.status, event.duration),
                              (self.custom_user2, 'test', 1, 0, datetime.timedelta(0, 10800)))

    def test_event_delete(self):
        """Method that tests `delete_by_id` method of Event class object."""

        self.assertTrue(Event.delete_by_id(101))
        self.assertFalse(Event.get_by_id(101))
        self.assertTrue(Event.delete_by_id(103))
        self.assertFalse(Event.get_by_id(103))
        self.assertFalse(Event.delete_by_id(205))
        self.assertFalse(Event.get_by_id(205))
        self.assertFalse(Event.delete_by_id(106))
        self.assertFalse(Event.delete_by_id(45))
