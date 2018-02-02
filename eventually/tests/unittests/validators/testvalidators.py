"""
Validator tests
===============
"""

import datetime
from django.test import TestCase
from utils.validators import *
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from unittest import mock
from django.http import HttpResponse

IMAGE_NAME = "testimage.png"
IMAGE_MIME_TYPE = "image/png"
GOOD_IMAGE_SIZE = 3 * 1024 * 1024
BAD_IMAGE_SIZE = 9 * 1024 * 1024
IMAGE_FORMAT = "png"

class ValidatorsTestCase(TestCase):
    """TestCase for validators"""

    def setUp(self):
        file = BytesIO()
        pil_image = Image.new('RGBA', size=(5000, 5000), color=(155, 0, 0))
        pil_image.save(file, format=IMAGE_FORMAT)
        file.seek(0)

        self.image_good = InMemoryUploadedFile(file, None, IMAGE_NAME, IMAGE_MIME_TYPE,
                                               GOOD_IMAGE_SIZE, None)
        self.image_badsize = InMemoryUploadedFile(file, None, IMAGE_NAME, IMAGE_MIME_TYPE,
                                                  BAD_IMAGE_SIZE, None)

        bad_file = BytesIO()
        pil_image = Image.new('RGBA', size=(5000, 5000), color=(155, 0, 0))
        pil_image.save(bad_file, format="tiff")
        bad_file.seek(0)
        self.image_badcontent = InMemoryUploadedFile(bad_file, None, 'testimage.vfc', 'image/vfc',
                                                     3 * 1024 * 1024, None)

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

    def test_password_validator_type_error_fail(self):
        """
        Method that tests `password_validator`,
        when `password` parameter has wrong type (not string).
        """
        password = 12

        is_valid = password_validator(password)

        self.assertIsNone(is_valid)

    def test_login_validate_success(self):
        """
        Method that tests `login_validate`.
        """
        data = {"email": "example@gmail.com",
                "password": "some_password"}

        is_valid = login_validate(data)

        self.assertTrue(is_valid)

    def test_login_validate_fail_empty_data(self):
        """
        Method that tests `login_validate`,
        when `data` is empty dict.
        """
        data = {}

        is_valid = login_validate(data)

        self.assertFalse(is_valid)

    def test_login_validate_fail_data_without_email(self):
        """
        Method that tests `login_validate`,
        when `data` does not contain `email` key.
        """
        data = {"password": "some_password"}

        is_valid = login_validate(data)

        self.assertFalse(is_valid)

    def test_login_validate_fail_invalid_email(self):
        """
        Method that tests `login_validate`,
        when `data['email']` does not contain `@` symbol.
        """
        data = {"email": "example_gmail.com",
                "password": "some_password"}

        is_valid = login_validate(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_create_success(self):
        """
        Method that tests `task_data_validate_create`.
        """
        data = {"title": "some_title",
                "description": "some_description",
                "status": 2,
                "users": [1, 2, 3]}

        is_valid = task_data_validate_create(data)

        self.assertTrue(is_valid)

    def test_task_data_validate_create_fail_data_without_all_required_keys(self):
        """
        Method that tests `task_data_validate_create`,
        when `data` does not contain all `required_keys`.
        """
        data = {"title": "some_title",
                "description": "some_description"}

        is_valid = task_data_validate_create(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_create_fail_title_invalid_type(self):
        """
        Method that tests `task_data_validate_create`,
        when `data['title']` is not a string.
        """
        data = {"title": 222,
                "description": "some_description",
                "status": "some_status"}

        is_valid = task_data_validate_create(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_create_fail_description_invalid_type(self):
        """
        Method that tests `task_data_validate_create`,
        when `data['description']` is not a string.
        """
        data = {"title": "some_title",
                "description": 222,
                "status": "some_status"}

        is_valid = task_data_validate_create(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_create_fail_users_invalid_type(self):
        """
        Method that tests `task_data_validate_create`,
        when `data['users']` is neither list nor tuple.
        """
        data = {"title": "some_title",
                "description": "some_description",
                "status": "some_status",
                "users": 222}

        is_valid = task_data_validate_create(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_create_fail_status_outside_range(self):
        """
        Method that tests `task_data_validate_create`,
        when `data['status']` is outside the `status_range` (0, 1, 2).
        """
        data = {"title": "some_title",
                "description": "some_description",
                "status": 10}

        is_valid = task_data_validate_create(data)

        self.assertFalse(is_valid)

    def test_paginator_page_validator_success_valid_int(self):
        """
        Method that tests `paginator_page_validator`,
        when type of `page_number` is int.
        """
        page_number = 2
        pages_amount = 3

        is_valid = paginator_page_validator(page_number, pages_amount)

        self.assertTrue(is_valid)

    def test_paginator_page_validator_success_valid_str(self):
        """
        Method that tests `paginator_page_validator`,
        when type of `page_number` is str, which consist of digits.
        """
        page_number = '2'
        pages_amount = 3

        is_valid = paginator_page_validator(page_number, pages_amount)

        self.assertTrue(is_valid)

    def test_paginator_page_validator_fail(self):
        """
        Method that tests `paginator_page_validator`,
        when `page_number` is outside the `pages_amount`.
        """
        page_number = 10
        pages_amount = 3

        is_valid = paginator_page_validator(page_number, pages_amount)

        self.assertFalse(is_valid)

    def test_chat_message_validator_success(self):
        """
        Method that tests `chat_message_validator`.
        """
        data = {"text": "some_text"}
        required_keys = ["text"]

        is_valid = chat_message_validator(data, required_keys)

        self.assertTrue(is_valid)

    def test_chat_message_validator_fail_data_without_all_required_keys(self):
        """
        Method that tests `chat_message_validator`,
        when `data` does not contain all `required_keys`.
        """
        data = {}
        required_keys = ["text"]

        is_valid = chat_message_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_chat_message_validator_fail_text_invalid_type(self):
        """
        Method that tests `chat_message_validator`,
        when `data['text']` is not a string.
        """
        data = {"text": 222}
        required_keys = ["text"]

        is_valid = chat_message_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_chat_message_validator_fail_text_invalid_length(self):
        """
        Method that tests `chat_message_validator`,
        when `data['text']` has length less than `min_length` (1).
        """
        data = {"text": ""}
        required_keys = ["text"]

        is_valid = chat_message_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_success(self):
        """
        Method that tests `comment_data_validator`.
        """
        data = {'text': "some_text",
                'team': 1,
                'event': 2,
                'vote': 3,
                'task': 4,
                'author': 5}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertTrue(is_valid)

    def test_comment_data_validator_fail_data_without_all_required_keys(self):
        """
        Method that tests `comment_data_validator`,
        when `data` does not contain all `required_keys`.
        """
        data = {"name": "Some_name",
                "team": "some_team",
                "text": "some_text"}
        required_keys = ["name", "team", "some_key", "text"]

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_fail_text_invalid_type(self):
        """
        Method that tests `comment_data_validator`,
        when `data['text']` is not a string.
        """
        data = {'text': 222,
                'team': 1,
                'event': 2,
                'vote': 3,
                'task': 4,
                'author': 5}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_fail_team_invalid_type(self):
        """
        Method that tests `comment_data_validator`,
        when `data['team']` is not an int.
        """
        data = {'text': "some_text",
                'team': "abc",
                'event': 2,
                'vote': 3,
                'task': 4,
                'author': 5}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_fail_event_invalid_type(self):
        """
        Method that tests `comment_data_validator`,
        when `data['event']` is not an int.
        """
        data = {'text': "some_text",
                'team': 2,
                'event': "abc",
                'vote': 3,
                'task': 4,
                'author': 5}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_fail_vote_invalid_type(self):
        """
        Method that tests `comment_data_validator`,
        when `data['vote']` is not an int.
        """
        data = {'text': "some_text",
                'team': 2,
                'event': 3,
                'vote': "abc",
                'task': 4,
                'author': 5}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_fail_task_invalid_type(self):
        """
        Method that tests `comment_data_validator`,
        when `data['task']` is not an int.
        """
        data = {'text': "some_text",
                'team': 2,
                'event': 3,
                'vote': 4,
                'task': "abc",
                'author': 5}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_comment_data_validator_fail_author_invalid_type(self):
        """
        Method that tests `comment_data_validator`,
        when `data['author']` is not an int.
        """
        data = {'text': "some_text",
                'team': 2,
                'event': 3,
                'vote': 4,
                'task': 5,
                'author': "abc"}
        required_keys = ['text', 'team', 'event', 'vote', 'task', 'author']

        is_valid = comment_data_validator(data, required_keys)

        self.assertFalse(is_valid)

    def test_task_data_validate_update_success(self):
        """
        Method that tests `task_data_validate_update`.
        """
        data = {'title': "some_title",
                'description': "some_description",
                'status': 1,
                'add_users': [1, 2, 3],
                'remove_users': [4, 5, 6]}

        is_valid = task_data_validate_update(data)

        self.assertTrue(is_valid)

    def test_task_data_validate_update_fail_title_invalid_type(self):
        """
        Method that tests `task_data_validate_update`,
        when `data['title']` is not a string.
        """
        data = {'title': 222,
                'description': "some_description",
                'status': 1,
                'add_users': [1, 2, 3],
                'remove_users': [4, 5, 6]}

        is_valid = task_data_validate_update(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_update_fail_description_invalid_type(self):
        """
        Method that tests `task_data_validate_update`,
        when `data['description']` is not a string.
        """
        data = {'title': "some_title",
                'description': 222,
                'status': 1,
                'add_users': [1, 2, 3],
                'remove_users': [4, 5, 6]}

        is_valid = task_data_validate_update(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_update_fail_status_invalid_type(self):
        """
        Method that tests `task_data_validate_update`,
        when `data['status']` is not an int.
        """
        data = {'title': "some_title",
                'description': "some_description",
                'status': "some_status",
                'add_users': [1, 2, 3],
                'remove_users': [4, 5, 6]}

        is_valid = task_data_validate_update(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_update_fail_add_users_invalid_type(self):
        """
        Method that tests `task_data_validate_update`,
        when `data['add_users']` is neither list nor tuple.
        """
        data = {'title': "some_title",
                'description': "some_description",
                'status': 1,
                'add_users': "[1, 2, 3]",
                'remove_users': [4, 5, 6]}

        is_valid = task_data_validate_update(data)

        self.assertFalse(is_valid)

    def test_task_data_validate_update_fail_remove_users_invalid_type(self):
        """
        Method that tests `task_data_validate_update`,
        when `data['remove_users']` is neither list nor tuple.
        """
        data = {'title': "some_title",
                'description': "some_description",
                'status': 1,
                'add_users': [1, 2, 3],
                'remove_users': "[4, 5, 6]"}

        is_valid = task_data_validate_update(data)

        self.assertFalse(is_valid)

    def test_profile_data_validator_success(self):
        """
        Method that tests `profile_data_validator`.
        """
        data = {"hobby": "swimming",
                "birthday": "180110",
                "photo": "png"}

        is_valid = profile_data_validator(data)

        self.assertTrue(is_valid)

    def test_profile_data_validator_fail_hobby_invalid_type(self):
        """
        Method that tests `profile_data_validator`,
        when `data['hobby']` is not a string.
        """
        data = {"hobby": 222}

        is_valid = profile_data_validator(data)

        self.assertIsNone(is_valid)

    def test_profile_data_validator_fail_birthday_invalid_type(self):
        """
        Method that tests `profile_data_validator`,
        when `data['birthday']` is not a string.
        """
        data = {"birthday": 222}

        is_valid = profile_data_validator(data)

        self.assertIsNone(is_valid)

    def test_profile_data_validator_fail_photo_invalid_type(self):
        """
        Method that tests `profile_data_validator`,
        when `data['photo']` is not a string.
        """
        data = {"photo": 222}

        is_valid = profile_data_validator(data)

        self.assertIsNone(is_valid)

    def test_valid_date_type_success_valid_format_Ymd(self):
        """
        Method that tests `valid_date_type`,
        when `date` format matches '%Y%m%d'.
        """
        date = "20180110"

        is_valid = valid_date_type(date)

        self.assertTrue(is_valid)

    def test_valid_date_type_success_valid_format_Y_m_d(self):
        """
        Method that tests `valid_date_type`,
        when `date` format matches '%Y-%m-%d'.
        """
        date = "2018-01-10"

        is_valid = valid_date_type(date)

        self.assertTrue(is_valid, True)

    def test_valid_date_type_success_valid_format_dmY(self):
        """
        Method that tests `valid_date_type`,
        when `date` format matches '%d%m%Y'.
        """
        date = "10012018"

        is_valid = valid_date_type(date)

        self.assertTrue(is_valid, True)

    def test_valid_date_type_success_valid_format_mdY(self):
        """
        Method that tests `valid_date_type`,
        when `date` format matches '%m%d%Y'.
        """
        date = "01102018"

        is_valid = valid_date_type(date)

        self.assertTrue(is_valid, True)

    def test_valid_date_type_fail_date_invalid_type(self):
        """
        Method that tests `valid_date_type`,
        when `date` is not a string.
        """
        date = 222

        is_valid = valid_date_type(date)

        self.assertFalse(is_valid)

    def test_valid_date_type_fail_invalid_format(self):
        """
        Method that tests `valid_date_type`,
        when `date` has invalid format
        (valid formats: '%Y%m%d', '%Y-%m-%d', '%d%m%Y', '%m%d%Y').
        """
        date = "abcdef"

        is_valid = valid_date_type(date)

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
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "status": "some_status"}
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

    def test_updating_email_validate_success(self):
        """Method that tests `reset_password_validate`."""
        data = {"name": "Some_name",
                "email": "example@gmail.com",
                "adress": "some_city",
                "status": "some_status"}

        requred_key = "email"

        is_valid = updating_email_validate(data, requred_key)

        self.assertTrue(is_valid)

    def test_updating_email_validate_fail(self):
        """Method that tests `reset_password_validate`."""
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "status": "some_status"}

        requred_key = "email"

        is_valid = updating_email_validate(data, requred_key)

        self.assertIsNone(is_valid)

    def test_updating_email_validate_required_keys(self):
        """
        Method that tests `updating_email_validate`,
        when `data` does not contain key as value of parameter `email`.
        """
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "password": "some_password"}
        email = "ffffff"

        is_valid = updating_email_validate(data, email)

        self.assertIsNone(is_valid)

    def test_updating_email_validate_string_validator_email_invalid_type(self):
        """
        Method that tests `updating_email_validate`,
        when value of `data['email']` is not a string.
        """
        data = {"name": "Some_name",
                "email": 123,
                "adress": "some_city",
                "password": "some_password"}
        email = "email"

        is_valid = updating_email_validate(data, email)

        self.assertIsNone(is_valid)

    def test_updating_email_validate_string_validator_email_invalid_length(self):
        """
        Method that tests `updating_email_validate`,
        when value of `data['email']` has length less than `min_length` (4).
        """
        data = {"name": "Some_name",
                "email": "s",
                "adress": "some_city",
                "password": "some_password"}
        email = "email"

        is_valid = updating_email_validate(data, email)

        self.assertIsNone(is_valid)

    def test_updating_password_validate_success(self):
        """Method that tests `reset_password_validate`."""
        data = {"name": "Some_name",
                "email": "example@gmail.com",
                "adress": "some_city",
                "password": "aaaA1"}

        requred_key = "password"

        is_valid = updating_password_validate(data, requred_key)

        self.assertTrue(is_valid)

    def test_updating_password_validate_fail(self):
        """Method that tests `reset_password_validate`."""
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "password": "somepassword"}

        requred_key = "password"

        is_valid = updating_password_validate(data, requred_key)

        self.assertIsNone(is_valid)

    def test_updating_password_validate_required_keys(self):
        """
        Method that tests `updating_password_validate`,
        when `data` does not contain key as value of parameter `new_password`.
        """
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "password": "somepassword"}
        new_password = "ffffff"

        is_valid = updating_password_validate(data, new_password)

        self.assertIsNone(is_valid)

    def test_updating_password_validate_string_validator_password_invalid_type(self):
        """
        Method that tests `updating_password_validate`,
        when value of `data['password']` is not a string.
        """
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "password": 123}
        new_password = "password"

        is_valid = updating_password_validate(data, new_password)

        self.assertIsNone(is_valid)

    def test_updating_password_validate_string_validator_password_invalid_length(self):
        """
        Method that tests `updating_password_validate`,
        when value of `data['password']` has length less than min_length (4).
        """
        data = {"name": "Some_name",
                "email": "some_email",
                "adress": "some_city",
                "password": "s"}
        new_password = "password"

        is_valid = updating_password_validate(data, new_password)

        self.assertIsNone(is_valid)

    def test_imagevalidator_size_pass(self):
        """ Positive test size verification statement"""
        with mock.patch("imghdr.what") as mock_file_extension:
            mock_file_extension.return_value = IMAGE_FORMAT
            self.assertEqual(image_validator(self.image_good), IMAGE_FORMAT)

    def test_imagevalidator_size_fail(self):
        """ Negative test size verification statement"""
        with mock.patch("imghdr.what") as mock_file_extension:
            mock_file_extension.return_value = IMAGE_FORMAT
            self.assertEqual(image_validator(self.image_badsize), False)

    def test_imagevalidator_image_pass(self):
        self.assertEqual(image_validator(self.image_good), IMAGE_FORMAT)

    def test_imagevalidator_image_fail(self):
        self.assertEqual(image_validator(self.image_badcontent), False)


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
        invalid_long_name_data = {'name': 'some name' * 30}

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


class VoteDataValidateTestCase(TestCase):
    """Class that provides test cases for the vote data validate function."""

    def test_none_data(self):
        """Test empty data list"""

        data = {}
        self.assertFalse(vote_data_validator(data, required_keys=[]))

    def test_valid_data(self):
        """Test valid data"""

        valid_data = {'event': 10,
                      'is_active': True,
                      'is_extended': True,
                      'title': 'my new title',
                      'vote_type': 0}
        self.assertTrue(vote_data_validator(valid_data, required_keys=[]))

    def test_required_keys_error(self):
        """Test required keys error"""

        valid_data = {'event': 10,
                      'is_active': True,
                      'is_extended': True,
                      'title': 'my new title',
                      'vote_type': 0}

        self.assertFalse(vote_data_validator(valid_data, required_keys=['vote']))

    def test_validate_error(self):
        """Test validate error"""

        valid_data = {'event': 10,
                      'is_active': True,
                      'is_extended': True,
                      'title': 'my new title',
                      'vote_type': 6}

        self.assertFalse(vote_data_validator(valid_data, required_keys=[]))


class AnswerDataValidateTestCase(TestCase):
    """Class that provides test cases for the answer data validate function."""

    def test_none_data(self):
        """Test empty data list"""

        data = {}
        self.assertFalse(answer_data_validator(data, required_keys=[]))

    def test_valid_data(self):
        """Test valid data"""

        valid_data = {'vote': 10,
                      'text': 'my text',
                      'members': [1, 2]}
        self.assertTrue(answer_data_validator(valid_data, required_keys=[]))

    def test_required_keys_error(self):
        """Test required keys error"""

        valid_data = {'vote': 10,
                      'text': 'my text',
                      'members': [1, 2]}
        self.assertFalse(answer_data_validator(valid_data, required_keys=['answer']))

    def test_validate_error(self):
        """Test validate error"""

        valid_data = {'vote': 10,
                      'text': 123,
                      'members': [1, 2]}

        self.assertFalse(answer_data_validator(valid_data, required_keys=[]))
