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


class EventDataValidateTestCase(TestCase):
    """Class that provides test cases for the event data validate function."""

    def test_success_data_validation(self):
        """Test success data validate."""

        valid_data = {'name': 'some name',
                      'owner': 12,
                      'description': '',
                      'start_at': 12345645,
                      'duration': 7200,
                      'longitude': 345.343,
                      'budget': 100,
                      'status': 3}

        self.assertTrue(event_data_validate(valid_data, required_keys=[]))

    def test_error_required_keys(self):
        """Test requires key validation error."""

        invalid_data = {'owner': 12,
                        'description': 'some text',
                        'start_at': 12345645,
                        'duration': 7200,
                        'longitude': 345.343,
                        'latitude': 23.34223,
                        'budget': 100,
                        'status': 3}

        self.assertFalse(event_data_validate(invalid_data, required_keys=['name']))

    def test_error_name_filed(self):
        """Test invalid cases of name field."""

        invalid_empty_name_data = {'name': ''}
        invalid_non_string_name_data = {'name': []}
        invalid_long_name_data = {'name': 'some name'*30}

        self.assertFalse(event_data_validate(invalid_empty_name_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_non_string_name_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_long_name_data, required_keys=[]))

    def test_error_owner_field(self):
        """Test invalid cases of owner field."""

        invalid_non_int_owner_data = {'owner': ''}
        invalid_negative_int_owner_data = {'owner': -2}

        self.assertFalse(event_data_validate(invalid_non_int_owner_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_negative_int_owner_data, required_keys=[]))

    def test_error_description_field(self):
        """Test invalid cases of description field."""

        invalid_non_string_description_data = {'description': {}}

        self.assertFalse(event_data_validate(invalid_non_string_description_data, required_keys=[]))

    def test_error_start_at_field(self):
        """Test invalid cases of start_at field."""

        invalid_non_int_start_at_data = {'start_at': ''}
        invalid_big_int_start_at_data = {'start_at': 156464848646846468846464}

        self.assertFalse(event_data_validate(invalid_non_int_start_at_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_big_int_start_at_data, required_keys=[]))

    def test_error_duration_field(self):
        """Test invalid cases of duration field."""

        invalid_non_int_duration_data = {'duration': 'text'}
        invalid_big_int_duration_data = {'duration': 345345245234523452345234524}

        self.assertFalse(event_data_validate(invalid_non_int_duration_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_big_int_duration_data, required_keys=[]))

    def test_error_longitude_latitude_fields(self):
        """Test invalid cases of longitude and latitude fields."""

        invalid_non_float_longitude_data = {'longitude': 456465, 'latitude': 345.5}

        self.assertFalse(event_data_validate(invalid_non_float_longitude_data, required_keys=[]))

    def test_error_budget_field(self):
        """Test invalid cases of budget field."""

        invalid_non_int_budget_data = {'budget': []}
        invalid_negative_budget_data = {'budget': -322}

        self.assertFalse(event_data_validate(invalid_non_int_budget_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_negative_budget_data, required_keys=[]))

    def test_error_status_field(self):
        """Test invalid cases of status field."""

        invalid_non_int_status_data = {'status': 'txt'}
        invalid_negative_status_data = {'status': -1}
        invalid_big_status_data = {'status': 4}

        self.assertFalse(event_data_validate(invalid_non_int_status_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_negative_status_data, required_keys=[]))
        self.assertFalse(event_data_validate(invalid_big_status_data, required_keys=[]))
