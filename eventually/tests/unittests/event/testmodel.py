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

            custom_user = CustomUser(id=101,
                                     first_name='john',
                                     last_name='doe',
                                     middle_name='eric',
                                     email='email',
                                     password='123456')
            custom_user.save()

            team = Team(id=101,
                        owner=custom_user,
                        members=[custom_user], 
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
                          description='test descript',
                          start_at=TEST_TIME,
                          duration=datetime.timedelta(seconds=12000),
                          longitude=-61.523438,
                          latitude=-61.523438,
                          budget=100,
                          status=2)
            event.save()


    def test_event_to_dict(self):
        """Method that tests `to_dict` method of certain Event instance."""

        event = Event.objects.get(pk=101)
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
        event = Event.objects.get(id=102)
        expect_event_dict = {
            'id': 102,
            'team': 101,
            'owner': 101,
            'name': 'football',
            'description': 'test descript',
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

        self.assertDictEqual(actual_event_dict, expect_event_dict)

    def test_event_success_get_by_id(self):
        """Method that tests `get_by_id` method of Event class object."""
        actuall_event = Event.get_by_id(101)
        expected_event = Event.objects.get(id=101)

        self.assertEqual(actuall_event, expected_event)

    def test_event_None_get_by_id(self):
        """Method that tests `get_by_id` method of Event class object."""
        actuall_event = Event.get_by_id(123)

        self.assertIsNone(actuall_event)

    # def test_event_create(self):
    #     """Method that tests `create` method of Event class object."""

    #     event_success1 = Event.create(self.team2,
    #                                   self.custom_user1,
    #                                   name='test',
    #                                   description='test description')
    #     event_success2 = Event.create(self.team2,
    #                                   self.custom_user3,
    #                                   name='test2',
    #                                   description='test2 description',
    #                                   start_at=TEST_TIME,
    #                                   status=1)
    #     with transaction.atomic():
    #         event_error1 = Event.create(self.team1, self.custom_user1)
    #     with transaction.atomic():
    #         event_error2 = Event.create(self.team1, self.custom_user2)

    #     self.assertTrue(event_success1)
    #     self.assertTrue(event_success2)
    #     self.assertFalse(event_error1)
    #     self.assertFalse(event_error2)

    #     with self.assertRaises(TypeError):
    #         Event.create(self.team1, name='test')
    #     with self.assertRaises(TypeError):
    #         Event.create(self.custom_user3, name='test')
    #     with self.assertRaises(TypeError):
    #         Event.create(self.custom_user3)
    #     with self.assertRaises(TypeError):
    #         Event.create(self.team1)

    def test_event_update(self):
        """Method that tests `update` method of certain Event instance."""

        actuall_event = Event.get_by_id(101)

        actuall_event.update(name='box', description='updated description')
        expected_event = Event.objects.get(id=101)

        self.assertEqual(actuall_event, expected_event)
    def test_event_all_update(self):
        """Method that tests `update` method of certain Event instance."""

        actuall_event = Event.get_by_id(101)
        new_owner = CustomUser.objects.create(id=201,
                                              email='exp@gmail.com',
                                              password='123')

        actuall_event.update(owner=new_owner,
                             name='tenis',
                             description='very fun game',
                             start_at=TEST_TIME,
                             duration=datetime.timedelta(seconds=11000),
                             longitude=-61.523438,
                             latitude=-61.523438,
                             budget=10,
                             status=2)

        self.assertEqual(actuall_event.owner, new_owner)
        self.assertEqual(actuall_event.name, 'tenis')
        self.assertEqual(actuall_event.description, 'very fun game')
        self.assertEqual(actuall_event.start_at, TEST_TIME)
        self.assertEqual(actuall_event.duration, datetime.timedelta(0, 11000))
        self.assertEqual(actuall_event.longitude, -61.523438)
        self.assertEqual(actuall_event.latitude, -61.523438)
        self.assertEqual(actuall_event.budget, 10)
        self.assertEqual(actuall_event.status, 2)

        # event.update(owner=self.custom_user3, name='swimming', start_at=TEST_TIME)
        # self.assertTupleEqual((event.owner, event.name, event.start_at, event.duration),
        #                       (self.custom_user3, 'swimming', TEST_TIME, None))

        # event.update(owner=self.custom_user2,
        #              name='test',
        #              budget=1,
        #              status=0,
        #              duration=datetime.timedelta(seconds=10800))
        # self.assertTupleEqual((event.owner, event.name, event.budget, event.status, event.duration),
        #                       (self.custom_user2, 'test', 1, 0, datetime.timedelta(0, 10800)))

    # def test_event_delete(self):
    #     """Method that tests `delete_by_id` method of Event class object."""

    #     self.assertTrue(Event.delete_by_id(101))
    #     self.assertFalse(Event.get_by_id(101))
    #     self.assertTrue(Event.delete_by_id(103))
    #     self.assertFalse(Event.get_by_id(103))
    #     self.assertFalse(Event.delete_by_id(205))
    #     self.assertFalse(Event.get_by_id(205))
    #     self.assertFalse(Event.delete_by_id(106))
    #     self.assertFalse(Event.delete_by_id(45))
