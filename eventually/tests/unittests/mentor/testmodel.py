"""
MentorStudent Model Test

This module provides complete testing for all Mentor's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from authentication.models import CustomUser
from topic.models import Topic
from curriculum.models import Curriculum
from mentor.models import MentorStudent
from team.models import Team


TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)

class MentorModelTestCase(TestCase):
    """TestCase for providing MentorStudent model testing"""

    def setUp(self):
        """Method that provides preparation before testing MentorStudent model's features."""
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user_first = CustomUser(id=100,
                                           first_name='petro',
                                           last_name='hanchuk',
                                           middle_name='mykola',
                                           email='email0@gmail.com')
            custom_user_first.set_password('Pas0')
            custom_user_first.save()

            custom_user_second = CustomUser(id=102,
                                            first_name='anton',
                                            last_name='shulga',
                                            middle_name='frensis',
                                            email='email2@gmail.com')
            custom_user_first.set_password('Pas2')
            custom_user_second.save()

            custom_user_third = CustomUser(id=103,
                                           first_name='fedir',
                                           last_name='bogolubov',
                                           middle_name='sergiy',
                                           email='email3@gmail.com')
            custom_user_first.set_password('Pas3')
            custom_user_third.save()

            team = Team(id=400,
                        owner=custom_user_first,
                        name='Coldplay')
            team.save()
            team.members.add(custom_user_second, custom_user_third)

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

            mentor = MentorStudent(id=500,
                                   mentor=custom_user_first,
                                   student=custom_user_second,
                                   topic=topic_python,
                                   is_done=0)
            mentor.save()

            mentor = MentorStudent(id=501,
                                   mentor=custom_user_first,
                                   student=custom_user_third,
                                   topic=topic_python,
                                   is_done=1)
            mentor.save()

            mentor = MentorStudent(id=502,
                                   mentor=None,
                                   student=custom_user_third,
                                   topic=topic_python,
                                   is_done=1)
            mentor.save()

    def test_mentor_to_dict(self):
        """Method that tests `to_dict` method of certain MentorStudent instance."""

        mentor = MentorStudent.objects.get(id=500)

        expect_mentor_dict = {
            'id': 500,
            'mentor':100,
            'student': 102,
            'topic': 200,
            'is_done': 0,
            'created_at': 1508044512,
            'updated_at': 1508044512
        }

        actual_mentor_dict = mentor.to_dict()

        self.assertDictEqual(actual_mentor_dict, expect_mentor_dict)

    def test_mentor_success_create(self):

        """Method that tests succeeded `create` method of MentorStudent class object."""

        student = CustomUser.objects.get(id=102)
        topic = Topic.objects.get(id=200)

        created_mentor = MentorStudent.create(student=student,
                                              topic=topic)

        self.assertIsInstance(created_mentor, MentorStudent)

    def test_mentor_none_create(self):
        """Method that tests unsucceeded `create` method of MentorStudent class object."""

        student = CustomUser.objects.get(id=102)
        topic = Topic()

        created_mentor = MentorStudent.create(student=student,
                                              topic=topic)

        self.assertIsNone(created_mentor)

    def test_mentor_update(self):
        """Method that tests `update` method of certain MentorStudent instance."""

        actual_mentor = MentorStudent.objects.get(id=500)
        student = CustomUser.objects.get(id=103)
        topic = Topic.objects.get(id=200)
        mentor = CustomUser.objects.get(id=102)

        actual_mentor.update(mentor=mentor, student=student, topic=topic, is_done=1)
        expected_mentor = MentorStudent.objects.get(id=500)

        self.assertEqual(actual_mentor, expected_mentor)

    def test_mentor_get_my_students(self):
        """Method that tests "get_my_students" method of MentorStudent class object."""

        get_my_students = MentorStudent().get_my_students(100)
        result = [student for student in get_my_students]
        expected_result = [MentorStudent(id=500), MentorStudent(id=501)]

        self.assertEqual(result, expected_result)

    def test_mentor_get_my_mentors(self):
        """Method that tests "get_my_mentors" method of MentorStudent class object."""

        get_my_mentors = MentorStudent().get_my_mentors(102)
        result = [mentor for mentor in get_my_mentors]
        expected_result = [MentorStudent(id=500)]
        self.assertEqual(result, expected_result)

    def test_mentor_get_all_students(self):
        """Method that tests "get_all_students" method of MentorStudent class object."""

        get_assigned_students = MentorStudent().get_assigned_students(102)
        result = [student for student in get_assigned_students]
        expected_result = [MentorStudent(id=500), MentorStudent(id=501)]
        self.assertEqual(result, expected_result)

    def test_mentor_get_available_students(self):
        """Method that tests "get_available_students" method of MentorStudent class object."""

        get_available_students = MentorStudent().get_available_students()
        result = [student for student in get_available_students]
        expected_result = [MentorStudent(id=502)]
        self.assertEqual(result, expected_result)
