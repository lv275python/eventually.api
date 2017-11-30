"""
Authentication view tests
================

This module provides complete testing for all Authentication's views functions.
"""

import datetime
import json
import pytz
from json import dumps
from unittest import mock
from django.http import JsonResponse
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from authentication.models import CustomUser
from customprofile.models import CustomProfile


class AuthenticationViewTest(TestCase):
    """TestCase for providing Authentication view testing."""

    def setUp(self):
        """Create CustomUser record in database."""

        not_active_user = CustomUser.objects.create(id=12, email='someemail@gmail.com')
        not_active_user.set_password('password')
        not_active_user.save()

        self.client = Client()

        time_mock = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = time_mock

            user = CustomUser.objects.create(id=100,
                                             first_name="Robert",
                                             last_name="Downey",
                                             middle_name="Jr.",
                                             email='mail@mail.co',
                                             is_active=True)
            user.set_password('1234')
            user.save()

            user_for_deletion = CustomUser.objects.create(id=1,
                                                          email='delete@mail.co',
                                                          is_active=True)
            user_for_deletion.set_password('123456')
            user_for_deletion.save()


    def test_register_success(self):
        """Test register view success."""

        request = self.client.post(reverse('register'),
                                   dumps({"email": "some@gmail.com", "password": "p1Riod"}),
                                   content_type='application/json')
        self.assertEqual(request.status_code, 201)

    def test_register_no_data(self):
        """Test register view without request data."""

        request = self.client.post(reverse('register'), dumps({}),
                                   content_type='application/json')
        self.assertEqual(request.status_code, 400)

    def test_register_data_is_invalid(self):
        """Test register view when data is not valid."""

        request = self.client.post(reverse('register'),
                                   dumps({"password": "Rd"}),
                                   content_type='application/json')
        self.assertEqual(request.status_code, 400)

    def test_register_email_exist(self):
        """Test register view when email is already exist."""

        request = self.client.post(reverse('register'),
                                   dumps({"email": "someemail@gmail.com", "password": "p1Rd"}),
                                   content_type='application/json')
        self.assertEqual(request.status_code, 400)

    def test_reg_bad_request(self):
        """Test register bad request method."""

        request = self.client.put(reverse('register'),
                                  dumps({"email": "someemail@gmail.com", "password": "p1Rd"}),
                                  content_type='application/json')
        self.assertEqual(request.status_code, 400)

    def test_activation_success(self):
        """Test success activation via email."""

        with mock.patch('authentication.views.handle_token') as handle_token:
            handle_token.return_value = {'email': 'someemail@gmail.com'}
            url = reverse('activate', args=["gndhntgid"])
            request = self.client.get(url)
            self.assertEqual(request.status_code, 200)

    def test_activation_create_profile_success(self):
        """Test success activation via email with empty profile creating."""

        with mock.patch('authentication.views.handle_token') as handle_token:
            handle_token.return_value = {'email': 'someemail@gmail.com'}
            url = reverse('activate', args=["gndhntgid"])
            request = self.client.get(url)
            actual_profile = CustomProfile.objects.get(user_id=12).to_dict()
            self.assertEqual(actual_profile['user'], 12)
            self.assertEqual(actual_profile['hobby'], '')
            self.assertEqual(actual_profile['photo'], '')
            self.assertIsNone(actual_profile['birthday'])
            self.assertEqual(request.status_code, 200)

    def test_activation_email_not_exist(self):
        """ Test activation via when user not founded in DB by email."""

        with mock.patch('authentication.views.handle_token') as handle_token:
            handle_token.return_value = {'email': 'someemail400@gmail.com'}
            url = reverse('activate', args=["gndhntgid"])
            request = self.client.get(url)
            self.assertEqual(request.status_code, 400)

    def test_activation_bad_token(self):
        """ Test activation via email when token expired/invalid."""

        url = reverse('activate', args=['LAKSJDk'])
        request = self.client.get(url)
        self.assertEqual(request.status_code, 498)

    def test_activation_bad_request(self):
        """Test activation via email with wrong request method."""

        url = reverse(('activate'), args=['someargs'])
        request = self.client.put(url, dumps({"email": "someemail@gmail.com", "password": "p1Rd"}),
                                  content_type='application/json')
        self.assertEqual(request.status_code, 404)


    def test_get(self):
        """ Positive test for retrieving objects from the database """

        user = json.dumps({'email':'mail@mail.co', 'password':'1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user_json_toexpect = {'id': 100,
                              'first_name': 'Robert',
                              'middle_name': 'Jr.',
                              'last_name': 'Downey',
                              'email': 'mail@mail.co',
                              'created_at': 1491825600,
                              'updated_at': 1491825600,
                              'is_active': True}

        received_user_json = self.client.get('/api/v1/user/100/')
        self.assertIsInstance(received_user_json, JsonResponse)

        received_user_json = json.loads(received_user_json.content)
        self.assertDictEqual(user_json_toexpect, received_user_json)


    def test_get_negative(self):
        """ Negative test for retrieving objects from the database """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user_get_response = self.client.get('/api/v1/user/100500/')
        self.assertEqual(user_get_response.status_code, 404)


    def test_put(self):
        """ Positive test for method to change objects in the database """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user = json.dumps({"first_name": "Jerry"})
        user_change_response = self.client.put('/api/v1/user/100/', user)
        self.assertEqual(user_change_response.status_code, 200)

        user_object = CustomUser.objects.get(id=100)
        user_changed_name = user_object.first_name
        self.assertEqual(user_changed_name, "Jerry")


    def test_put_password(self):
        """ Positive test on password change """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user_password = json.dumps({"password": "1Aa"})
        password_change_response = self.client.put('/api/v1/user/100/', user_password)
        self.assertEqual(password_change_response.status_code, 200)


    def test_put_negative_password(self):
        """ Negative test on change password """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user_password = json.dumps({"password": "1a"})
        password_change_response = self.client.put('/api/v1/user/100/', user_password)
        self.assertEqual(password_change_response.status_code, 400)


    def test_put_negative(self):
        """ User change negative test """

        user = json.dumps({'email':'mail@mail.co', 'password':'1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user = json.dumps({"first_name": "Jerry"})
        user_change_response = self.client.put('/api/v1/user/100500/', user)
        self.assertEqual(user_change_response.status_code, 404)


    def test_delete(self):
        """ Delete user positive test """

        user = json.dumps({'email':'mail@mail.co', 'password':'1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        delete_user_response = self.client.delete('/api/v1/user/100/')
        self.assertEqual(delete_user_response.status_code, 200)


    def test_deleteuserexist_negative(self):
        """ User delete negative test """

        user = json.dumps({'email':'mail@mail.co', 'password':'1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        delete_user_reponse = self.client.delete('/api/v1/user/1/')
        self.assertEqual(delete_user_reponse.status_code, 403)

        delete_user_reponse = self.client.delete('/api/v1/user/100500/')
        self.assertEqual(delete_user_reponse.status_code, 404)

    def test_deleteuserinexist_negative(self):
        """ User delete negative test """

        user = json.dumps({'email':'mail@mail.co', 'password':'1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        delete_user_reponse = self.client.delete('/api/v1/user/100500/')
        self.assertEqual(delete_user_reponse.status_code, 404)


    def test_login(self):
        """ Positive user login test """

        user = json.dumps({'email':'mail@mail.co', 'password':'1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_login_negative(self):
        """ Negative user login test """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        response = self.client.put(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        user = json.dumps({'email': 'mail'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_logout(self):
        """ Positive user logout test """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        response = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        resp_logout = self.client.get((reverse('logout_user')))
        self.assertEqual(resp_logout.status_code, 200)


    def test_logout_negative(self):
        """ Negative user logout test """

        user = json.dumps({'email': 'mail@mail.co', 'password': '1234'})
        resp_login = self.client.post(reverse('login_user'), user, content_type='application/json')
        self.assertEqual(resp_login.status_code, 200)

        resp_logout = self.client.patch((reverse('logout_user')))
        self.assertEqual(resp_logout.status_code, 400)
