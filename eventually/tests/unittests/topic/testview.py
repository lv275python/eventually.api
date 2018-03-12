"""
Topic View tests
======================
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from curriculum.models import Curriculum
from topic.models import Topic
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class TestTopicView(TestCase):
    """ Tests for Topic views """

    def setUp(self):

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            custom_user = CustomUser.objects.create(id=123,
                                                    email='email1@mail.com',
                                                    first_name='1fname',
                                                    middle_name='1mname',
                                                    last_name='1lname',
                                                    is_active=True)
            custom_user.set_password('1111')
            custom_user.save()

            Curriculum.objects.create(id=111,
                                      name="testcurriculum",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      team=None)

            Topic.objects.create(id=212,
                                 curriculum=Curriculum.get_by_id(111),
                                 author=custom_user,
                                 title='Topic #1',
                                 description="t_descr",
                                 mentors=(custom_user,))

            Topic.objects.create(id=213,
                                 curriculum=Curriculum.get_by_id(111),
                                 author=custom_user,
                                 title='Topic #2',
                                 description="t_descr",
                                 mentors=(custom_user, ))

        self.client = Client()
        self.client.login(username='email1@mail.com', password='1111')

    def test_success_get_by_curriculum_id(self):
        """Method that tests the successful get request for the all topics"""

        expected_data = {'topics': [{'id': 213,
                                     'curriculum': 111,
                                     'author': 123,
                                     'created_at': 1509344112,
                                     'updated_at': 1509344112,
                                     'title': 'Topic #2',
                                     'description': "t_descr",
                                     'mentors': [123]},
                                    {'id': 212,
                                     'curriculum': 111,
                                     'author': 123,
                                     'created_at': 1509344112,
                                     'updated_at': 1509344112,
                                     'title': 'Topic #1',
                                     'description': "t_descr",
                                     'mentors': [123]}]}

        url = reverse('curriculums:topics:index', args=[111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_by_topic_id(self):
        """Method that tests the successful get request for the topic with the certain id"""

        expected_data = {'id': 213,
                         'curriculum': 111,
                         'author': 123,
                         'created_at': 1509344112,
                         'updated_at': 1509344112,
                         'title': 'Topic #2',
                         'description': "t_descr",
                         'mentors': [123]}

        url = reverse('curriculums:topics:detail', args=[111, 213])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_get_by_curriculum_invalid_id(self):
        """Method that tests the unsuccessful get request for the all topics"""

        url = reverse('curriculums:topics:index', args=[112])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unsuccess_get_by_invalid_topic_id(self):
        """Method that tests the unsuccessful get request for the topic with the certain id"""

        url = reverse('curriculums:topics:detail', args=[111, 215])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_post(self):
        """Method that tests the success post request for creating of topic."""

        data = {'title': 'some new curriculum',
                'description': 'short description',
                'mentors': ()}

        url = reverse('curriculums:topics:index', args=[111])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_error_post_no_data(self):
        """Method that tests the unsuccessful post request for creating of topic with no data."""

        data = {}

        url = reverse('curriculums:topics:index', args=[111])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_post_invalid_curriculum_id(self):
        """Method that tests the unsuccessful post request for creating of topic with invalid
        curriculum id."""

        data = {'title': 'some new curriculum',
                'description': 'short description',
                'mentors': ()}

        url = reverse('curriculums:topics:index', args=[114])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_db_creating_topic(self):
        """Method that tests unsuccessful post request when db creating is failed."""
        with mock.patch('topic.models.Topic.create') as topic_create:
            topic_create.return_value = None
            data = {'name': 'some new curriculum',
                    'mentors': (),
                    'description': 'short description'}
            url = reverse('curriculums:topics:index', args=[111])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 501)

    def test_method_is_topic_mentor(self):
        """Method that tests 'is_topic_mentor' function."""
        expected_data = {'is_mentor': True}
        url = reverse('curriculums:topics:is_topic_mentor', args=[111, 212])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))
