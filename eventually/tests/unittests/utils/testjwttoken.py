"""
JWT Token Test
==============

This module provides complete testing for jwt token util.
"""

import datetime
import jwt
import time
from django.test import TestCase
from django.utils import timezone
from utils import jwttoken
from unittest import mock

TEST_TIME = datetime.datetime(2017, 8, 7, 8, 11, 12)


class JWTTokenTestCase(TestCase):
    """TestCase for providing jwttoken util testing."""

    def setUp(self):
        """Method that set ups basic constants before testing jwttoken's features."""

        jwttoken.SECRET_KEY = 'test'
        jwttoken.ALGORITHM = 'HS384'

    def test_success_jwt_token(self):
        """Method that tests succeeded `create_token` method."""

        data = {'test': 1, 2: 'some text'}
        expected_token = jwt.encode(data, jwttoken.SECRET_KEY, jwttoken.ALGORITHM)
        actual_token = jwttoken.create_token(data)
        self.assertEquals(actual_token, expected_token)

    def test_error_jwt_token(self):
        """Method that tests unsucceeded `create_token` method."""

        data = [1, 3]
        actual_token = jwttoken.create_token(data)

        self.assertIsNone(actual_token)

    def test_success_expiration_time_jwt_token(self):
        """Method that tests succeeded `create_token` method with expiration time parameter."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            data = {'test': 1, '2': 'some text'}
            expected_token = (
                b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.'
                b'eyJ0ZXN0IjoxLCIyIjoic29tZSB0ZXh0IiwiZXhwIjoxNTAyMDgyNzMyfQ.'
                b'GLACBjEm6XZ7eKbyF9ATtEw-ttLinjhM2IoCoc4rbUfhtgvVsfbk15fQGVtAf7cq'
            )
            actual_token = jwttoken.create_token(data, expiration_time=60)

            self.assertEquals(actual_token, expected_token)

    def test_success_not_before_time_jwt_token(self):
        """Method that tests succeeded `create_token` method with not before time parameter."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            data = {'test': 1, '2': 'some text'}
            expected_token = (
                b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.'
                b'eyJ0ZXN0IjoxLCIyIjoic29tZSB0ZXh0IiwibmJmIjoxNTAyMDgyNzMyfQ.'
                b'QuYDCDhXrLauJ8veSzhsknpeQGgyJQ3Z6VBsK35vYCMmG-02vKb9DlbrfyeiOWHa'
            )

            actual_token = jwttoken.create_token(data, not_before_time=60)
            self.assertEquals(actual_token, expected_token)

    def test_success_handle_token(self):
        """Method that tests succeeded `handle_token` method."""

        data = {1: 'some text', 'some filed': 2}
        token = jwt.encode(data, jwttoken.SECRET_KEY, jwttoken.ALGORITHM)
        expected_dict = {'1': 'some text', 'some filed': 2}
        actual_dict = jwttoken.handle_token(token)

        self.assertDictEqual(actual_dict, expected_dict)

    def test_error_handle_token(self):
        """Method that tests unsucceeded `handle_token` method."""

        data = {1: 'some text', 'some filed': 2, 'exp': int(timezone.now().timestamp()) + 1}
        token = jwt.encode(data, jwttoken.SECRET_KEY, jwttoken.ALGORITHM)
        time.sleep(2)
        handled_result = jwttoken.handle_token(token)

        self.assertIsNone(handled_result)
