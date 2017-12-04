"""
Forget Password test module
===========================
"""

import json
from unittest import mock
from django.test import TestCase, Client
from django.urls import reverse
from authentication.views import CustomUser

URL_WITHOUT_TOKEN = reverse('forget_password')
URL_WITH_TOKEN = reverse('forget_password_token', args={"token":''})

class TestForgetPassword(TestCase):
    """ Class for Forget Password tests """

    def setUp(self):
        """ Set up test browser client """
        self.client = Client()

        user = CustomUser.objects.create(id=100, email="john@email.com")
        user.set_password = "QwErTy12234"
        user.save()

    def test_post_positive(self):
        """ Positive test for forget password POST function """

        email_exist = json.dumps({"email": "john@email.com"})
        expect_200 = self.client.post(URL_WITHOUT_TOKEN,
                                      email_exist, content_type='application/json')
        self.assertEqual(expect_200.status_code, 200)


    def test_post_bademail(self):
        """ Negative test for forget password POST function """

        email_not_exist = json.dumps({"email": "doesnotexist@gmail.com"})
        expect_400 = self.client.post(URL_WITHOUT_TOKEN,
                                      email_not_exist, content_type='application/json')
        self.assertEqual(expect_400.status_code, 400)


    def test_post_noemail(self):
        """ Negative test for forget password POST function """

        expect_400 = self.client.post(URL_WITHOUT_TOKEN, {}, content_type='application/json')
        self.assertEqual(expect_400.status_code, 400)


    def test_put_positive(self):
        """ Positive test for forget password PUT function """

        with mock.patch('authentication.views.handle_token') as handle_token:
            handle_token.return_value = {"user_id":100, 'email': 'john@email.com'}
            new_password_valid = json.dumps({"new_password": "QwErTy1234"})
            expect_200 = self.client.put(URL_WITH_TOKEN,
                                         new_password_valid, content_type='application/json')
            self.assertEqual(expect_200.status_code, 200)


    def test_put_badidentifier(self):
        """ Test PUT function with bad identifier """

        new_password_valid = json.dumps({"new_password": "QwErTy1234"})
        expect_400 = self.client.put(URL_WITH_TOKEN,
                                     new_password_valid, content_type='application/json')
        self.assertEqual(expect_400.status_code, 400)


    def test_put_baduser(self):
        """ Test PUT function with no user specified"""

        new_password_valid = json.dumps({"new_password": "QwErTy1234"})
        expect_400 = self.client.put(URL_WITH_TOKEN,
                                     new_password_valid, content_type='application/json')
        self.assertEqual(expect_400.status_code, 400)


    def test_put_nouser(self):
        """ Test PUT method with inexisting user"""

        with mock.patch('authentication.views.handle_token') as handle_token:
            handle_token.return_value = {"user_id": 100500, 'email': 'john@email.com'}
            new_password_valid = json.dumps({"new_password": "QwErTy1234"})
            expect_400 = self.client.put(URL_WITH_TOKEN,
                                         new_password_valid, content_type='application/json')
            self.assertEqual(expect_400.status_code, 400)


    def test_put_badpassword(self):
        """ Test PUT function with invalid password"""

        with mock.patch('authentication.views.handle_token') as handle_token:
            handle_token.return_value = {"user_id": 100, 'email': 'john@email.com'}
            new_password_invalid = json.dumps({"password": "1"})
            expect_400 = self.client.put(URL_WITH_TOKEN,
                                         new_password_invalid, content_type='application/json')
            self.assertEqual(expect_400.status_code, 400)


    def test_put_notoken(self):
        """ Test PUT method with invalid token """

        expect_498 = self.client.put(URL_WITHOUT_TOKEN, {}, content_type='application/json')
        self.assertEqual(expect_498.status_code, 498)
