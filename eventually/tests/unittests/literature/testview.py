"""
Literature view tests
================

This module provides complete testing for all Literature views functions.
"""

import datetime
import json
from unittest import mock
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from authentication.models import CustomUser
from item.models import Item
from literature.models import LiteratureItem
from topic.models import Topic

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)


class LiteratureItemViewTest(TestCase):
    """TestCase for providing Literature view testing."""

    def setUp(self):
        """Method that provides preparation before testing Literature view's features."""

        custom_user_first = CustomUser.objects.create(id=101, email='email@gmail.com', is_active=True)
        custom_user_first.set_password('123Qwerty')
        custom_user_first.save()

        custom_user_second = CustomUser.objects.create(id=102, email='potter@gmail.com', is_active=True)
        custom_user_second.set_password('123ABCabc')
        custom_user_second.save()

        topic = Topic.objects.create(id=68, title='Topic', description='New skills')
        topic.save()
        item = Item.objects.create(id=16, form=1, topic_id=68)
        item.save()

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            literature_first = LiteratureItem.objects.create(id=10,
                                                             title='Book One',
                                                             description='Book for Java',
                                                             source='www.online.com',
                                                             author=custom_user_first,
                                                             item_id=16)
            literature_first.save()

        self.client_first = Client()
        self.client_first.login(username='email@gmail.com', password='123Qwerty')

        self.client_second = Client()
        self.client_second.login(username='potter@gmail.com', password='123ABCabc')

    def test_success_get_literature_item(self):
        """Method that tests the successful request to the literature item."""

        expected_data = {'id': 10,
                         'title': 'Book One',
                         'description': 'Book for Java',
                         'source': 'www.online.com',
                         'create_at': 1509344112,
                         'update_at': 1509344112,
                         'author': 101,
                         'item': 16}

        url = reverse('item:literature:literature_details', args=[16, 10])
        response = self.client_first.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_not_success_get_literature_item(self):
        """Method that tests the unsuccessful request to the literature item
        Test the incorrect literature id.
        """

        url = reverse('item:literature:literature_details', args=[16, 11])
        response = self.client_first.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_get_literature_list(self):
        """Method that tests the success request to the literature list."""

        expected_data = {'literature_list': [{'id': 10,
                                              'title': 'Book One',
                                              'description': 'Book for Java',
                                              'source': 'www.online.com',
                                              'create_at': 1509344112,
                                              'update_at': 1509344112,
                                              'author': 101,
                                              'item': 16}]}

        url = reverse('item:literature:literature', args=[16])
        response = self.client_first.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_success_get_user_literature_list(self):
        """Method that tests the success request to the user literature list."""

        expected_data = {'user_literature_list': [{'id': 10,
                                                   'title': 'Book One',
                                                   'description': 'Book for Java',
                                                   'source': 'www.online.com',
                                                   'create_at': 1509344112,
                                                   'update_at': 1509344112,
                                                   'author': 101,
                                                   'item': 16}]}

        url = reverse('literature')
        response = self.client_first.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))

    def test_not_success_get_user_literature_list(self):
        """Method that tests the unsuccessful request to the user literature list."""

        url = reverse('literature')
        response = self.client_second.get(url)
        self.assertEqual(response.status_code, 404)

    def test_not_success_post_literature_item(self):
        """Method that tests the unsuccessful request to the add literature item
        with invalid post data."""

        data = {}
        url = reverse('item:literature:literature', args=[16])
        response = self.client_first.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_post_literature_item(self):
        """Method that tests the successful request to the add literature item"""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            data = {
                'title': 'Book',
                'description': 'For feature developers',
                'source': 'www.online.com',
                'author': 101,
                'item': 16
            }
            url = reverse('item:literature:literature', args=[16])
            response = self.client_first.post(url, json.dumps(data), content_type='application/json')
            response_dict = json.loads(response.content.decode('utf-8'))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_dict['title'], 'Book')
            self.assertEqual(response_dict['description'], 'For feature developers')
            self.assertEqual(response_dict['source'], 'www.online.com')
            self.assertEqual(response_dict['author'], 101)
            self.assertEqual(response_dict['item'], 16)

    def test_error_db_creating_post(self):
        """Method that tests unsuccessful post request when db creating is failed."""

        with mock.patch('literature.models.LiteratureItem.create') as literature_create:
            literature_create.return_value = None
            data = {
                'title': 'Book',
                'description': 'For feature developers',
                'source': 'www.online.com',
                'author': 101,
                'item': 16
            }
            url = reverse('item:literature:literature', args=[16])
            response = self.client_first.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_not_success_put_literature_id_invalid(self):
        """Method that tests unsuccessful put request with invalid literature id."""

        data = {
            'title': 'Book',
            'description': 'For feature developers',
            'source': 'www.online.com'
        }
        url = reverse('item:literature:literature_details', args=[16, 120])
        response = self.client_first.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_not_success_put_wrong_author(self):
        """Method that tests unsuccessful put request with wrong author."""

        data = {
            'title': 'Book',
            'description': 'For feature developers',
            'source': 'www.online.com'
        }
        url = reverse('item:literature:literature_details', args=[16, 10])
        response = self.client_second.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_not_success_put_empty_json(self):
        """Method that tests unsuccessful put request with empty json."""

        data = {}
        url = reverse('item:literature:literature_details', args=[16, 10])
        response = self.client_first.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_put(self):
        """Method that tests successful put request."""

        data = {
            'title': 'Article',
            'description': 'New article for JS',
            'source': 'www.bookclub.com',
        }
        url = reverse('item:literature:literature_details', args=[16, 10])
        response = self.client_first.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_not_success_delete_literature_id_invalid(self):
        """Method that tests unsuccessful delete request with invalid literature id."""

        url = reverse('item:literature:literature_details', args=[16, 120])
        response = self.client_first.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_not_success_delete_wrong_author(self):
        """Method that tests unsuccessful delete request with wrong author."""

        url = reverse('item:literature:literature_details', args=[16, 10])
        response = self.client_second.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_success_delete(self):
        """Method that tests successful delete request."""

        url = reverse('item:literature:literature_details', args=[16, 10])
        response = self.client_first.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_error_db_creating_delete(self):
        """Method that tests unsuccessful delete request when db creating is failed."""

        with mock.patch('literature.models.LiteratureItem.delete_by_id') as literature_delete:
            literature_delete.return_value = None

            url = reverse('item:literature:literature_details', args=[16, 10])
            response = self.client_first.delete(url)
            self.assertEqual(response.status_code, 400)
