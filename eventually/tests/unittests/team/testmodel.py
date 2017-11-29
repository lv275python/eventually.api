"""
Team Model Test
================
This module provides complete testing for all Team's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from authentication.models import CustomUser
from team.models import Team

TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class TeamModelTestCase(TestCase):
    """TestCase for providing Team model testing"""

    def setUp(self):
        """Method that provides preparation before testing Team model's features."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user = CustomUser(id=101,
                                     first_name='john',
                                     last_name='doe',
                                     middle_name='eric',
                                     email='email',
                                     password='123456')
            custom_user.save()

            members = [custom_user]
            owner = custom_user
            name = 'somename'
            description = 'somedescription'
            image = 'link1'
            team_first = Team(101, owner=owner, members=members, name=name, description=description, image=image)
            team_first.save()

            members = []
            owner = custom_user
            name = 'somename1'
            description = ''
            image = ''
            team_second = Team(102, owner=owner, members=members, name=name, description=description, image=image)
            team_second.save()

    def test_team_to_dict(self):
        """Method that tests `to_dict` method of certain Team instance."""

        team = Team.objects.get(id=101)
        expect_team_dict = {'id': 101,
                            'name': 'somename',
                            'description': 'somedescription',
                            'image': 'link1',
                            'created_at': 1508044512,
                            'updated_at': 1508044512,
                            'owner_id': 101,
                            'members_id': [101]}

        actual_team_dict = team.to_dict()

        self.assertDictEqual(actual_team_dict, expect_team_dict)

    def test_team_all_parameters_to_dict(self):
        """Method that tests `to_dict` method of certain Team instance."""

        team = Team.objects.get(id=102)
        expect_team_dict = {'id': 102,
                            'name': 'somename1',
                            'description': '',
                            'image': '',
                            'created_at': 1508044512,
                            'updated_at': 1508044512,
                            'owner_id': 101,
                            'members_id': []}

        actual_team_dict = team.to_dict()

        self.assertDictEqual(actual_team_dict, expect_team_dict)

    def test_team_success_get_by_id(self):
        """
        Method that tests succeeded `get_by_id` method of Team class object.
        """

        actual_team = Team.get_by_id(101)
        expected_team = Team.objects.get(id=101)

        self.assertEqual(actual_team, expected_team)

    def test_team_none_get_by_id(self):
        """
        Method that tests unsucceeded `get_by_id` method of Team class object.
        """

        actual_team = Team.get_by_id(123)

        self.assertIsNone(actual_team)

    def test_team_success_create(self):
        """
        Method that tests succeeded `create` method of Team class object.
        """
        members = [CustomUser.objects.get(id=101)]
        owner = CustomUser.objects.get(id=101)
        created_team = Team.create(owner=owner,
                                   members=members,
                                   name='test event name')

        self.assertIsInstance(created_team, Team)

    def test_team_none_create(self):
        """
        Method that tests unsucceeded `create` method of Team class object.
        """
        members = [CustomUser.objects.get(id=101)]
        owner = CustomUser.objects.get(id=101)
        created_team = Team.create(owner=owner,
                                   members=members)

        self.assertIsNone(created_team)

    def test_team_update(self):
        """
        Method that tests `update` method of certain Team instance.
        Test for updating only a few attributes.
        """

        actual_team = Team.get_by_id(101)

        actual_team.update(name='somename3', description='updated description')
        expected_team = Team.objects.get(id=101)

        self.assertEqual(actual_team, expected_team)

    def test_team_all_update(self):
        """
        Method that tests `update` method of certain Team instance.
        Test for updating all attributes.
        """

        actual_team = Team.get_by_id(101)
        new_owner = CustomUser.objects.create(id=201,
                                              email='exp@gmail.com',
                                              password='123')
        new_members = [CustomUser.objects.get(id=101), new_owner]
        actual_team.update(owner=new_owner,
                           members_add=[new_owner],
                           name='tennis',
                           description='very fun game',
                           image='link11')

        self.assertEqual(actual_team.owner, new_owner)
        self.assertListEqual(list(actual_team.members.all()), new_members)
        self.assertEqual(actual_team.name, 'tennis')
        self.assertEqual(actual_team.image, 'link11')
        self.assertEqual(actual_team.description, 'very fun game')

    def test_team_success_delete(self):
        """
        Method that tests succeeded `delete_by_id` method of Team class object.
        """

        is_team_delete = Team.delete_by_id(101)
        self.assertTrue(is_team_delete)
        self.assertRaises(Team.DoesNotExist, Team.objects.get, pk=101)

    def test_team_none_delete(self):
        """
        Method that tests unsucceeded `delete_by_id` method of Team class object.
        """

        is_team_delete = Team.delete_by_id(188)
        self.assertIsNone(is_team_delete)


    def test_team_repr(self):
        """Method that test `__repr__` magic method of Team instance object."""

        team = Team.objects.get(id=101)
        actual_repr = team.__repr__()
        expected_str = '101 somename somedescription link1 101 [101]'
        self.assertEqual(actual_repr, expected_str)

    def test_team_str(self):
        """Method that test `__str__` magic method of Team instance object."""

        team = Team.objects.get(id=101)
        actual_str = team.__str__()
        expected_str = '101 somename somedescription link1 \
2017-10-15 05:15:12+00:00 2017-10-15 05:15:12+00:00 101 [101]'
        self.assertMultiLineEqual(actual_str, expected_str)
