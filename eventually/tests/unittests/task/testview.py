"""
Task view tests
===============
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from team.models import Team
from event.models import Event
from task.models import Task
from unittest import mock

TEST_TIME = datetime.datetime(2017, 11, 14, 5, 12, 12)


class TaskViewTest(TestCase):
    """TestCase for providing Task view testing"""

    def setUp(self):
        """Method that provides preparation before testing Task view`s features."""
        custom_user = CustomUser.objects.create(id=11, email='useremail@email.com', is_active=True)
        custom_user.set_password('Pw123')
        custom_user.save()

        self.client = Client()
        self.client.login(username='useremail@email.com', password='Pw123')

        team = Team.objects.create(id=11, owner=custom_user, members=[custom_user], name='Placebo')

        event = Event.objects.create(id=11, team=team, owner=custom_user, name='Party')


        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            task = Task.objects.create(id=11,
                                       event=event,
                                       users=[custom_user],
                                       title='do something',
                                       description='give me fork',
                                       status=1)
            task.save()

    def test_success_get_one(self):
        """Method that tests the successful request to the certain task"""

        expected_data = {'id': 11,
                         'event': 11,
                         'users': [11,],
                         'created_at': 1510629132,
                         'updated_at': 1510629132,
                         'title': 'do something',
                         'description': 'give me fork',
                         'status': 1}

        url = reverse('event:task:detail', args=[11, 11, 11])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_all(self):
        """Method that tests the successful request to the all tasks"""

        expected_data = {'tasks': [{'id': 11,
                                    'event': 11,
                                    'users': [11,],
                                    'created_at': 1510629132,
                                    'updated_at': 1510629132,
                                    'title': 'do something',
                                    'description': 'give me fork',
                                    'status': 1}]}

        url = reverse('event:task:index', args=[11, 11])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_error_get_all(self):
        """
        Method that tests the unsuccessful get request for all tasks of the certain event.
        Test the incorrect event id.
        """

        url = reverse('event:task:index', args=[11, 13])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_fail_get(self):
        """Method that test unsuccessful request for certain task. Test invalid task id."""

        url = reverse('event:task:detail', args=[11, 11, 1019])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_post(self):
        """Method that tests the success post request for creating task"""

        data = {'users': [11,],
                'title': 'do something else',
                'description': 'give me pan',
                'status': 1}

        url = reverse('event:task:index', args=[11, 11])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_dict['users'], [11,])
        self.assertEqual(response_dict['title'], 'do something else')
        self.assertEqual(response_dict['description'], 'give me pan')
        self.assertEqual(response_dict['status'], 1)

    def test_invalid_data_post(self):
        """Method that tests unsuccessful post request with invalid post data."""

        data = {'description': '',
                'status': 3}
        url = reverse('event:task:index', args=[11, 11])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_team_post(self):
        """Method that tests unsuccessful post request with invalid team id."""

        data = {'users': [11,],
                'title': 'do something else',
                'description': 'give me pan',
                'status': 1}
        url = reverse('event:task:index', args=[14 ,11])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_invalid_event_post(self):
        """Method that tests unsuccessful post request with invalid event id."""

        data = {'users': [11,],
                'title': 'do something else',
                'description': 'give me pan',
                'status': 1}
        url = reverse('event:task:index', args=[11 ,112])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_empty_json_post(self):
        """Method that tests unsuccessful post request with empty JSON data."""

        data = {}
        url = reverse('event:task:index', args=[11 ,112])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_db_creating_post(self):
        """Method that tests unsuccessful post request when db creating is failed."""

        with mock.patch('task.models.Task.create') as task_create:
            task_create.return_value = None
            data = {'title': 'some name',
                    'description': 'hello',
                    'status': 0,
                    'users': [11,]}
            url = reverse('event:task:index', args=[11 ,11])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_success_put(self):
        """Method that test invalid put request for the updating the certain task."""
        custom_user = CustomUser.objects.create(id=22, email='email+1@email.com', is_active=True)
        custom_user.set_password('Pw123')
        custom_user.save()

        data = {'title': 'my awesome title',
                'add_users': [22, 4],
                'remove_users': [22, 5]}

        url = reverse('event:task:detail', args=[11, 11, 11])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_invalid_task_id_put(self):
        """Method that tests unsuccessful put request with invalid task id."""

        data = {'title': 'my awesome title',
                'description': 'test',
                'status': 1}
        url = reverse('event:task:detail', args=[11, 11, 141])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_invalid_data(self):
        """Method that tests unsuccessful put request with invalid data."""

        data = {'title': 'my awesome title',
                'description': 12,
                'status': 1}
        url = reverse('event:task:detail', args=[11, 11, 11])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_wrong_user(self):
        """Method that tests unsuccessful put request with no permissions."""
        custom_user = CustomUser.objects.create(id=14, email='user@email.com', is_active=True)
        custom_user.set_password('Pw123')
        custom_user.save()

        self.client = Client()
        self.client.login(username='user@email.com', password='Pw123')

        data = {'title': 'my awesome title'}

        url = reverse('event:task:detail', args=[11, 11, 11])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_success_delete(self):
        """Method that tests successful delete request"""

        url = reverse('event:task:detail', args=[11, 11, 11])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)


    def test_fail_user_delete(self):
        """Method that tests unsuccessful delete request with no permissions."""

        custom_user = CustomUser.objects.create(id=12, email='email+1@email.com', is_active=True)
        custom_user.set_password('Pw123')
        custom_user.save()

        self.client = Client()
        self.client.login(username='email+1@email.com', password='Pw123')

        url = reverse('event:task:detail', args=[11, 11, 11])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_error_db_deleting_post(self):
        """Method that tests unsuccessful delete request when db deleting is failed."""

        with mock.patch('task.models.Task.delete_by_id') as task_delete:
            task_delete.return_value = None
            url = reverse('event:task:detail', args=[11, 11, 11])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)
