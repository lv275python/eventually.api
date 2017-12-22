"""
Team view tests
================

This module provides complete testing for all Team's views functions.
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from team.models import Team
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class EventViewTest(TestCase):
    """TestCase for providing Event view testing."""

    def setUp(self):
        """Method that provides preparation before testing Event view's features."""

        custom_user = CustomUser.objects.create(id=101, email='email@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()

        custom_user_a = CustomUser.objects.create(id=102, email='email1@gmail.com', is_active=True)
        custom_user_a.set_password('123Qwerty')
        custom_user_a.save()

        self.client = Client()
        self.client.login(username='email@gmail.com', password='123Qwerty')

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            team = Team.objects.create(id=101,
                                       owner=custom_user,
                                       members=[custom_user],
                                       name='some_name',
                                       description='some_description',
                                       image='link')
            team.save()

    def test_success_get_all(self):
        """Method that tests the successful get request for the all teams of the certain user."""

        expected_data = {'teams': [{'id': 101,
                                  'name': 'some_name',
                                  'description': 'some_description',
                                  'image': 'link',
                                  'created_at': 1509344112,
                                  'updated_at': 1509344112,
                                  'owner_id': 101,
                                  'members_id': [
                                     101
                                  ]}]
                        }

        url = reverse('teams')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    # def test_error_get_all(self):
    #     """
    #     Method that tests the unsuccessful get request for all teams of the certain user.
    #     Test the incorrect team.
    #     """

    #     url = reverse('event:index', args=[110])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)

    def test_success_get_one(self):
        """Method that tests the successful get request to the certain event."""

        expected_data = {'id': 101,
                         'name': 'some_name',
                         'description': 'some_description',
                         'image': 'link',
                         'created_at': 1509344112,
                         'updated_at': 1509344112,
                         'owner_id': 101,
                         'members_id': [
                            101]}

        url = reverse('team', args=[101])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_error_get_one(self):
        """Method that test unsuccessful get request for certain team. Test invalid team id."""

        url = reverse('team', args=[110])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_success_post(self):
        """Method that tests the success post request for creating of event."""

        data = {'name': 'some name',
                'members_id': [102,]}
        url = reverse('teams')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_dict['name'], 'some name')
        self.assertEqual(response_dict['owner_id'], 101)
        self.assertSetEqual(set(response_dict['members_id']), {101, 102})

    def test_error_empty_json_post(self):
        """Method that tests unsuccessful post request with empty JSON data."""

        data = {}
        url = reverse('teams')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_data_post(self):
        """Method that tests unsuccessful post request with invalid post data."""

        data = {'name': 'some name',
                'members_id': '101'}
        url = reverse('teams')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_keys_post(self):
        """Method that tests unsuccessful post request with invalid team id."""

        data = {'name123': 'some name',
                'members_id_': '101'}
        url = reverse('teams')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_db_creating_post(self):
        """Method that tests unsuccessful post request when db creating is failed."""

        with mock.patch('team.models.Team.create') as team_create:
            team_create.return_value = None
            data = {'name': 'some name',
                    'members_id': '101'}
            url = reverse('teams')
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_success_put(self):
        """Method that tests invalid put request for the updating the certain event."""

        data = {'description': 'test',
                'owner_id': 102,
                'members_di_add': [102]}

        url = reverse('team', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_team_id_put(self):
        """Method that tests unsuccessful put request with invalid event id."""

        data = {'description': 'test',
                'owner_id': 102,
                'members_di_add': [102]}
        url = reverse('team', args=[110])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_team_owner_put(self):
        """Method that tests unsuccessful put request with invalid event id."""
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            team_second = Team.objects.create(id=102,
                                              owner=CustomUser.get_by_id(102),
                                              members=[CustomUser.get_by_id(102)],
                                              name='some_name',
                                              description='some_description',
                                              image='link')
            team_second.save()
        data = {'description': 'test',
                'owner_id': 102,
                'members_di_add': [102]}
        url = reverse('team', args=[102])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)


    def test_error_empty_json_put(self):
        """Method that tests unsuccessful put request with empty JSON data."""

        data = {}
        url = reverse('team', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_data_put(self):
        """Method that tests unsuccessful put request with invalid put data from client."""

        data = {'description': 111,
                'owner_id': '102',
                'members_id_add': "102"}
        url = reverse('team', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_delete(self):
        """Method that tests successful delete request"""

        url = reverse('team', args=[101])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_team_id_delete(self):
        """Method that tests unsuccessful delete request with invalid event id."""

        url = reverse('team', args=[110])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_owner_id_delete(self):
        """Method that tests unsuccessful delete request with invalid owner id. User in not owner"""
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            team_second = Team.objects.create(id=102,
                                              owner=CustomUser.get_by_id(102),
                                              members=[CustomUser.get_by_id(102)],
                                              name='some_name',
                                              description='some_description',
                                              image='link')
            team_second.save()
        url = reverse('team', args=[102])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_error_db_deleting_post(self):
        """Method that tests unsuccessful delete request when db deleting is failed."""

        with mock.patch('team.models.Team.delete_by_id') as team_delete:
            team_delete.return_value = None
            url = reverse('team', args=[101])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)
