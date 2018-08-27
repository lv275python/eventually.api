"""
SuggestedTopics view tests
================

This module provides complete testing for all Suggested Topics views functions.
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from suggestedtopics.models import SuggestedTopics
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class SuggestedTopicsViewTest(TestCase):
    """TestCase for providing SuggestedTopics view testing."""

    def setUp(self):
        """Method that provides preparation before testing SuggestedTopics view's features."""

        custom_user = CustomUser.objects.create(id=301, email='email@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()

        self.client = Client()
        self.client.login(username='email@gmail.com', password='123Qwerty')

        custom_user_second = CustomUser.objects.create(id=302, email='emailll@gmail.com', is_active=True)
        custom_user_second.set_password('12344Qwerty')
        custom_user_second.save()

        self.client_second = Client()
        self.client_second.login(username='emailll@gmail.com', password='12344Qwerty')

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            interested_users = []
            name = 'some_name'
            description = 'some_description'
            suggested_topic_first = SuggestedTopics(101, owner=custom_user, interested_users=interested_users, name=name, description=description)
            suggested_topic_first.save()


    def test_success_get_all(self):
        """Method that tests the successful get request for the SuggestedTopics."""

        expected_data = {'suggested_topics': [{'id': 101,
                                    'name': 'some_name',
                                    'description': 'some_description',
                                    'created_at': 1509344112,
                                    'updated_at': 1509344112,
                                    'owner': 301,
                                    'interested_users': [],
                                    'interested_users_name':[]
                                    }]
                         }

        url = reverse('suggested_topics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_post(self):
        """Method that tests the success post request for creating Suggested Topics."""

        data = {'name': 'new name',
                'description': 'new description'}
        url = reverse('suggested_topics')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_dict['name'], 'new name')
        self.assertEqual(response_dict['description'], 'new description')

    def test_error_empty_json_post(self):
        """Method that tests unsuccessful post request with empty JSON data."""

        data = {}
        url = reverse('suggested_topics')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_keys_post(self):
        """Method that tests unsuccessful post request with invalid keys. """

        data = {'descriptionssss': 'description',
                'name123': 'name'
                }
        url = reverse('suggested_topics')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_db_creating_post(self):
        """Method that tests unsuccessful post request when db creating is failed."""

        with mock.patch('suggestedtopics.models.SuggestedTopics.create') as suggested_topic_create:
            suggested_topic_create.return_value = None
            data = {'name': 'new_name',
                    'description': 'description'
                    }
            url = reverse('suggested_topics')
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 501)

    def test_success_put(self):
        """Method that tests success put request for the updating the certain suggested topic."""

        data = {'name': 'new name 123',
                'description': 'new description 123'}

        url = reverse('suggested_topic', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_unsuccess_put(self):
        """Method that tests unsuccess put request for the updating the certain suggested topic."""

        data = {'name': 'new name 123',
                'description': 'new description 123'}

        url = reverse('suggested_topic', args=[1010])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_empty_data_put(self):
        """Method that tests unsuccess put request for the updating the certain suggested topic."""

        data = {}

        url = reverse('suggested_topic', args=[101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_suggested_topic(self):
        """Method that tests unsuccessful delete request with invalid user id data"""

        url = reverse('suggested_topic', args=[101])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_error_db_deleting_post(self):
        """Method that tests unsuccessful delete request when db deleting is failed."""

        with mock.patch('suggestedtopics.models.SuggestedTopics.delete_by_id') as suggested_topic_delete:
            suggested_topic_delete.return_value = None
            url = reverse('suggested_topic', args=[101])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)

    def test_error_invalid_owner_id_delete(self):
        """Method that tests unsuccessful delete request with invalid owner id. User in not owner"""

        url = reverse('suggested_topic', args=[101])
        response = self.client_second.delete(url)
        self.assertEqual(response.status_code, 403)
