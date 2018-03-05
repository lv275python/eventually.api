"""
SuggestedTopics Model Test
================
This module provides complete testing for all Team's model functions.

"""

import datetime
from unittest import mock
from django.test import TestCase
from authentication.models import CustomUser
from suggestedtopics.models import SuggestedTopics

TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class SuggestedTopicsModelTestCase(TestCase):
    """
    TestCase for providing SuggestedTopics model testing

    """

    def setUp(self):
        """
        Method that provides preparation before testing SuggestedTopics model's features.

        """

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user = CustomUser(id=301,
                                     first_name='Homer',
                                     last_name='Simpson',
                                     middle_name='Jay',
                                     email='member2@gmail.com')
            custom_user.set_password('donuts')
            custom_user.save()

            interested_users = []
            owner = custom_user
            name = 'somename'
            description = 'somedescription'
            suggested_topic_first = SuggestedTopics(101, owner=owner, interested_users=interested_users, name=name, description=description)
            suggested_topic_first.save()

    def test_suggested_topics_to_dict(self):
        """
        Method that tests `to_dict` method of certain SuggestedTopics instance.

        """

        suggested_topic = SuggestedTopics.objects.get(id=101)
        expect_suggested_topic_dict = {'id': 101,
                            'name': 'somename',
                            'description': 'somedescription',
                            'created_at': 1508044512,
                            'updated_at': 1508044512,
                            'owner': 301,
                            'interested_users': []}

        actual_suggested_topic_dict = suggested_topic.to_dict()

        self.assertDictEqual(actual_suggested_topic_dict, expect_suggested_topic_dict)

    def test_suggested_topic_success_create(self):
        """
        Method that tests succeeded `create` method of SuggestedTopics class object.

        """
        owner = CustomUser.objects.get(id=301)
        created_suggested_topic = SuggestedTopics.create(owner=owner,
                                                         name='name',
                                                         description = 'description')

        self.assertIsInstance(created_suggested_topic, SuggestedTopics)

    def test_suggested_topic_none_create(self):
        """
        Method that tests unsucceeded `create` method of Suggested Topic class object.

        """
        owner = CustomUser.objects.get(id=301)
        created_suggested_topic = SuggestedTopics.create(owner=owner,
                                                         name='name',
                                                         description=None)

        self.assertIsNone(created_suggested_topic)

    def test_suggested_topic_update(self):
        """
        Method that tests `update` method of SuggestedTopics class object.

        """

        actual_suggested_topic = SuggestedTopics.objects.get(id=101)
        actual_suggested_topic.update(name='new name', description='new description',
                                      interested_user=301)

        self.assertEqual(actual_suggested_topic.name, 'new name')
        self.assertEqual(actual_suggested_topic.description, 'new description')
        self.assertEqual(actual_suggested_topic.interested_user, [301])


    def test_suggested_topic_get_all(self):
        """
        Method that tests 'get_all' method of SuggestedTopics class object.

        """

        expected_suggested_topic = SuggestedTopics.objects.all()
        actual_suggested_topic = SuggestedTopics.get_all()

        self.assertEqual (list(expected_suggested_topic), list(actual_suggested_topic))


