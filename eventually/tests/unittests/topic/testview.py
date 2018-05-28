"""
Topic View tests
======================
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.cache import cache
from django.core.urlresolvers import reverse
from curriculum.models import Curriculum
from topic.models import Topic
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class TestTopicView(TestCase):
    """ Tests for Topic views """

    def setUp(self):

        with mock.patch('django.utils.timezone.now') as mock_time:
            cache.clear()
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

            custom_user = CustomUser.objects.create(id=124,
                                                     email='email2@mail.com',
                                                     first_name='2fname',
                                                     middle_name='2mname',
                                                     last_name='2lname',
                                                     is_active=True)
            custom_user.set_password('2222')
            custom_user.save()

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

    def test_unsuccessful_get_by_invalid_topic_id(self):
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

    def test_topic_success_delete(self):
        """Method that tests the successful delete request."""
        url = reverse('curriculums:topics:delete', args=[111, 213])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_topic_error_delete_no_topic(self):
        """Method that tests the unsuccessful delete request with invalid topic."""
        url = reverse('curriculums:topics:delete', args=[111, 215])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_error_delete_db_error(self):
        """Method that tests the unsuccessful delete request with db error."""
        with mock.patch('topic.models.Topic.delete_by_id') as topic_delete:
            topic_delete.return_value = None
            url = reverse('curriculums:topics:delete', args=[111, 213])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)

    def test_topic_delete_error_access_denied(self):
        """Method that tests the unsuccessful delete request with no rights."""
        self.client = Client()
        self.client.login(username='email2@mail.com', password='2222')
        url = reverse('curriculums:topics:delete', args=[111, 213])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_method_is_topic_mentor(self):
        """Method that tests 'is_topic_mentor' function."""
        expected_data = {'is_mentor': True}
        url = reverse('curriculums:topics:is_topic_mentor', args=[111, 212])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))


    def test_error_put_no_data(self):
        """Method that tests the unsuccessful put request for updating a topic with no data."""

        data = {}

        url = reverse('curriculums:topics:detail', args=[111, 212])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_put_wrong_topic_id(self):
        """Method that tests the unsuccessful put request for updating a topic with wrong topic_id."""

        data = {'title': 'some new curriculum',
                'description': 'short description',
                'mentors': ()}

        url = reverse('curriculums:topics:detail', args=[111, 2120])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_put_user_not_in_topic_mentor(self):
        """Method that tests the unsuccessful put request for updating a topic when user is not a topic mentor"""

        Topic.objects.create(id=214,
                             curriculum=Curriculum.get_by_id(111),
                             author=CustomUser.get_by_id(123),
                             title='Topic #3',
                             description="t_descr",
                             mentors=(CustomUser.get_by_id(124),))

        data = {'title': 'some new curriculum',
                'description': 'short description',
                'mentors': ()}

        url = reverse('curriculums:topics:detail', args=[111, 214])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_success_topic_put(self):
        """Method that tests the successful put request"""

        data = {'title': 'some new curriculum',
                'description': 'short description',
                'mentors': ()}

        url = reverse('curriculums:topics:detail', args=[111, 212])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_success_add_mentors(self):
        """Method that tests the successful put request for adding mentor"""

        data = {'title': 'some new curriculum',
                'description': 'short description',
                'addMentors': [124]}

        url = reverse('curriculums:topics:detail', args=[111, 212])
        response = self.client.put(url, json.dumps(data), content_type='application/json')

        topic_1 = Topic.get_by_id(212)
        topic_1_dict = topic_1.to_dict()

        self.assertEqual(topic_1_dict.get('mentors'), [123, 124])

    def test_success_mentors_topics(self):
        """Method that tests the successful call of mentors_topics"""

        topic_1 = Topic.get_by_id(212)
        topic_2 = Topic.get_by_id(213)
        expected_data = {'topics': [topic_1.to_dict(), topic_2.to_dict()]}

        url = reverse('mentor:mentors_topics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))
