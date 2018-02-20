"""Topic Model Test
================

This module provides complete testing for all Topic's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from topic.models import Topic
from curriculum.models import Curriculum
from authentication.models import CustomUser
from team.models import Team

TEST_TIME = datetime.datetime(2017, 2, 2, 12, 00, 12)


class TopicModelTestCase(TestCase):
    """TestCase for providing Topic model testing"""

    def setUp(self):
        """Method that provides preparation before testing Topic model's features."""

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

            test_curriculum = Curriculum.objects.create(id=111,
                                                        name="testcurriculum",
                                                        goals=["goal1", "goal2"],
                                                        description="t_descr",
                                                        team=team)


            topic = Topic(id=11,
                          curriculum=test_curriculum,
                          author = custom_user_first,
                          mentors=[custom_user_first, custom_user_second],
                          title='Topic title',
                          description='My awesome topic')
            topic.save()

    def test_topic_to_dict(self):
        """Method that tests `to_dict` method of certain Topic instance."""

        topic = Topic.objects.get(id=11)
        expect_topic_dict = {
            'id': 11,
            'title': 'Topic title',
            'description': 'My awesome topic',
            'created_at': 1486029612,
            'updated_at': 1486029612,
            'curriculum': 111,
            'author': 11,
            'mentors': [11, 12]
        }

        actual_topic_dict = topic.to_dict()

        self.assertDictEqual(actual_topic_dict, expect_topic_dict)

    def test_topic_success_get_by_id(self):
        """Method that tests succeeded `get_by_id` method of Topic class object."""

        actual_topic = Topic.get_by_id(11)
        expected_topic = Topic.objects.get(id=11)

        self.assertEqual(actual_topic, expected_topic)

    def test_topic_none_get_by_id(self):
        """Method that tests unsucceeded `get_by_id` method of Topic class object."""

        actual_topic = Topic.get_by_id(234)

        self.assertIsNone(actual_topic)

    def test_topic_success_create(self):
        """Method that tests succeeded `create` method of Topic class object."""

        author = CustomUser.objects.get(id=11)
        curriculum = Curriculum.objects.get(id=111)
        created_topic = Topic.create(curriculum=curriculum,
                                     author=author,
                                     title='My awesome title',
                                     description='Hello i`m description')

        self.assertIsInstance(created_topic, Topic)

    def test_topic_none_create(self):
        """Method that tests unsucceeded `create` method of Topic class object."""

        author = CustomUser.objects.get(id=11)
        curriculum = Curriculum.objects.get(id=111)
        created_topic = Topic.create(curriculum=curriculum,
                                     author=author)

        self.assertIsNone(created_topic)

    def test_topic_update(self):
        """
        Method that tests `update` method of certain Topic instance.
        Test for updating all attributes.
        """

        actual_topic = Topic.objects.get(id=11)
        title = 'Some new title'
        description = 'hello, it`s me'
        actual_topic.update(title=title,
                            description=description)

        self.assertEqual(actual_topic.title, title)
        self.assertEqual(actual_topic.description, description)

    def test_topic_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of Topic class object."""

        is_deleted = Topic.delete_by_id(11)
        self.assertTrue(is_deleted)
        self.assertRaises(Topic.DoesNotExist, Topic.objects.get, pk=11)

    def test_topic_none_delete(self):
        """Method that tests unsucceeded `delete_by_id` method of Topic class object."""

        is_topic_delete = Topic.delete_by_id(1423)
        self.assertIsNone(is_topic_delete)

    def test_topic_repr(self):
        """Method that test `__repr__` magic method of Topic instance object."""

        topic = Topic.objects.get(id=11)
        actual_repr = topic.__repr__()

        self.assertEqual(actual_repr, 'Topic(id=11)')

    def test_topic_str(self):
        """Method that test `__str__` magic method of Topic instance object."""

        topic = Topic.objects.get(id=11)
        actual_str = topic.__str__()
        expected_str = "'id': 11, " \
                       "'title': 'Topic title', " \
                       "'description': 'My awesome topic', " \
                       "'created_at': 1486029612, " \
                       "'updated_at': 1486029612, " \
                       "'curriculum': 111, " \
                       "'author': 11, " \
                       "'mentors': [11, 12]"
        self.assertMultiLineEqual(actual_str, expected_str)

    def test_topic_add_mentors(self):
        """
        Method that tests `update_mentors` method of the certain Topic instance.
        Test for adding authors.
        """

        actual_topic = Topic.objects.get(id=11)
        user_first = CustomUser.objects.get(id=11)
        user_second = CustomUser.objects.get(id=12)
        users = [user_first, user_second]
        actual_topic.add_mentors(mentors_list=users)
        expected_topic = Topic.objects.get(id=11)
        self.assertListEqual(list(actual_topic.mentors.all()), list(expected_topic.mentors.all()))

    def test_topic_remove_mentors(self):
        """
        Method that tests `update_authors` method of the certain Topic instance.
        Test for removing authors.
        """

        actual_topic = Topic.objects.get(id=11)
        user_first = CustomUser.objects.get(id=12)
        user_second = CustomUser.objects.get(id=11)
        users = [user_first, user_second]
        actual_topic.remove_mentors(mentors_list=users)
        expected_topic = Topic.objects.get(id=11)
        self.assertListEqual(list(actual_topic.mentors.all()), list(expected_topic.mentors.all()))
