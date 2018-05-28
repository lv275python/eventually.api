"""
Event view tests
================

This module provides complete testing for all Event's views functions.
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.cache import cache
from team.models import Team
from event.models import Event
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class EventViewTest(TestCase):
    """TestCase for providing Event view testing."""

    def setUp(self):
        """Method that provides preparation before testing Event view's features."""

        custom_user = CustomUser.objects.create(id=101, email='email@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()

        self.client = Client()
        self.client.login(username='email@gmail.com', password='123Qwerty')

        team = Team.objects.create(id=101, owner=custom_user, members=[custom_user], name='chelsea')

        with mock.patch('django.utils.timezone.now') as mock_time:
            cache.clear()
            mock_time.return_value = TEST_TIME
            event = Event.objects.create(id=101, team=team, owner=custom_user, name='ride', start_at=TEST_TIME)
            event.save()

    def test_success_get_all(self):
        """Method that tests the successful get request for the all events of the certain team."""

        expected_data = {'events': [{'id': 101,
                                     'team': 101,
                                     'name': 'ride',
                                     'owner': 101,
                                     'description': '',
                                     'start_at': 1509344112,
                                     'created_at': 1509344112,
                                     'updated_at': 1509344112,
                                     'duration': None,
                                     'longitude': None,
                                     'latitude': None,
                                     'budget': None,
                                     'status': 0}]}

        url = reverse('event:index', args=[101])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_all_events_from_my_teams(self):
        """Method that tests the successful get request for all events
        from those teams, I am member of."""

        expected_data = {'events': [{'id': 101,
                                     'team': 101,
                                     'name': 'ride',
                                     'owner': 101,
                                     'description': '',
                                     'start_at': 1509344112,
                                     'created_at': 1509344112,
                                     'updated_at': 1509344112,
                                     'duration': None,
                                     'longitude': None,
                                     'latitude': None,
                                     'budget': None,
                                     'status': 0}]}

        url = reverse('events:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_error_get_all(self):
        """
        Method that tests the unsuccessful get request for all events of the certain team.
        Test the incorrect team id.
        """

        url = reverse('event:index', args=[110])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_get_one(self):
        """Method that tests the successful get request to the certain event."""

        expected_data = {'id': 101,
                         'team': 101,
                         'name': 'ride',
                         'owner': 101,
                         'description': '',
                         'start_at': 1509344112,
                         'created_at': 1509344112,
                         'updated_at': 1509344112,
                         'duration': None,
                         'longitude': None,
                         'latitude': None,
                         'budget': None,
                         'status': 0}

        url = reverse('event:detail', args=[101, 101])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_error_get_one(self):
        """Method that test unsuccessful get request for certain event. Test invalid event id."""

        url = reverse('event:detail', args=[101, 110])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_post(self):
        """Method that tests the success post request for creating of event."""

        data = {'name': 'some name',
                'start_at': 12345645,
                'duration': 7200,
                'budget': 100,
                'status': 3}

        url = reverse('event:index', args=[101])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_dict['name'], 'some name')
        self.assertEqual(response_dict['description'], '')
        self.assertEqual(response_dict['start_at'], 12345645)
        self.assertEqual(response_dict['duration'], 7200)
        self.assertEqual(response_dict['budget'], 100)
        self.assertEqual(response_dict['status'], 3)

    def test_error_empty_json_post(self):
        """Method that tests unsuccessful post request with empty JSON data."""

        data = {}
        url = reverse('event:index', args=[101])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_data_post(self):
        """Method that tests unsuccessful post request with invalid post data."""

        data = {'description': '',
                'budget': 500,
                'status': 3}
        url = reverse('event:index', args=[101])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_team_post(self):
        """Method that tests unsuccessful post request with invalid team id."""

        data = {'name': 'some name',
                'description': '',
                'status': 2}
        url = reverse('event:index', args=[111])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_db_creating_post(self):
        """Method that tests unsuccessful post request when db creating is failed."""

        with mock.patch('event.models.Event.create') as event_create:
            event_create.return_value = None
            data = {'name': 'some name',
                    'description': '',
                    'status': 2}
            url = reverse('event:index', args=[101])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_success_put(self):
        """Method that tests invalid put request for the updating the certain event."""

        data = {'description': 'test',
                'start_at': 12345645,
                'duration': 5500,
                'budget': 150,
                'status': 2}

        url = reverse('event:detail', args=[101, 101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_event_id_put(self):
        """Method that tests unsuccessful put request with invalid event id."""

        data = {'name': 'updated name',
                'description': 'test',
                'start_at': 12345645,
                'duration': 5500,
                'budget': 150,
                'status': 2}
        url = reverse('event:detail', args=[101, 110])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_owner_id_put(self):
        """Method that tests unsuccessful put request with invalid owner id. User in not owner."""

        custom_user = CustomUser.objects.create(id=102, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=102, owner=custom_user, members=[custom_user], name='chelsea')
        team.save()
        event = Event.objects.create(id=102, team=team, owner=custom_user, name='box')
        event.save()

        data = {'name': 'updated name',
                'description': 'test',
                'start_at': 12345645,
                'duration': 5500,
                'budget': 150,
                'status': 2}
        url = reverse('event:detail', args=[101, 102])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_error_empty_json_put(self):
        """Method that tests unsuccessful put request with empty JSON data."""

        data = {}
        url = reverse('event:detail', args=[101, 101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_data_put(self):
        """Method that tests unsuccessful put request with invalid put data from client."""

        data = {'name': 'some name',
                'description': '',
                'duration': -23}
        url = reverse('event:detail', args=[101, 101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_delete(self):
        """Method that tests successful delete request"""

        url = reverse('event:detail', args=[101, 101])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_event_id_delete(self):
        """Method that tests unsuccessful delete request with invalid event id."""

        url = reverse('event:detail', args=[101, 110])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_owner_id_delete(self):
        """Method that tests unsuccessful delete request with invalid owner id. User in not owner"""

        custom_user = CustomUser.objects.create(id=102, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=102, owner=custom_user, members=[custom_user], name='chelsea')
        team.save()
        event = Event.objects.create(id=102, team=team, owner=custom_user, name='box')
        event.save()

        url = reverse('event:detail', args=[101, 102])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_error_db_deleting_post(self):
        """Method that tests unsuccessful delete request when db deleting is failed."""

        with mock.patch('event.models.Event.delete_by_id') as event_delete:
            event_delete.return_value = None
            url = reverse('event:detail', args=[101, 101])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)

    def test_error_event_paginator_validate(self):
        """
        Method that tests the unsuccessful get request because of event_paginator_validate.
        """

        url = reverse('events:index')
        response = self.client.get(url, {'limit': 2})
        self.assertEqual(response.status_code, 400)

    def test_if_event_from_date_param_validate(self):
        """
        Method that tests the get request when event_from_date_param_validate is true
        """
        expected_data = {'events': [{'id': 101,
                                     'team': 101,
                                     'name': 'ride',
                                     'owner': 101,
                                     'description': '',
                                     'start_at': 1509344112,
                                     'created_at': 1509344112,
                                     'updated_at': 1509344112,
                                     'duration': None,
                                     'longitude': None,
                                     'latitude': None,
                                     'budget': None,
                                     'status': 0}],
                         'full_length': 1}

        url = reverse('events:index')
        response = self.client.get(url, {'number': 1, 'limit': 2, 'from_date': 1509344110})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_event_from_date_param_validate_else(self):
        """
        Method that tests the get request when event_from_date_param_validate is false
        """

        test_time_now = datetime.datetime.now()
        test_time_future = datetime.datetime.fromtimestamp(test_time_now.timestamp()+60*60*24)

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            event = Event.objects.create(id=102, team=Team.get_by_id(101), owner=CustomUser.get_by_id(101),
                                         name='some_event', start_at=test_time_future)
            event.save()

        expected_data = {'events': [{'id': 102,
                                     'team': 101,
                                     'name': 'some_event',
                                     'owner': 101,
                                     'description': '',
                                     'start_at': int(test_time_future.timestamp()),
                                     'created_at': 1509344112,
                                     'updated_at': 1509344112,
                                     'duration': None,
                                     'longitude': None,
                                     'latitude': None,
                                     'budget': None,
                                     'status': 0}],
                         'full_length': 1}

        url = reverse('events:index')
        response = self.client.get(url, {'number': 1, 'limit': 2})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))
