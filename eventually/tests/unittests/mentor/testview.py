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

        expected_data = {
            'my_students': [{'created_at': 1508044512,
                             'email': 'email2@gmail.com',
                             'first_name': 'anton',
                             'id': 102,
                             'is_active': True,
                             'last_name': 'shulga',
                             'middle_name': 'frensis',
                             'updated_at': 1508044512}],
            'assigned_students': [],
            'available_students': []
        }

        url = reverse('mentor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_filter(self):
        """Method that tests the successful get request with filters data  """

        data = {
            'topic': 200,
            'is_done': 0,
            'from': 1508044512,
            'to': 1508044512
        }

        url = reverse('mentor')
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)

    def test_mentor_success_post(self):
        """Method that tests the success post request."""

        data = {

            'student': 103,
            'topicId': 200
        }
        url = reverse('mentor')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_mentor_invalid_data_post(self):
        """Method that tests the unsuccessful post request. db error."""

        with mock.patch('mentor.models.MentorStudent.create') as mentor_create:
            mentor_create.return_value = None

            data = {
                'student': 103,
                'topic': 201,
            }

            url = reverse('mentor')
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_mentor_updated_post(self):
        """Method that tests the success post request to update mentor."""

        data = {
            'mentor': 100,
            'student': 102,
            'topic': 200
        }
        url = reverse('mentor')
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_invalid_student_post(self):
        """Method that tests the unsuccessful post request with invalid student."""

        data = {
            'mentor': 100,
            'student': 999,
            'topic': 200,
            'is_done': 0
        }
        url = reverse('mentor')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_mentor_post(self):
        """Method that tests the unsuccessful post request with invalid mentor."""

        data = {
            'mentor': '102',
            'student': '103',
            'topic': 200,
            'is_done': 0
        }
        url = reverse('mentor')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_get_mentors(self):
        """Method that tests the successful get request for the all mentors list for the certain student."""

        url = reverse('mentors_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_success_get_students(self):
        """Method that tests the successful get request for the all students list for the certain mentor."""

        url = reverse('students_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
