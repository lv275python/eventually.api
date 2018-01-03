"""
CustomProfile view tests
========================
This module provides complete testing for all CustomProfile's views functions.
"""

import json
import pytz
import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from customprofile.models import CustomProfile
from authentication.models import CustomUser
from unittest import mock

TEST_CREATED_AT = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)


class CustomProfileViewTest(TestCase):
    """TestCase for providing CustomProfile view testing."""

    def setUp(self):
        """Method that provides preparation before testing CustomProfile view's features."""

        user = CustomUser.objects.create(id=101,
                                         first_name="Robert",
                                         last_name="Downey",
                                         middle_name="Jr.",
                                         email='mail@gmail.com',
                                         is_active=True)
        user.set_password('Ivan16')
        user.save()

        user_second = CustomUser.objects.create(id=102, email='dima@gmail.com', is_active=True)
        user_second.set_password('Dima5')
        user_second.save()

        self.client = Client()

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_CREATED_AT

            custom_profile = CustomProfile.objects.create(id=101,
                                                          user=user,
                                                          hobby='box',
                                                          photo='link1',
                                                          birthday='2000-2-4',
                                                          created_at=TEST_CREATED_AT,
                                                          updated_at=TEST_CREATED_AT)
            custom_profile.save()

            custom_profile_second = CustomProfile.objects.create(user=user_second)
            custom_profile_second.save()

    def test_success_get(self):
        """Method that tests the successful get request for the profile of the certain user."""
        self.client.login(username='mail@gmail.com', password='Ivan16')

        expected_data = {'id': 101,
                         'user': 101,
                         'email': 'mail@gmail.com',
                         'first_name': 'Robert',
                         'middle_name': 'Jr.',
                         'last_name': 'Downey',
                         'hobby': 'box',
                         'photo': 'link1',
                         'birthday': '2000-02-04',
                         'is_active': True,
                         'created_at': 1491825600,
                         'updated_at': 1491825600,}

        url = reverse('profile', args=[101])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_invalid_user_id_get(self):
        """
        Method that tests the unsuccessful get request for user's profile.
        Test the incorrect user id.
        """
        self.client.login(username='dima@gmail.com', password='Dima5')

        url = reverse('profile', args=[111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_success_put(self):
        """Method that tests invalid put request for the updating the certain profile."""
        self.client.login(username='mail@gmail.com', password='Ivan16')
        data = {'hobby': 'programming',
                'photo': 'link16',
                'birthday': '2000-2-4'}
        url = reverse('profile', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_data_put(self):
        """Method that tests unsuccessful put request with invalid put data ."""
        self.client.login(username='mail@gmail.com', password='Ivan16')

        data = {'user.id': 55, 
                'hobby': -3,
                'photo': 5,
                'birthday': '2000-2-4'}
        url = reverse('profile', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_user_id_not_request_user_put(self):
        """Method that tests unsuccessful put request when user id != request.user."""
        self.client.login(username='mail@gmail.com', password='Ivan16')
        data = {'hobby': 'programming',
                'photo': 'link16',
                'birthday': '2000-2-4'}
        url = reverse('profile', args=[102])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_success_delete(self):
        """Method that tests successful logout user"""
        self.client.login(username='mail@gmail.com', password='Ivan16')
        url = reverse('profile_del')
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
