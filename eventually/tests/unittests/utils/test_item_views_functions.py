"""
Item Views Middleware Test
==========================
"""

import datetime
from unittest import mock
from django.test import TestCase
from authentication.models import CustomUser
from curriculum.models import Curriculum
from topic.models import Topic
from item.models import Item
from utils.item_views_functions import organized_items_sequence

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class ItemViewsFunctionsTestCase(TestCase):
    """Test for Item Views Functions"""
    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            custom_user = CustomUser.objects.create(id=123,
                                                    email='email1@mail.com',
                                                    first_name='1fname',
                                                    middle_name='1mname',
                                                    last_name='1lname',
                                                    is_active=True)

            Curriculum.objects.create(id=111,
                                      name="testcurriculum",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      team=None)

            Topic.objects.create(id=212,
                                 curriculum=Curriculum.get_by_id(111),
                                 author=custom_user,
                                 title='Topic #1',
                                 description="t_descr",
                                 mentors=[custom_user])

            Item.objects.create(id=311,
                                topic=Topic.get_by_id(212),
                                authors=[custom_user],
                                name='Node.js',
                                form=1,
                                description='description')

            Item.objects.create(id=312,
                                superiors=[311,],
                                topic=Topic.get_by_id(212),
                                authors=[custom_user],
                                name='Item Name',
                                form=1,
                                description='second description')

        self.topic = Topic.get_by_id(212)
        self.items_superiors_dict = {item.get_item_superiors()[0]: item.get_item_superiors()[1]
                                for item in self.topic.item_set.all()}

    def test_organized_items_sequence(self):
        """Test for organized_items_sequence method"""
        organized_list = organized_items_sequence(self.items_superiors_dict)
        self.assertListEqual(organized_list, [311, 312])
