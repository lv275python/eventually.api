"""
Item Model Test
===============

This module provides complete testing for all Item's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from authentication.models import CustomUser
from curriculum.models import Curriculum
from item.models import Item
from team.models import Team
from topic.models import Topic


TEST_TIME = datetime.datetime(2016, 10, 15, 8, 15, 12)


class ItemModelTestCase(TestCase):
    """TestCase for providing Item model testing"""

    def setUp(self):
        """Method that provides preparation before testing Item model's features."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user_first = CustomUser(id=101,
                                           first_name='john',
                                           last_name='doe',
                                           middle_name='eric',
                                           email='email',
                                           password='123456')
            custom_user_first.save()
            custom_user_second = CustomUser(id=102,
                                            first_name='eric',
                                            last_name='moreno',
                                            middle_name='mike',
                                            email='test@email',
                                            password='123456')
            custom_user_second.save()

            custom_user_third = CustomUser(id=103,
                                           first_name='pablo',
                                           last_name='martines',
                                           middle_name='jo',
                                           email='sometest@email',
                                           password='123456')
            custom_user_third.save()

            team = Team(id=101,
                        owner=custom_user_first,
                        name='Coldplay')
            team.save()
            team.members.add(custom_user_first, custom_user_second)

            curriculum = Curriculum.objects.create(id=101,
                                                   name="testcurriculum",
                                                   goals=["goal1", "goal2"],
                                                   description="test_descr",
                                                   team=team)
            curriculum.save()

            topic_python = Topic(id=101,
                          curriculum=curriculum,
                          title='Python',
                          description='My awesome topic')
            topic_python.save()
            topic_python.mentors.add(custom_user_first, custom_user_third)

            topic_html = Topic(id=102,
                          curriculum=curriculum,
                          title='HTML',
                          description='My another awesome topic')
            topic_html.save()
            topic_html.mentors.add(custom_user_third)

            item_first = Item(id=101,
                              name='read documentation',
                              form=0,
                              topic=topic_python)
            item_first.save()
            item_first.authors.add(custom_user_first, custom_user_third)

            item_second = Item(id=102,
                               name='pass test',
                               form=1,
                               topic=topic_python,
                               estimation=datetime.timedelta(seconds=54000))
            item_second.save()
            item_second.authors.add(custom_user_first)

            item_third = Item(id=103,
                              name='watch videos',
                              form=0,
                              topic=topic_html,
                              description='test',
                              estimation=datetime.timedelta(seconds=1104000))
            item_third.save()
            item_third.authors.add(custom_user_first, custom_user_third)
            item_third.superiors.add(item_first, item_second)

    def test_item_repr(self):
        """Method that test `__repr__` magic method of Item instance object."""

        item = Item.objects.get(id=103)
        actual_repr = item.__repr__()
        expected_repr = ('Item(id=103)')
        self.assertEqual(actual_repr, expected_repr)

    def test_item_str(self):
        """Method that test `__str__` magic method of Item instance object."""

        item = Item.objects.get(id=101)
        actual_repr = item.__str__()
        expected_repr = ("'id': 101, 'name': 'read documentation', 'authors': [101, 103], "
                         "'topic': 101, 'form': 0, 'superiors': [], 'description': '', "
                         "'estimation': None, 'created_at': 1476508512, 'updated_at': 1476508512")
        self.assertEqual(actual_repr, expected_repr)

    def test_item_to_dict(self):
        """
        Method that tests `to_dict` method of certain Item instance.

        Function tests Item instance with all filled parameters.
        """

        item = Item.objects.get(id=103)
        expected_item_dict = {'id': 103,
                              'name': 'watch videos',
                              'authors': [101, 103],
                              'topic': 102,
                              'form': 0,
                              'superiors': [101, 102],
                              'description': 'test',
                              'estimation': 1104000,
                              'created_at': 1476508512,
                              'updated_at': 1476508512}
        actual_item_dict = item.to_dict()
        actual_item_dict['authors'].sort()
        actual_item_dict['superiors'].sort()
        self.assertDictEqual(actual_item_dict, expected_item_dict)

    def test_item_success_get_by_id(self):
        """Method that tests succeeded `get_by_id` method of Item class object."""

        actual_item = Item.get_by_id(102)
        expected_item = Item.objects.get(id=102)
        self.assertEqual(actual_item, expected_item)

    def test_item_none_get_by_id(self):
        """Method that tests unsucceeded `get_by_id` method of Item class object."""

        actual_item = Item.get_by_id(123)
        self.assertIsNone(actual_item)

    def test_item_success_create(self):
        """Method that tests succeeded `create` method of Item class object."""

        user_first = CustomUser.objects.get(id=101)
        user_second = CustomUser.objects.get(id=102)
        users = [user_first, user_second]
        superior_first = Item.objects.get(id=102)
        superior_second = Item.objects.get(id=103)
        superiors = [superior_first, superior_second]
        topic = Topic.objects.get(id=101)
        time = datetime.timedelta(seconds=66000)
        item = Item.create(name='new', authors=users, topic=topic,
                           form=1, superiors=superiors, estimation=time)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.name, 'new')
        self.assertEqual(item.topic.id, 101)
        self.assertEqual(item.form, 1)
        self.assertListEqual(list(item.authors.all()), users)
        self.assertListEqual(list(item.superiors.all()), superiors)
        self.assertEqual(item.description, '')
        self.assertEqual(item.estimation, time)

    def test_item_none_create(self):
        """Method that tests unsucceeded `create` method of Item class object."""

        author = CustomUser.objects.get(id=101)
        topic = Topic.objects.get(id=101)
        item = Item.create(name='test', authors=[author], topic=topic, form='str')
        self.assertIsNone(item)

    def test_item_update(self):
        """
        Method that tests `update` method of the certain Item instance.

        Test for updating all attributes.
        """

        estimation = datetime.timedelta(seconds=104000)
        actual_item = Item.objects.get(id=101)
        actual_item.update(name='listen book',
                           form=2,
                           description='updated description',
                           estimation=estimation)
        expected_item = Item.objects.get(id=101)
        self.assertEqual(actual_item, expected_item)
        self.assertEqual(actual_item.name, 'listen book')
        self.assertEqual(actual_item.form, 2)
        self.assertEqual(actual_item.description, 'updated description')
        self.assertEqual(actual_item.estimation, estimation)


    def test_item_add_authors(self):
        """
        Method that tests `update_authors` method of the certain Item instance.

        Test for adding authors.
        """

        actual_item = Item.objects.get(id=101)
        user_first = CustomUser.objects.get(id=101)
        user_second = CustomUser.objects.get(id=102)
        users = [user_first, user_second]
        actual_item.update_authors(authors_add=users)
        expected_item = Item.objects.get(id=101)
        self.assertListEqual(list(actual_item.authors.all()), list(expected_item.authors.all()))

    def test_item_remove_authors(self):
        """
        Method that tests `update_authors` method of the certain Item instance.

        Test for removing authors.
        """

        actual_item = Item.objects.get(id=103)
        user_first = CustomUser.objects.get(id=101)
        user_second = CustomUser.objects.get(id=102)
        users = [user_first, user_second]
        actual_item.update_authors(authors_del=users)
        expected_item = Item.objects.get(id=103)
        self.assertListEqual(list(actual_item.authors.all()), list(expected_item.authors.all()))

    def test_item_add_superiors(self):
        """
        Method that tests `update_superiors` method of the certain Item instance.

        Test for adding superiors.
        """

        actual_item = Item.objects.get(id=101)
        superior_first = Item.objects.get(id=102)
        superior_second = Item.objects.get(id=103)
        superiors = [superior_first, superior_second]
        actual_item.update_superiors(superiors_add=superiors)
        expected_item = Item.objects.get(id=101)
        self.assertListEqual(list(actual_item.authors.all()), list(expected_item.authors.all()))

    def test_item_remove_superiors(self):
        """
        Method that tests `update_superiors` method of the certain Item instance.

        Test for removing superiors.
        """

        actual_item = Item.objects.get(id=103)
        superior_first = Item.objects.get(id=102)
        superior_second = Item.objects.get(id=103)
        superiors = [superior_first, superior_second]
        actual_item.update_superiors(superiors_del=superiors)
        expected_item = Item.objects.get(id=103)
        self.assertListEqual(list(actual_item.authors.all()), list(expected_item.authors.all()))

    def test_item_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of Item class object."""

        is_item_delete = Item.delete_by_id(101)
        self.assertTrue(is_item_delete)
        self.assertRaises(Item.DoesNotExist, Item.objects.get, pk=101)

    def test_item_none_delete(self):
        """Method that tests unsucceeded `delete_by_id` method of Item class object."""

        is_item_delete = Item.delete_by_id(188)
        self.assertIsNone(is_item_delete)
