"""Task Model Test
================

This module provides complete testing for all Task's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from django.db import transaction
from task.models import Task
from event.models import Event
from authentication.models import CustomUser
from team.models import Team


TEST_TIME = datetime.datetime(2017, 2, 2, 12, 00, 12)


class TaskModelTestCase(TestCase):
    """TestCase for providing Event model testing"""

    def setUp(self):
        """Method that provides preparation before testing Event model's features."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            self.custom_user1 = CustomUser(id=111,
                                           first_name='Jared',
                                           last_name='Leto',
                                           middle_name='Joseph',
                                           email='Jared.Leto@gmail.com',
                                           password='30sectomrs')
            self.custom_user1.save()
            self.custom_user2 = CustomUser(id=112,
                                           first_name='Jack',
                                           last_name='Nicholson',
                                           middle_name='Joseph',
                                           email='Jack.Nicholson@gmail.com',
                                           password='CuckoosNest75')
            self.custom_user2.save()
            self.custom_user3 = CustomUser(id=113,
                                           first_name='Anthony',
                                           last_name='Hopkins',
                                           middle_name='Philip',
                                           email='test@gmail.com',
                                           password='147258')
            self.custom_user3.save()

            self.team1 = Team(id=111, name='Coldplay')
            self.team1.save()
            self.team2 = Team(id=112, name='Twenty One Pilots')
            self.team2.save()
            self.event1 = Event(id=111,
                                team=self.team2,
                                owner=self.custom_user2,
                                name='party',
                                description='test party description',
                                duration=datetime.timedelta(seconds=10800),
                                start_at=datetime.datetime(2015, 11, 8, 2, 45, 12),
                                latitude=-151.523438,
                                budget=100,
                                status=2)
            self.event1.save()
            self.event2 = Event(id=112,
                                team=self.team2,
                                owner=self.custom_user3,
                                name='python meetup',
                                description='test python meetup description',
                                start_at=TEST_TIME,
                                longitude=52.994950,
                                budget=123,
                                status=3)
            self.event2.save()
            self.task1 = Task(id=11,
                              event=self.event1,
                              users=[self.custom_user1, self.custom_user3],
                              title='Potato thing',
                              description='My awesome task, give me potato',
                              status=0)
            self.task1.save()
            self.task2 = Task(id=12,
                              event=self.event2,
                              users=[self.custom_user2],
                              title='Tomato thing',
                              description='My awesome task, give me tomato',
                              status=1)
            self.task2.save()

    def test_task_to_dict(self):
        """Method that tests `to_dict` method of certain Task instance."""

        test_task_dict1 = {
            'id': 11,
            'title': 'Potato thing',
            'description': 'My awesome task, give me potato',
            'status': 0,
            'created_at': 1486029612,
            'updated_at': 1486029612,
            'event': 111,
            'users': [111, 113]
        }

        test_task_dict2 = {
            'id': 12,
            'title': 'Tomato thing',
            'description': 'My awesome task, give me tomato',
            'status': 1,
            'created_at': 1486029612,
            'updated_at': 1486029612,
            'event': 112,
            'users': [112]
        }



        self.assertEqual(self.task1.to_dict(), test_task_dict1)
        self.assertEqual(self.task2.to_dict(), test_task_dict2)


    def test_task_get_by_id(self):
        """Method that tests `get_by_id` method of Event class object."""

        self.assertEqual(Task.get_by_id(11), self.task1)
        self.assertEqual(Task.get_by_id(12), self.task2)


    def test_task_create(self):
        """Method that tests `create` method of Task class object."""

        task_success1 = Task.create(self.event1,
                                    [self.custom_user2, self.custom_user3],
                                    title='test',
                                    description='test description',
                                    status=0)
        task_success2 = Task.create(self.event2,
                                    [self.custom_user3],
                                    title='test2',
                                    description='test2 description',
                                    status=1)
        with transaction.atomic():
            task_error1 = Task.create(self.event1, self.custom_user1)
        with transaction.atomic():
            task_error2 = Task.create(self.event2, self.custom_user3)

        self.assertTrue(task_success1)
        self.assertTrue(task_success2)
        self.assertFalse(task_error1)
        self.assertFalse(task_error2)

        with self.assertRaises(TypeError):
            Task.create(self.team1, title='test')
        with self.assertRaises(TypeError):
            Task.create(self.custom_user3, title='test')
        with self.assertRaises(TypeError):
            Task.create(self.custom_user3)
        with self.assertRaises(TypeError):
            Task.create(self.team1)

    def test_task_update(self):
        """Method that tests `update` method of certain Event instance."""

        task = Task.get_by_id(11)

        task.update(title='Hello, i`m title', description='Hello from the other side')
        self.assertTupleEqual((task.title, task.description),
                              ('Hello, i`m title', 'Hello from the other side'))

        task.update(event=self.event2, title='Hello, i`m best title', status=2)
        self.assertTupleEqual((task.event, task.title, task.status),
                              (self.event2, 'Hello, i`m best title', 2))

    def test_task_delete(self):
        """Method that tests `delete_by_id` method of Task class object."""

        self.assertTrue(Task.delete_by_id(11))
        self.assertTrue(Task.delete_by_id(12))
        self.assertFalse(Task.delete_by_id(205))
        self.assertFalse(Task.delete_by_id(106))
