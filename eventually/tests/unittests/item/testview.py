"""
Item View tests
======================
"""

import json
import datetime
from authentication.models import CustomUser
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from curriculum.models import Curriculum
from item.models import Item
from topic.models import Topic
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class TestItemView(TestCase):
    """ Tests for Item views """

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

            custom_user = CustomUser.objects.create(id=124,
                                                    email='email2@mail.com',
                                                    first_name='2fname',
                                                    middle_name='2mname',
                                                    last_name='2lname',
                                                    is_active=True)
            custom_user.set_password('2222')
            custom_user.save()

            custom_user = CustomUser.objects.create(id=125,
                                                    email='email3@mail.com',
                                                    first_name='3fname',
                                                    middle_name='3mname',
                                                    last_name='3lname',
                                                    is_active=True)
            custom_user.set_password('3333')
            custom_user.save()

            Curriculum.objects.create(id=111,
                                      name="testcurriculum",
                                      goals=["goal1", "goal2"],
                                      description="t_descr")

            Topic.objects.create(id=212,
                                 curriculum=Curriculum.get_by_id(111),
                                 author=CustomUser.get_by_id(123),
                                 title='Topic #1',
                                 description="t_descr",
                                 mentors=[CustomUser.get_by_id(123), CustomUser.get_by_id(124)])

            Item.objects.create(id=311,
                                topic=Topic.get_by_id(212),
                                authors=[CustomUser.get_by_id(123), CustomUser.get_by_id(124)],
                                name='Node.js',
                                form=1,
                                description='description')

            Item.objects.create(id=312,
                                topic=Topic.get_by_id(212),
                                authors=[CustomUser.get_by_id(123), CustomUser.get_by_id(124)],
                                name='Item Name',
                                form=1,
                                description='second description')

        self.client = Client()
        self.client.login(username='email1@mail.com', password='1111')

    def test_success_get_by_item_id(self):
        """Method that tests the successful get request for the certain item"""

        expected_data = {'id': 311,
                         'name': 'Node.js',
                         'authors': [123, 124],
                         'topic': 212,
                         'form': 1,
                         'superiors': [],
                         'description': 'description',
                         'estimation': None,
                         'created_at': 1509344112,
                         'updated_at': 1509344112}
        url = reverse('curriculums:topics:items:detail', args=[111, 212, 311])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_error_get_by_wrong_id(self):
        """
        Method that tests the unsuccessful get request for the certain item with wrong item id
        """

        url = reverse('curriculums:topics:items:detail', args=[111, 212, 211])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_get_by_topic_id(self):
        """Method that tests the successful get request for all topic items"""

        expected_data = {'items': [{'id': 312,
                                    'name': 'Item Name',
                                    'authors': [123, 124],
                                    'topic': 212,
                                    'form': 1,
                                    'superiors': [],
                                    'description': 'second description',
                                    'estimation': None,
                                    'created_at': 1509344112,
                                    'updated_at': 1509344112},
                                   {'id': 311,
                                    'name': 'Node.js',
                                    'authors': [123, 124],
                                    'topic': 212,
                                    'form': 1,
                                    'superiors': [],
                                    'description': 'description',
                                    'estimation': None,
                                    'created_at': 1509344112,
                                    'updated_at': 1509344112}
                                   ]}
        url = reverse('curriculums:topics:items:index', args=[111, 212])
        response = self.client.get(url)
        response_date = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response_date, expected_data)

    def test_error_get_by_wrong_topic_id(self):
        """Method that tests the unsuccessful get request with wrong topic id"""

        url = reverse('curriculums:topics:items:index', args=[111, 215])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_post(self):
        """Method that tests the successful post request for creating of item."""

        data = {'name': 'some new item',
                'description': 'short description',
                'form': 1}

        url = reverse('curriculums:topics:items:index', args=[111, 212])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_error_post_no_data(self):
        """Method that tests the unsuccessful post request for creating of item with no data."""

        data = {}

        url = reverse('curriculums:topics:items:index', args=[111, 212])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_post_invalid_topic_id(self):
        """
        Method that tests the unsuccessful post request for creating of item with
        invalid topic id.
        """

        data = {'name': 'some new curriculum',
                'description': 'short description',
                'form': 0}

        url = reverse('curriculums:topics:items:index', args=[111, 216])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_post_access_denied(self):
        """
        Method that tests the unsuccessful post request for creating of item with no rights.
        """

        data = {'name': 'some new curriculum',
                'description': 'short description',
                'form': 0}

        self.client = Client()
        self.client.login(username='email3@mail.com', password='3333')

        url = reverse('curriculums:topics:items:index', args=[111, 212])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_post_db_creating_error(self):
        """
        Method that tests the unsuccessful post request when db creating is failed.
        """
        with mock.patch('item.models.Item.create') as item_create:
            item_create.return_value = None
            data = {'name': 'some new item',
                    'description': 'short description',
                    'form': 0}
            url = reverse('curriculums:topics:items:index', args=[111, 212])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 501)

    def test_put_success(self):

        data = {
            'superiors':[],
            'estimation':None
        }

        url = reverse('curriculums:topics:items:detail', args=[111,212,311])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_put_if_not_item(self):
        data = {'name': 'some updated item',
                'description': 'another description',
                'form': 1}
        url = reverse('curriculums:topics:items:detail', args=[111, 212, 500])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_if_not_topic(self):
        data = {'name': 'some updated item',
                'description': 'another description',
                'form': 1}
        url = reverse('curriculums:topics:items:detail', args=[111, 500, 311])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_is_user_not_a_mentor(self):
        self.client_second = Client()
        self.client_second.login(username='email3@mail.com', password='3333')

        data = {'name': 'some updated item',
                            'description': 'another description',
                            'form': 1}

        url = reverse('curriculums:topics:items:detail', args=[111, 212, 311])
        response = self.client_second.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)


    def test_put_if_not_data(self):
        data = {}
        url = reverse('curriculums:topics:items:detail', args=[111, 212, 311])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_if_not_topic(self):
        url = reverse('curriculums:topics:items:delete', args=[111, 500, 311])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_if_not_item(self):
        url = reverse('curriculums:topics:items:delete', args=[111, 212, 500])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_if_user_not_mentor(self):
        self.client_second = Client()
        self.client_second.login(username='email3@mail.com', password='3333')
        url = reverse('curriculums:topics:items:delete', args=[111, 212, 311])
        response = self.client_second.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_success(self):
        url = reverse('curriculums:topics:items:delete', args=[111, 212, 311])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_not_success(self):
        with mock.patch('item.models.Item.delete_by_id') as item_delete:
            item_delete.return_value = None
            url = reverse('curriculums:topics:items:detail', args=[111, 212, 311])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 400)
