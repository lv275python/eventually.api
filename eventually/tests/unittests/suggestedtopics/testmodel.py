"""
SuggestedTopics Model Test
================
This module provides complete testing for all Team's model functions.

"""

import datetime
from unittest import mock
from suggestedtopics.models import cache as tested_cache
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

            interested_user = CustomUser(id=302,
                                     first_name='Roman',
                                     last_name='Simpson',
                                     middle_name='Jay',
                                     email='roman@gmail.com')
            interested_user.set_password('roman')

            interested_user.save()
            interested_users = []
            owner = custom_user
            name = 'somename'
            description = 'somedescription'
            suggested_topic_first = SuggestedTopics(101, owner=owner, interested_users=interested_users, name=name, description=description)
            suggested_topic_first.save()
            suggested_topic_second = SuggestedTopics(102, owner=owner, interested_users=interested_users, name=name, description=description)
            suggested_topic_second.interested_users.add(interested_user)
            suggested_topic_second.save()

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
                            'interested_users': [],
                            'interested_users_name': []}

        actual_suggested_topic_dict = suggested_topic.to_dict()
        self.assertDictEqual(actual_suggested_topic_dict, expect_suggested_topic_dict)

        suggested_topic_second = SuggestedTopics.objects.get(id=102)
        expect_suggested_second_topic_dict = {'id': 102,
                                       'name': 'somename',
                                       'description': 'somedescription',
                                       'created_at': 1508044512,
                                       'updated_at': 1508044512,
                                       'owner': 301,
                                       'interested_users': [302],
                                       'interested_users_name': ['Roman Simpson']}

        actual_suggested_second_topic_dict = suggested_topic_second.to_dict()
        self.assertDictEqual(actual_suggested_second_topic_dict, expect_suggested_second_topic_dict)

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

        with mock.patch('suggestedtopics.models.cache') as mock_cache:
            mock_cache. __contains__.return_value = True

            actual_suggested_topic = SuggestedTopics.objects.get(id=101)
            actual_suggested_topic.update(name='new name', description='new description',
                                          interested_user=301, remove_interest=False)

            interested_users = [user.id for user in actual_suggested_topic.interested_users.all()]

            redis_key = 'suggested_topic_by_id_{0}'.format(self.id)
            tested_cache.set(redis_key, None)
            tested_cache.set("all_suggested_topic", None)

            actual_suggested_topic_update = SuggestedTopics.objects.get(id=101)
            actual_suggested_topic_update.update(name='new name_name', description='new description_des',
                                          interested_user=301, remove_interest=False)

            self.assertEqual(actual_suggested_topic_update.name, 'new name_name')
            self.assertEqual(actual_suggested_topic_update.description, 'new description_des')
            self.assertEqual(interested_users, [301])

    def test_suggested_topic_update_remove_user(self):
        """
        Method that tests `update` method of SuggestedTopics if user leave the topic

        """

        actual_suggested_topic = SuggestedTopics.objects.get(id=101)
        actual_suggested_topic.update(name='new name', description='new description',
                                      interested_user=301, remove_interest=False)
        interested_users = [user.id for user in actual_suggested_topic.interested_users.all()]
        self.assertEqual(interested_users, [301])

        actual_suggested_topic.update(interested_user=301, remove_interest=True)
        interested_users = [user.id for user in actual_suggested_topic.interested_users.all()]
        self.assertEqual(interested_users, [])

    def test_suggested_topic_get_all(self):
        """
        Method that tests 'get_all' method of SuggestedTopics class object.

        """
        with mock.patch('suggestedtopics.models.cache') as mock_cache:
            with mock.patch('suggestedtopics.models.pickle') as mock_pickle:
                mock_cache. __contains__.return_value = True
                mock_pickle.load.return_value = True

                actual_suggested_topic = SuggestedTopics.get_all()

    def test_suggested_topic_get_all_not(self):
        """
        Method that tests 'get_all' method of SuggestedTopics class object.

        """
        expected_suggested_topic = SuggestedTopics.objects.all()
        actual_suggested_topic = SuggestedTopics.get_all()

        self.assertEqual(list(expected_suggested_topic), list(actual_suggested_topic))
