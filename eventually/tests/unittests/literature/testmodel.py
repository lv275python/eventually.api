import datetime
from django.test import TestCase
from authentication.models import CustomUser
from curriculum.models import Curriculum
from item.models import Item
from literature.models import LiteratureItem
from team.models import Team
from topic.models import Topic
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class LiteratureItemTestCase(TestCase):
    """TestCase for LiteratureItem model"""

    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            user = CustomUser(id=111,
                              email="email2",
                              password="pass2",
                              first_name="firstname2",
                              middle_name="middle2",
                              last_name="last2")
            user.save()

            team = Team(id=111,
                        owner=user,
                        members=[user],
                        name='team1')
            team.save()

            curriculum = Curriculum(id=112,
                                    name="tes",
                                    goals=["goal1", "goal2"],
                                    description="t_descr",
                                    team=team)
            curriculum.save()

            topic = Topic(id=111,
                          curriculum=curriculum,
                          author=user,
                          title='Topic title',
                          description='My awesome topic')
            topic.save()

            item = Item(id=111,
                        topic=topic,
                        name='read documentation',
                        form=0)
            item.save()

            literature = LiteratureItem(id=111,
                                        title='title',
                                        description='description',
                                        source='source',
                                        author=user,
                                        item=item)
            literature.save()

    def test_literature_parameters_to_dict(self):
        """Method that tests `to_dict` method of certain LiteratureItem instance."""
        literature = LiteratureItem.objects.get(id=111)
        expect_literature_dict = {'id': 111,
                                  'title': 'title',
                                  'description': 'description',
                                  'source': 'source',
                                  'create_at': 1508044512,
                                  'update_at': 1508044512,
                                  'author': 111,
                                  'item': 111
                                  }

        actual_literature_dict = literature.to_dict()
        self.assertEqual(actual_literature_dict, expect_literature_dict)

    def test_literature_none_get_by_id(self):
        """Method that tests `to_dict` method of certain LiteratureItem instance."""
        literature = LiteratureItem.get_by_id(113)
        self.assertIsNone(literature)

    def test_literature_get_by_id(self):
        """Method that tests `to_dict` method of certain LiteratureItem instance."""
        literature = LiteratureItem.get_by_id(111)
        self.assertEqual(literature.id, 111)

    def test_literature_repr(self):
        """Method that tests `__repr__` method of certain LiteratureItem instance."""
        literature = LiteratureItem.objects.get(id=111)
        expected_literature_repr = "LiteratureItem(id=111)"

        self.assertEqual(repr(literature), expected_literature_repr)

    def test_literature_str(self):
        """Method that tests `__str__` method of certain LiteratureItem instance."""
        literature = LiteratureItem.objects.get(id=111)
        expected_literature_str = "'id': 111, " \
                                  "'title': 'title', " \
                                  "'description': 'description', " \
                                  "'source': 'source', " \
                                  "'create_at': 1508044512, " \
                                  "'update_at': 1508044512, "\
                                  "'author': 111, " \
                                  "'item': 111"
        self.assertEqual(str(literature), expected_literature_str)

    def test_literature_success_create(self):
        """Method that tests succeeded `create` method of LiteratureItem class object."""
        author = CustomUser.objects.get(id=111)
        item = Item.objects.get(id=111)
        created_literature = LiteratureItem.create(title="my title",
                                                   source="source of book",
                                                   author=author,
                                                   item=item)
        self.assertIsInstance(created_literature, LiteratureItem)

    def test_literature_unsuccessful_create(self):
        """Method that tests unsuccessful `create` method of Literature class object."""
        author = CustomUser()
        item = Item.objects.get(id=111)
        created_literature = LiteratureItem.create(title='yyy',
                                                   source="yyy",
                                                   author=author,
                                                   item=item)
        self.assertIsNone(created_literature)

    def test_literature_update(self):
        """Method that tests `update` method of certain LiteratureItem instance."""

        actual_literature = LiteratureItem.get_by_id(111)
        actual_literature.update(title='new title',
                                 description='new description',
                                 source='new source')
        expected_literature = LiteratureItem.objects.get(id=111)
        self.assertEqual(actual_literature, expected_literature)

    def test_literature_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of LiteratureItem class object."""

        is_literature_delete = LiteratureItem.delete_by_id(111)
        self.assertTrue(is_literature_delete)

    def test_literature_unsuccessful_delete(self):
        """Method that tests unsuccessful `delete_by_id` method of LiteratureItem class object."""

        id_literature_delete = LiteratureItem.delete_by_id(112)
        self.assertIsNone(id_literature_delete)
