"""
Assignment View tests
======================
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from assignment.models import Assignment
from item.models import Item
from curriculum.models import Curriculum
from topic.models import Topic
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class TestAssignmentApp(TestCase):
    """ Tests for Curriculum app model """

    def setUp(self):
        custom_user = CustomUser.objects.create(id=1,
                                                email='email.1@mail.com',
                                                first_name='1fname',
                                                middle_name='1mname',
                                                last_name='1lname',
                                                is_active=True)
        custom_user.set_password('1111')
        custom_user.save()

        custom_user = CustomUser.objects.create(id=2,
                                                email='email.2@mail.com',
                                                first_name='2fname',
                                                middle_name='2mname',
                                                last_name='2lname',
                                                is_active=True)

        custom_user.set_password('1111')
        custom_user.save()

        self.client = Client()
        self.client.login(username='email.1@mail.com', password='1111')

        Curriculum.objects.create(id=111,
                                  name="testcurriculum",
                                  goals=["goal1", "goal2"],
                                  description="some_description",
                                  )

        Topic.objects.create(id=222,
                             curriculum=Curriculum.get_by_id(111),
                             author=CustomUser.get_by_id(1),
                             title='Topic #1',
                             description="test_description",
                             mentors=(CustomUser.get_by_id(1),))

        Topic.objects.create(id=223,
                             curriculum=Curriculum.get_by_id(111),
                             author=CustomUser.get_by_id(2),
                             title='Topic #1',
                             description="test_description",
                             mentors=(CustomUser.get_by_id(2),))

        Item.objects.create(id=333,
                            topic=Topic.get_by_id(222),
                            authors=(CustomUser.get_by_id(1),),
                            name='Item #1',
                            form=0,
                            description='description')

        Item.objects.create(id=334,
                            topic=Topic.get_by_id(222),
                            authors=(CustomUser.get_by_id(1),),
                            name='Item #2',
                            form=0,
                            description='description',
                            superiors=[333])

        Item.objects.create(id=335,
                            topic=Topic.get_by_id(223),
                            authors=(CustomUser.get_by_id(1),),
                            name='Item #3',
                            form=0,
                            description='description')

        Assignment.objects.create(id=444,
                                  user=CustomUser.get_by_id(1),
                                  item=Item.get_by_id(333))

        Assignment.objects.create(id=445,
                                  user=CustomUser.get_by_id(1),
                                  item=Item.get_by_id(334))

    def test_success_get_by_id(self):
        """Method that tests the successful get request for the Assignment with the certain id"""
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            Assignment.objects.create(
                id=111,
                statement='my_statement1',
                grade=True,
                user=CustomUser.get_by_id(1),
                item=Item.get_by_id(333),
                status=2
            )

            url = reverse('assignment:AssignmentAnswer')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 201)

    def test_failed_get_by_id(self):
        """Method that tests the successful get request for the Assignment with the certain id"""
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.objects.filter.return_value = False
            url = reverse('assignment:AssignmentAnswer')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)


class AssignmentFunctionViewTestCase(TestCase):
    def setUp(self):
        self.custom_user = CustomUser.objects.create(id=1,
                                                     email='email.1@mail.com',
                                                     first_name='1fname',
                                                     middle_name='1mname',
                                                     last_name='1lname',
                                                     is_active=True)
        self.custom_user.set_password('1111')
        self.custom_user.save()

        self.curriculum = Curriculum.objects.create(id=111,
                                                    name="testcurriculum",
                                                    goals=["goal1", "goal2"],
                                                    description="some_description",
                                                    owner=self.custom_user
                                                    )

        self.topic = Topic.objects.create(id=222,
                                          curriculum=self.curriculum,
                                          author=self.custom_user,
                                          title='Topic #1',
                                          description="test_description",
                                          mentors=[self.custom_user])

        self.item = Item.objects.create(id=333,
                                        topic=self.topic,
                                        authors=[self.custom_user],
                                        name='Item #1',
                                        form=0,
                                        description='description')

        self.assignment = Assignment.objects.create(id=444,
                                                    user=self.custom_user,
                                                    item=self.item)

        self.client = Client()
        self.client.login(username='email.1@mail.com', password='1111')

    def test_get_curriculum_list_positive(self):
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.get_curriculums.return_value = [self.curriculum]
            response = self.client.get(reverse('assignment:curriculums'))

            self.assertEqual(response.status_code, 200)

    def test_get_curriculum_list_negative(self):
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.get_curriculums.return_value = None
            response = self.client.get(reverse('assignment:curriculums'))

            self.assertEqual(response.status_code, 404)

    def test_get_topic_list_positive(self):
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.get_topics.return_value = [self.topic]
            url = reverse('assignment:topics', kwargs={'curriculum_id': 111})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_get_topic_list_negative(self):
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.get_topics.return_value = None
            url = reverse('assignment:topics', kwargs={'curriculum_id': 111})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 404)

    def test_get_assignment_list_user_id(self):
        with mock.patch('assignment.views.CustomUser') as mock_user:
            with mock.patch('assignment.views.Assignment') as mock_assignment:
                mock_user.get_by_id.return_value = self.custom_user
                mock_assignment.get_assignment_by_mentor_id.return_value = [self.assignment]
                url = reverse('assignment:assignment_list', kwargs={'topic_id':222, 'user_id':111})
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)

    def test_get_assignment_list_not_user_id(self):
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.get_assignments_by_student_topic_item_ids.return_value = [self.assignment]
            url = reverse('assignment:assignment_list_students', kwargs={'topic_id':222})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_get_assignment_list_negative(self):
        with mock.patch('assignment.views.Assignment') as mock_assignment:
            mock_assignment.get_assignments_by_student_topic_item_ids.return_value = None
            url = reverse('assignment:assignment_list_students', kwargs={'topic_id':222})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 404)

    def test_send_answer_positive(self):
        with mock.patch('assignment.views.CustomUser') as mock_user:
            mock_user.get_by_id.return_value = self.custom_user
            url = reverse('assignment:SendAnswer')
            data = {'userId': None, 'message': None}
            response = self.client.post(url, json.dumps(data), content_type='application/json')

            self.assertEqual(response.status_code, 200)

    def test_send_answer_not_data(self):
        url = reverse('assignment:SendAnswer')
        data = {}
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_send_answer_not_user(self):
        with mock.patch('assignment.views.CustomUser') as mock_user:
            mock_user.get_by_id.return_value = None
            url = reverse('assignment:SendAnswer')
            data = {'userId': None, 'message': None}
            response = self.client.post(url, json.dumps(data), content_type='application/json')

            self.assertEqual(response.status_code, 400)

    def test_send_answer_wrong_method(self):
        url = reverse('assignment:SendAnswer')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)