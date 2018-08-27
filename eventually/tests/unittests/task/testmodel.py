"""Task Model Test
================

This module provides complete testing for all Task's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from suggestedtopics.models import cache as tested_cache
from task.models import Task
from event.models import Event
from authentication.models import CustomUser
from team.models import Team
from django.core.cache import cache


TEST_TIME = datetime.datetime(2017, 2, 2, 12, 00, 12)

class TaskModelTestCase(TestCase):
    """TestCase for providing Task model testing"""

    def setUp(self):
        """Method that provides preparation before testing Task model's features."""

        cache.clear()

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user_first = CustomUser(id=11,
                                           first_name='Jared',
                                           last_name='Leto',
                                           middle_name='Joseph',
                                           email='Jared.Leto@gmail.com',
                                           password='30sectomrs')
            custom_user_first.save()
            custom_user_second = CustomUser(id=12,
                                            first_name='Jack',
                                            last_name='Nicholson',
                                            middle_name='Joseph',
                                            email='Jack.Nicholson@gmail.com',
                                            password='CuckoosNest75')
            custom_user_second.save()

            team = Team(id=11,
                        owner=custom_user_first,
                        members=[custom_user_first],
                        name='Coldplay')
            team.save()

            event_first = Event(id=11,
                                team=team,
                                owner=custom_user_first,
                                name='Party')
            event_first.save()

            event_second = Event(id=12,
                                 team=team,
                                 owner=custom_user_first,
                                 name='Horror')
            event_second.save()

            task = Task(id=11,
                        event=event_first,
                        users=[custom_user_first, custom_user_second],
                        title='Potato thing',
                        description='My awesome task, give me potato',
                        status=0)
            task.save()

            task = Task(id=12,
                        event=event_second,
                        users=[custom_user_second],
                        title='Tomato thing',
                        description='My awesome task, give me tomato',
                        status=1)

            task.save()

    def test_task_to_dict(self):
        """Method that tests `to_dict` method of certain Task instance."""

        task = Task.objects.get(id=11)
        expect_task_dict = {
            'id': 11,
            'title': 'Potato thing',
            'description': 'My awesome task, give me potato',
            'status': 0,
            'created_at': 1486029612,
            'updated_at': 1486029612,
            'event': 11,
            'users': [11,12]
        }

        actual_task_dict = task.to_dict()

        self.assertDictEqual(actual_task_dict, expect_task_dict)

    def test_task_success_get_by_id(self):
        """Method that tests succeeded `get_by_id` method of Task class object."""

        with mock.patch('task.models.cache') as mock_cache:
            with mock.patch('task.models.pickle') as mock_pickle:
                mock_cache. __contains__.return_value = True
                mock_pickle.load.return_value = True
                Task.get_by_id(11)

        actual_task = Task.get_by_id(11)
        expected_task = Task.objects.get(id=11)

        self.assertEqual(actual_task, expected_task)

    def test_task_none_get_by_id(self):
        """Method that tests unsucceeded `get_by_id` method of Task class object."""

        actual_task = Task.get_by_id(234)

        self.assertIsNone(actual_task)

    def test_task_success_create(self):
        """Method that tests succeeded `create` method of Task class object."""

        users = CustomUser.objects.get(id=11)
        event = Event.objects.get(id=11)
        created_task = Task.create(event=event,
                                   users=[users],
                                   title='My awesome title',
                                   description='Hello i`m description',
                                   status=1)

        self.assertIsInstance(created_task, Task)

    def test_task_none_create(self):
        """Method that tests unsucceeded `create` method of Task class object."""

        users = CustomUser.objects.get(id=11)
        event = Event.objects.get(id=11)
        created_task = Task.create(event=event,
                                   users=users)

        self.assertIsNone(created_task)

    def test_task_update(self):
        """
        Method that tests `update` method of certain Task instance
        Test for updating all attributes.
        """
        with mock.patch('task.models.cache') as mock_cache:
            mock_cache. __contains__.return_value = True

            redis_key = 'task_by_id_{0}'.format(self.id)
            tested_cache.set(redis_key, None)
            tested_cache.set("task", None)

            actual_task_update = Task.objects.get(id=12)
            actual_task_update.update(title='Some new title_1',
                           description='hello, it`s me_1',
                           status=1)

            self.assertEqual(actual_task_update.title, 'Some new title_1')
            self.assertEqual(actual_task_update.description, 'hello, it`s me_1')
            self.assertEqual(actual_task_update.status, 1)

    def test_task_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of Task class object."""

        is_deleted = Task.delete_by_id(11)
        self.assertTrue(is_deleted)
        self.assertRaises(Task.DoesNotExist, Task.objects.get, pk=11)

    def test_task_none_delete(self):
        """Method that tests unsucceeded `delete_by_id` method of Task class object."""

        is_task_delete = Task.delete_by_id(1423)
        self.assertIsNone(is_task_delete)

    def test_task_add_users(self):
        """Method that tests `add_users` and "remove_users" method of Task class object."""

        with mock.patch('task.models.cache') as mock_cache:
            mock_cache.__contains__.return_value = True

            task = Task.objects.get(id=12)
            first_member = CustomUser.objects.get(id=11)
            second_member = CustomUser.objects.get(id=12)
            task.add_users(users_list=[first_member,second_member])
            task.remove_users(users_list=[first_member])

            redis_key = 'task_by_id_{0}'.format(self.id)
            tested_cache.set(redis_key, None)
            tested_cache.set('task', None)

            expected_members = [second_member]

            actual_team_members = list(task.users.all())
            expected_team_members = list(expected_members)
            self.assertListEqual(actual_team_members, expected_team_members)

    def test_task_repr(self):
        """Method that test `__repr__` magic method of Task instance object."""

        task = Task.objects.get(id=11)
        actual_repr = task.__repr__()

        self.assertEqual(actual_repr, 'Task(id=11)')

    def test_task_str(self):
        """Method that test `__str__` magic method of Task instance object."""

        task = Task.objects.get(id=11)
        actual_str = task.__str__()
        expected_str = "'id': 11, " \
                       "'title': 'Potato thing', " \
                       "'description': 'My awesome task, give me potato', " \
                       "'status': 0, " \
                       "'created_at': 1486029612, " \
                       "'updated_at': 1486029612, " \
                       "'event': 11, " \
                       "'users': [11, 12]"
        self.assertMultiLineEqual(actual_str, expected_str)
