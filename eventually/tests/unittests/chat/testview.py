"""
Chat Views Test.
==================

This module provides complete testing for all Chat's views functions.
"""
import datetime
import json
from unittest import mock
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone
from authentication.models import CustomUser
from comment.models import Comment
from utils.redishelper import REDIS_HELPER

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12, 0, tzinfo=timezone.utc)


class ChatViewTest(TestCase):
    """TestCase for providing Comment view testing."""

    def setUp(self):
        """Method that provides preparation before testing Event view's features."""


        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user = CustomUser.objects.create(id=100, email='email@gmail.com', is_active=True)
            custom_user.set_password('Aa123456')
            custom_user.save()

            receiver = CustomUser.objects.create(id=1500, email='receiver@gmail.com', is_active=True)
            receiver.set_password('123456')
            receiver.save()

            second_custom_user = CustomUser.objects.create(id=200, email='qwerty@gmail.com', is_active=True)
            second_custom_user.set_password('Aaqwerty11')
            second_custom_user.save()

            Comment.objects.create(id=100, author=custom_user,
                                   text='football', receiver=receiver)
            Comment.objects.create(id=200, author=custom_user,
                                   text='some_sport', receiver=receiver)
            Comment.objects.create(id=300, author=second_custom_user,
                                   text='any_sport', receiver=receiver)
            Comment.objects.create(id=400, author=second_custom_user,
                                   text='sport', receiver=receiver)
        self.client = Client()
        self.client.login(username='email@gmail.com', password='Aa123456')

    def test_get_success(self):
        """
            Method that tests the successful get request for the page with chat messages that belong
            to the certain conversation.
            """
        data = {"messages": [{"id": 100,
                              "text": 'football',
                              "created_at": int(TEST_TIME.timestamp()),
                              "updated_at": int(TEST_TIME.timestamp()),
                              "team": None,
                              "event": None,
                              "task": None,
                              "vote": None,
                              "author": {'id': 100,
                                         'first_name': '',
                                         'middle_name': '',
                                         'last_name': '',
                                         'email': 'email@gmail.com',
                                         'created_at': int(TEST_TIME.timestamp()),
                                         'updated_at': int(TEST_TIME.timestamp()),
                                         'is_active': True},
                              "receiver": 1500},
                             {"id": 200,
                              "text": 'some_sport',
                              "created_at": int(TEST_TIME.timestamp()),
                              "updated_at": int(TEST_TIME.timestamp()),
                              "team": None,
                              "event": None,
                              "task": None,
                              "vote": None,
                              "author": {'id': 100,
                                         'first_name': '',
                                         'middle_name': '',
                                         'last_name': '',
                                         'email': 'email@gmail.com',
                                         'created_at': int(TEST_TIME.timestamp()),
                                         'updated_at': int(TEST_TIME.timestamp()),
                                         'is_active': True},
                              "receiver": 1500}],
                "next_page": -1,
                "per_page": 20}
        url = reverse('pages', args=[1500, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data))

    def test_get_failed_wrong_id(self):
        """
        Method that tests the unsuccessful get request for creating a page with chat messages.
        Wrong receiver id in url.
        """
        url = reverse('pages', args=[1501, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_failed_author_is_interlocutor(self):
        """
        Method that tests the unsuccessful get request for creating a page with chat messages.
        Author is interlocutor.
        """
        url = reverse('pages', args=[1500, 1])
        client = Client()
        client.login(username='receiver@gmail.com', password='123456')
        response = client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_get_failed_invalid_page_number(self):
        """
        Method that tests the unsuccessful get request for creating of page with chat messages.
        Wrong page number in url.
        """
        url = reverse('pages', args=[1500, 2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        """
        Method that tests the successful post request for creating of chat message.
        """
        data = {"text": 'some_text'}
        url = reverse('chat', args=[1500])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_failed_empty_json(self):
        """
        Method that tests the unsuccessful post request for creating of chat message.
        Empty json.
        """
        data = {}
        url = reverse('chat', args=[1500])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_fail_wrong_id(self):
        """
        Method that tests the unsuccessful post request for creating of chat message.
        Wrong receiver id in url.
        """
        data = {"text": 'some_text'}
        url = reverse('chat', args=[1501])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_post_fail_not_valid_message(self):
        """
        Method that tests the unsuccessful post request for chat message.
        Not valid message.
        """
        data = {"text": 0}
        url = reverse('chat', args=[1500])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_failed_author_is_receiver(self):
        """
        Method that tests the unsuccessful post request for chat message.
        Author is receiver.
        """
        data = {"text": 'some_text'}
        url = reverse('chat', args=[1500])
        client = Client()
        client.login(username='receiver@gmail.com', password='123456')
        response = client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_failed_not_message(self):
        """
        Method that tests the successful post request for creating of chat message.
        """
        with mock.patch('comment.models.Comment.create') as comment_create:
            comment_create.return_value = None

            data = {"text": 'some text'}
            url = reverse('chat', args=[1500])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)


class OnlineStatusViewTest(TestCase):
    def setUp(self):
        """Method that provides preparation before testing OnlineStatus view's features."""
        custom_user = CustomUser.objects.create(id=100, email='email@gmail.com', is_active=True)
        custom_user.set_password('Aa123456')
        custom_user.save()

        second_custom_user = CustomUser.objects.create(id=200, email='qwerty@gmail.com', is_active=True)
        second_custom_user.set_password('Aaqwerty11')
        second_custom_user.save()

        third_custom_user = CustomUser.objects.create(id=300, email='third@gmail.com', is_active=True)
        third_custom_user.set_password('Aauser11')
        third_custom_user.save()

        self.client = Client()
        self.client.login(username='email@gmail.com', password='Aa123456')

    def test_post_online_status(self):
        """
        Method that tests the successful online_status request.
        """
        data = {'users': [100, 200, 300]}
        users = CustomUser.objects.all()
        for user in users:  # set user id in redis db
            REDIS_HELPER.set(user.id, user.email)
        data_users_online = {str(user.id): user.email for user in users}
        url = reverse('online_status')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data_users_online))

