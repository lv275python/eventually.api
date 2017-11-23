"""
Authentication view tests
================

This module provides complete testing for all Authentication's views functions.
"""

from json import dumps
from unittest import mock

from authentication.models import CustomUser
from django.test import TestCase
from django.core.urlresolvers import reverse


class AuthenticationViewTest(TestCase):
    """TestCase for providing Authentication view testing."""

    def setUp(self):
        """Create CustomUser record in database."""

        not_active_user = CustomUser.objects.create(id=12, email='someemail@gmail.com')
        not_active_user.set_password('password')
        not_active_user.save()

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
