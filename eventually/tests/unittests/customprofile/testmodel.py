"""
CustomProfile Model Test
========================

This module provides complete testing for all CustomProfiles's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from django.utils import timezone
from authentication.models import CustomUser
from customprofile.models import CustomProfile


TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12, 0, tzinfo=timezone.utc)


class CustomProfileTestCase(TestCase):
    """TestCase for providing CustomProfile model testing"""

    def setUp(self):
        """Method that provides preparation before testing CustomProfile model's features."""
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user_first = CustomUser(id=101,
                                           first_name='petro',
                                           last_name='hanchuk',
                                           middle_name='mykola',
                                           email='email1',
                                           password='pas1')
            custom_user_first.save()

            custom_user_second = CustomUser(id=102,
                                            first_name='pavlo',
                                            last_name='hul',
                                            middle_name='vova',
                                            email='email2',
                                            password='pas2')
            custom_user_second.save()

            custom_user_third = CustomUser(id=103,
                                           first_name='dimas',
                                           last_name='revak',
                                           middle_name='yura',
                                           email='email1ko@net',
                                           password='pas5555')
            custom_user_third.save()

            profile = CustomProfile(id=101,
                                    user=custom_user_first,
                                    hobby='box',
                                    photo='link1',
                                    birthday=datetime.date(1995, 6, 8))
            profile.save()

            profile = CustomProfile(id=102,
                                    user=custom_user_second,
                                    birthday=datetime.date(1997, 7, 7))
            profile.save()

    def test_profile_to_dict(self):
        """Method that tests `to_dict` method of certain CustomProfile instance."""

        profile = CustomProfile.objects.get(id=101)
        expect_profile_dict = {'id': 101,
                               'user': 101,
                               'hobby': 'box',
                               'photo': 'link1',
                               'birthday': datetime.date(1995, 6, 8),
                               'created_at': 1509351312,
                               'updated_at': 1509351312}

        actual_profile_dict = profile.to_dict()

        self.assertDictEqual(actual_profile_dict, expect_profile_dict)

    def test_profile_success_get_by_id(self):
        """
        Method that tests succeeded `get_by_id` method of CustomProfile class object.
        """

        actual_profile = CustomProfile.get_by_id(101)
        expected_profile = CustomProfile.objects.get(id=101)

        self.assertEqual(actual_profile, expected_profile)

    def test_profile_none_get_by_id(self):
        """
        Method that tests unsucceeded `get_by_id` method of CustomProfile class object.
        """

        actual_profile = CustomProfile.get_by_id(10561)

        self.assertIsNone(actual_profile)

    def test_profile_success_create(self):
        """Method that tests succeeded `create` method of CustomProfile class object."""

        date_of_birth = datetime.date(1995, 6, 8)
        userok = CustomUser.objects.get(id=103)
        expected_profile = CustomProfile.create(user=userok,
                                                hobby='box',
                                                photo='link1',
                                                birthday=date_of_birth)

        self.assertIsInstance(expected_profile, CustomProfile)

    def test_profile_none_create(self):
        """Method that tests unsucceeded `create` method of CustomProfile class object."""

        userok = CustomUser()
        expected_profile = CustomProfile.create(user=userok)

        self.assertIsNone(expected_profile)

    def test_profile_update(self):
        """
        Method that tests `update` method of certain CustomProfile instance.
        Test for updating only a few attributes.
        """

        actual_profile = CustomProfile.objects.get(id=101)
        hobby = 'reading'
        actual_profile.update(hobby=hobby)
        expected_profile = CustomProfile.objects.get(id=101)

        self.assertEqual(actual_profile.hobby, hobby)
        self.assertEqual(actual_profile, expected_profile)

    def test_profile_all_update(self):
        """
        Method that tests `update` method of certain CustomProfile instance.
        Test for updating all attributes.
        """

        date_of_birth = datetime.date(1999, 1, 1)
        actual_profile = CustomProfile.objects.get(id=101)
        actual_profile.update(hobby='swimming',
                              photo='zal',
                              birthday=date_of_birth)

        self.assertEqual(actual_profile.hobby, 'swimming')
        self.assertEqual(actual_profile.photo, 'zal')
        self.assertEqual(actual_profile.birthday, date_of_birth)

    def test_profile_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of CustomProfile class object."""

        is_profile_delete = CustomProfile.delete_by_id(101)

        self.assertTrue(is_profile_delete)
        self.assertRaises(CustomProfile.DoesNotExist, CustomProfile.objects.get, id=101)

    def test_profile_none_delete(self):
        """Method that tests succeeded `delete_by_id` method of CustomProfile class object."""

        is_profile_delete = CustomProfile.delete_by_id(199)
        self.assertIsNone(is_profile_delete)

    def test_profile_repr(self):
        """Method that test `__repr__` magic method of CustomProfile instance object."""

        profile = CustomProfile.objects.get(id=101)
        actual_repr = profile.__repr__()
        expected_repr = '101 box link1 1995-06-08'

        self.assertEqual(actual_repr, expected_repr)

    def test_profile_str(self):
        """Method that test `__str__` magic method of CustomProfile instance object."""

        profile = CustomProfile.objects.get(id=101)
        actual_str = profile.__str__()
        new_str = "id:{} hobby:{} photo:{} birthday:{}\
                created_at:{} update_at:{}".format(101,
                                                   'box',
                                                   'link1',
                                                   datetime.date(1995, 6, 8),
                                                   TEST_TIME,
                                                   TEST_TIME)
        self.assertEqual(actual_str, new_str)
