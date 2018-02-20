"""
MentorStudent View Test
================

This module provides complete testing for all MentorStudent's view functions.
"""
import json
import datetime
from unittest import mock
from django.test import TestCase, Client
from authentication.models import CustomUser
from topic.models import Topic
from curriculum.models import Curriculum
from mentor.models import MentorStudent
from team.models import Team
from django.core.urlresolvers import reverse


TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class MentorStudentViewTestCase(TestCase):
    """TestCase for providing MentorStudent view testing"""

    def setUp(self):
        """Method that provides preparation before testing MentorStudent view features."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user_first = CustomUser(id=100,
                                           first_name='petro',
                                           last_name='hanchuk',
                                           middle_name='mykola',
                                           email='email0@gmail.com',
                                           is_active=True)
            custom_user_first.set_password('Pas0')
            custom_user_first.save()

            custom_user_second = CustomUser(id=102,
                                            first_name='anton',
                                            last_name='shulga',
                                            middle_name='frensis',
                                            email='email2@gmail.com',
                                            is_active=True)
            custom_user_second.set_password('Pas2')
            custom_user_second.save()

            custom_user_third = CustomUser(id=103,
                                           first_name='fedir',
                                           last_name='bogolubov',
                                           middle_name='sergiy',
                                           email='email3@gmail.com',
                                           is_active=True)
            custom_user_third.set_password('Pas3')
            custom_user_third.save()

            team = Team(id=400,
                        owner=custom_user_first,
                        name='Coldplay')
            team.save()
            team.members.add(custom_user_first, custom_user_second, custom_user_third)

            curriculum = Curriculum.objects.create(id=300,
                                                   name="testcurriculum",
                                                   goals=["goal1", "goal2"],
                                                   description="test_descr",
                                                   team=team)
            curriculum.save()

            topic_python = Topic(id=200,
                                 curriculum=curriculum,
                                 title='Python',
                                 description='My awesome topic')
            topic_python.save()

            topic_react = Topic(id=201,
                                curriculum=curriculum,
                                author=custom_user_first,
                                title='React',
                                description='My awesome topic')
            topic_react.save()

            mentor = MentorStudent(id=500,
                                   mentor=custom_user_first,
                                   student=custom_user_second,
                                   topic=topic_python,
                                   is_done=0)
            mentor.save()

        self.client = Client()
        self.client.login(username='email0@gmail.com', password='Pas0')

    def test_success_get_all(self):
        """Method that tests the successful get request for the certain mentors."""

        expected_data = {'my_students': [{'created_at': 1508044512,
                                          'email': 'email2@gmail.com',
                                           'first_name': 'anton',
                                           'id': 102,
                                           'is_active': True,
                                           'last_name': 'shulga',
                                           'middle_name': 'frensis',
                                           'updated_at': 1508044512}],
                         'assigned_students': [],
                         'available_students': []}

        url = reverse('mentor:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_filter(self):
        """Method that tests the successful get request with filters data  """

        data = {'topic': 200,
                'is_done': 0,
                'from': 1508044512,
                'to': 1508044512}

        url = reverse('mentor:index')
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)

    def test_mentor_success_post(self):
        """Method that tests the successful post request."""

        data = {'student': 103,
                'topicId': 200}
        url = reverse('mentor:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_mentor_error_no_data_post(self):
        """Method that tests the unsuccessful post request with no data."""

        data = {}
        url = reverse('mentor:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_mentor_error_post_not_topic(self):
        """Method that tests the unsuccessful post request with invalid topic_id."""

        data = {'topicId': 205}
        url = reverse('mentor:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_mentor_error_post_student_is_author(self):
        """Method that tests the unsuccessful post request with student id the same as
        topic's author id."""

        data = {'topicId': 201}
        url = reverse('mentor:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_mentor_error_post_is_already_in_db(self):
        """Method that tests the unsuccessful post request when student is already assigned
        to the certain topic."""

        self.client = Client()
        self.client.login(username='email2@gmail.com', password='Pas2')
        data = {'topicId': 200}
        url = reverse('mentor:index')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_mentor_error_creating_db_post(self):
        """Method that tests the unsuccessful post request. db error."""

        with mock.patch('mentor.models.MentorStudent.create') as mentor_create:
            mentor_create.return_value = None

            self.client = Client()
            self.client.login(username='email3@gmail.com', password='Pas3')

            data = {'topicId': 201}

            url = reverse('mentor:index')
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_mentor_updated_put(self):
        """Method that tests the success put request to update mentor."""
        with mock.patch('mentor.models.MentorStudent.create') as mentor_create:
            self.client = Client()
            self.client.login(username='email2@gmail.com', password='Pas2')
            data = {'mentor': 100,
                    'student': 102,
                    'topic': 200}
            url = reverse('mentor:index')
            response = self.client.put(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_mentor_error_put_invalid_data(self):
        """Method that tests the unsuccessful put request to update mentor with invalid data."""

        data = {}
        url = reverse('mentor:index')
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_mentor_error_put_no_student(self):
        """Method that tests the unsuccessful put request to update mentor."""

        data = {'mentor': 100,
                'topic': 200}
        url = reverse('mentor:index')
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_mentor_success_delete(self):
        """Method that tests the successful delete request."""

        self.client = Client()
        self.client.login(username='email2@gmail.com', password='Pas2')

        data = {'topic': 200}

        url = reverse('mentor:delete', args=[200])
        response = self.client.delete(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_mentor_error_object_not_found(self):
        """Method that tests the unsuccessful delete request. Object not found."""

        data = {'topic': 200}

        url = reverse('mentor:delete', args=[200])
        response = self.client.delete(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_mentor_error_db_operation_failed_delete(self):
        """Method that tests the unsuccessful delete request. DB operation failed."""

        with mock.patch('mentor.models.MentorStudent.delete_by_id') as mentor_delete:
            mentor_delete.return_value = None
            self.client = Client()
            self.client.login(username='email2@gmail.com', password='Pas2')
            data = {'topic': 200}

            url = reverse('mentor:delete', args=[200])
            response = self.client.delete(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_mentor_success_get_mentors(self):
        """Method that tests the successful get_mentors request."""

        self.client = Client()
        self.client.login(username='email2@gmail.com', password='Pas2')
        expected_data = {'receivers': [{'created_at': 1508044512,
                                        'email': 'email0@gmail.com',
                                        'first_name': 'petro',
                                        'id': 100,
                                        'is_active': True,
                                        'last_name': 'hanchuk',
                                        'middle_name': 'mykola',
                                        'updated_at': 1508044512}]}

        url = reverse('mentor:mentors_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_mentor_success_get_students(self):
        """Method that tests the successful get_students request."""

        self.client = Client()
        self.client.login(username='email0@gmail.com', password='Pas0')
        expected_data = {'receivers': [{'created_at': 1508044512,
                                        'email': 'email2@gmail.com',
                                        'first_name': 'anton',
                                        'id': 102,
                                        'is_active': True,
                                        'last_name': 'shulga',
                                        'middle_name': 'frensis',
                                        'updated_at': 1508044512}]}

        url = reverse('mentor:students_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_mentor_success__is_topic_student(self):
        """Method that tests the successful is_topic_student request."""

        self.client = Client()
        self.client.login(username='email2@gmail.com', password='Pas2')
        expected_data = {'is_student': True}

        url = reverse('mentor:is_topic_student', args=[200])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))
