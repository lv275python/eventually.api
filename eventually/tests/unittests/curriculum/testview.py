"""
Curriculum View tests
======================
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from curriculum.models import Curriculum
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class TestCurriculumApp(TestCase):
    """ Tests for Curriculum app model """

    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            custom_user = CustomUser.objects.create(id=1,
                                                    email='email1@mail.com',
                                                    first_name='1fname',
                                                    middle_name='1mname',
                                                    last_name='1lname',
                                                    is_active=True)
            custom_user.set_password('1111')
            custom_user.save()

            custom_user_second = CustomUser.objects.create(id=2,
                                                           email='easdmail1@mail.com',
                                                           first_name='1fname',
                                                           middle_name='1mname',
                                                           last_name='1lname',
                                                           is_active=True)
            custom_user_second.set_password('122111')
            custom_user_second.save()

            Curriculum.objects.create(id=111,
                                      name="testcurriculum",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      owner=custom_user)

            Curriculum.objects.create(id=112,
                                      name="tes",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      owner=custom_user)

        self.client = Client()
        self.client.login(username='email1@mail.com', password='1111')

        self.client_second = Client()
        self.client_second.login(username='easdmail1@mail.com', password='122111')

    def test_success_get_all(self):
        """Method that tests the successful get request for the all curriculums"""

        expected_data = {'curriculums': [{'id': 111,
                                          'name': "testcurriculum",
                                          'description': "t_descr",
                                          'goals': ["goal1", "goal2"],
                                          'owner': 1,
                                          'created': 1509344112,
                                          'updated': 1509344112},
                                         {'id': 112,
                                          'name': "tes",
                                          'description': "t_descr",
                                          'goals': ["goal1", "goal2"],
                                          'owner': 1,
                                          'created': 1509344112,
                                          'updated': 1509344112}
                                         ]}

        url = reverse('curriculums:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_by_id(self):
        """Method that tests the successful get request for the curriculum with the certain id"""
        expected_data = {'id': 111,
                         'name': "testcurriculum",
                         'description': "t_descr",
                         'goals': ["goal1", "goal2"],
                         'owner': 1,
                         'created': 1509344112,
                         'updated': 1509344112}
        url = reverse('curriculums:detail', args=[111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_post(self):
        """Method that tests the successful post request for creating of curriculum."""
        data = {'title': 'some new curriculum', 'owner': 1,
                'description': 'short description'}

        url = reverse('curriculums:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_error_post_no_data(self):
        """Method that tests the unsuccessful post request for creating curriculum
        with no data."""

        data = {}

        url = reverse('curriculums:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_error_invalid_data(self):
        """Method that tests the unsuccessful post request for creating curriculum
        with invalid data."""

        data = {'name': 'some new curriculum',
                'name': 'short description'}

        url = reverse('curriculums:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_success(self):
        """Method that tests success put request for the updating the certain curriculum."""

        data = {'name': 'some updated curriculum',
                'description': 'short description'}

        url = reverse('curriculums:detail', args=[111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_empty_data(self):
        """Method that tests success put request for the updating the certain curriculum."""

        data = {}

        url = reverse('curriculums:detail', args=[111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_unsuccess(self):
        """Method that tests unsuccess put request for the updating the certain curriculum."""

        data = {'name': 'some updated curriculum',
                'description': 'short description'}

        url = reverse('curriculums:detail', args=[1111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_invalid_owner(self):
        """Method that tests unsuccess put request for the updating the certain curriculum."""

        data = {'name': 'some updated curriculum',
                'description': 'short description'}

        url = reverse('curriculums:detail', args=[111])
        response = self.client_second.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_delete_success(self):
        """Method that tests successful delete curriculum"""
        url = reverse('curriculums:detail', args=[111])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_unsuccess(self):
        """Method that tests successful delete curriculum"""
        url = reverse('curriculums:detail', args=[1111])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_permisions_denide(self):
        """Method that tests successful delete curriculum"""
        url = reverse('curriculums:detail', args=[111])
        response = self.client_second.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_error(self):
        """Method that tests successful delete curriculum"""
        with mock.patch('curriculum.models.Curriculum.delete_by_id') as curriculum_delete:
            curriculum_delete.return_value = None
            url = reverse('curriculums:detail', args=[111])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)
