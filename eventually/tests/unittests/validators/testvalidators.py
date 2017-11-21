"""
Validator tests
===============
"""

import datetime
from django.test import TestCase
from utils.validators import *


class ValidatorsTestCase(TestCase):
    """TestCase for validators"""

    def test_list_of_int_validator_list_int(self):
        """Method that tests list_of_int_validator method with list of int enter parameter"""
        my_list = list_of_int_validator([1, 2, 3])
        self.assertTrue(my_list)

    def test_list_of_int_validator_tuple_int(self):
        """Method that tests list_of_int_validator method with tuple of int enter parameter"""
        my_list = list_of_int_validator((1, 2, 3))
        self.assertTrue(my_list)

    def test_list_of_int_validator_int(self):
        """Method that tests list_of_int_validator method with int enter parameter"""
        my_list = list_of_int_validator(1)
        self.assertFalse(my_list)

    def test_list_of_int_validator_str(self):
        """Method that tests list_of_int_validator method with str enter parameter"""
        my_list = list_of_int_validator('a')
        self.assertFalse(my_list)

    def test_list_of_int_validator_list_of_decimal(self):
        """Method that tests list_of_int_validator method with list of decimal enter parameter"""
        my_list = list_of_int_validator([1.25, 2, 3.5])
        self.assertFalse(my_list)

    def test_list_of_int_validator_list_of_str(self):
        """Method that tests list_of_int_validator method with list of str enter parameter"""
        my_list = list_of_int_validator(['a', 'b'])
        self.assertFalse(my_list)

    def test_list_of_int_validator_empty_list(self):
        """Method that tests list_of_int_validator method with empty list enter parameter"""
        my_list = list_of_int_validator([])
        self.assertFalse(my_list)

    def test_string_validator_str(self):
        """Method that tests string_validator method with str enter parameter"""
        my_str = string_validator('a')
        self.assertTrue(my_str)

    def test_string_validator_int(self):
        """Method that tests string_validator method with int enter parameter"""
        my_str = string_validator(1)
        self.assertFalse(my_str)

    def test_string_validator_list(self):
        """Method that tests string_validator method with list enter parameter"""
        my_str = string_validator(['a', 'b'])
        self.assertFalse(my_str)

    def test_string_validator_min_length(self):
        """Method that tests string_validator method with str and min_length enter parameters"""
        my_str = string_validator('a', 1)
        self.assertTrue(my_str)

    def test_string_validator_error_min_length(self):
        """Method that tests string_validator method with str and error min_length enter parameters"""
        my_str = string_validator('a', 3)
        self.assertFalse(my_str)

    def test_string_validator_max_length(self):
        """Method that tests string_validator method with str and max_length enter parameters"""
        my_str = string_validator('word', 1, 5)
        self.assertTrue(my_str)

    def test_string_validator_error_max_length(self):
        """Method that tests string_validator method with str and error max_length enter parameters"""
        my_str = string_validator('word', 1, 3)
        self.assertFalse(my_str)

    def test_password_validator_success(self):
        """Method that tests `password_validator`."""
        password = 'fgh1DFvd2'

        is_valid = password_validator(password)

        self.assertTrue(is_valid)

    def test_password_validator_fail(self):
        """Method that tests `password_validator`."""
        password = 'fghDFvd'

        is_valid = password_validator(password)

        self.assertIsNone(is_valid)

    def test_duration_validator_success(self):
        """Method that tests `duration_validator`."""
        value = 25

        is_valid = duration_validator(value)

        self.assertTrue(is_valid)

    def test_duration_validator_fail_string(self):
        """Method that tests `duration_validator`."""
        value = "some_text"

        is_valid = duration_validator(value)

        self.assertIsNone(is_valid)

    def test_duration_validator_fail_not_positive(self):
        """Method that tests `duration_validator`."""
        value = -25

        is_valid = duration_validator(value)

        self.assertIsNone(is_valid)

    def test_duration_validator_fail_overflow(self):
        """Method that tests `duration_validator`."""
        value = 250000000000000000

        is_valid = duration_validator(value)

        self.assertIsNone(is_valid)

    def test_timestamp_validator_success(self):
        """Method that tests `timestamp_validator`."""
        value = 255

        is_valid = timestamp_validator(value)

        self.assertTrue(is_valid)

    def test_timestamp_validator_fail(self):
        """Method that tests `timestamp_validator`."""
        value = 'some_text'

        is_valid = timestamp_validator(value)

        self.assertIsNone(is_valid)

    def test_required_keys_validator_strict_success(self):
        """Method that tests `required_keys_validator`."""
        data = {"name": "Some_name", "email": "some_email"}
        keys_required = ["name", "email"]

        is_valid = required_keys_validator(data, keys_required)

        self.assertTrue(is_valid)

    def test_required_keys_validator_strict_fail(self):
        """Method that tests `required_keys_validator`."""
        data = {
            "name": "Some_name",
            "email": "some_email",
            "adress": "some_city",
            "status": "some_status"
        }
        keys_required = ["name", "email"]

        is_valid = required_keys_validator(data, keys_required)

        self.assertFalse(is_valid)

    def test_required_keys_validator_not_strict_success(self):
        """Method that tests `required_keys_validator`."""
        data = {"name": "some_name", "email": "some_email", "adress": "some_city"}
        keys_required = ["name", "email"]

        is_valid = required_keys_validator(data, keys_required, strict=False)

        self.assertTrue(is_valid)

    def test_required_keys_validator_not_strict_fail(self):
        """Method that tests `required_keys_validator`."""
        data = {"name": "some_name", "email": "some_email", "adress": "some_city"}
        keys_required = ["name", "hobby"]

        is_valid = required_keys_validator(data, keys_required, strict=False)

        self.assertFalse(is_valid)

    def test_reset_password_validate_success(self):
        """Method that tests `reset_password_validate`."""
        data = {
            "name": "Some_name",
            "email": "some_email",
            "adress": "some_city",
            "status": "some_status"
        }

        requred_key = "name"

        is_valid = reset_password_validate(data, requred_key)

        self.assertTrue(is_valid)

    def test_reset_password_validate_fail(self):
        """Method that tests `reset_password_validate`."""
        data = {
            "name": 123,
            "email": "some_email",
            "adress": "some_city",
            "status": "some_status"
        }

        requred_key = "name"

        is_valid = reset_password_validate(data, requred_key)

        self.assertIsNone(is_valid)

class EmailValidatorsTestCase(TestCase):
    """TestCase for email validator"""

    def test_email_valid(self):
        """Method that tests registration email validation"""

        email = 'john.smith@mail.com'

        is_valid = email_validator(email)

        self.assertTrue(is_valid)

    def test_email_invalid(self):
        """Method that tests registration email validation"""

        email = 'John.Smithmail.com'

        is_valid = email_validator(email)

        self.assertIsNone(is_valid)

class RegistrationValidatorsTestCase(TestCase):
    """TestCase for registration validator"""

    def test_registration_valid(self):
        """Method that tests registration validation"""

        data = {'email': 'somemail@mail.com',
                'password': 'mypaDssw1223'}

        is_valid = registration_validate(data)

        self.assertTrue(is_valid)

    def test_registration_invalid_required_keys(self):
        """Method that tests registration required keys validation"""

        data = {'email': 'somemail@mail.com'}
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, "not password")

        data = {'password': 'mypaDssw1223',
                'email': 111}
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, "email is not string")

        data = {'password': 'mypaDssw1223'}
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, "not email")

        data = {'email': 'somemail@mail.com',
                'password': 111}
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, 'password is not string')

        data = {}
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, 'empty data')


    def test_registration_invalid_not_string(self):
        """Method that tests registration string validation"""

        data = {'first_name': 124,
                'password': 'mypaDssw1223',
                'email': 'somemail@mail.com'
                }
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, "not password")

        data = {'last_name': 2451,
                'password': 'mypaDssw1223',
                'email': 'alkdasdj@mail.com'}
        is_valid = registration_validate(data)
        self.assertFalse(is_valid, "email is not string")
