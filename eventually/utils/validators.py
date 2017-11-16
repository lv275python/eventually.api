"""
Project validators
==================

Module that provides validation functions for all kinds of project's data.
"""
import datetime
import re

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

PASSWORD_REG_EXP = r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$'


def string_validator(value, min_length=0, max_length=None):
    """
    Function that provides string validation.

    :param value: the string literal itself.
    :type value: string

    :param min_length: the minimal length of the received string value.
    :type min_length: integer

    :param max_length: the maximum length of the received string value.
    :type max_length: integer

    :return: `True` if value if valid and `False` if it is not.
    """

    if not isinstance(value, str):
        return False

    if len(value) < min_length:
        return False

    if max_length:
        if len(value) > max_length:
            return False

    return True


def duration_validator(value):
    """
    Function that provides validation for time duration field.

    :param value: the duration that represented as the amount of second.
    :type value: int or float

    :return: `True` if value if valid and `None` if it is not.
    """

    if not isinstance(value, int) and not isinstance(value, float):
        return

    if value < 0:
        return

    try:
        datetime.timedelta(seconds=value)
        return True
    except OverflowError:
        pass


def timestamp_validator(value):
    """
    Function that provides validation for time date and datetime fields.

    :param value: the timestamp that represented as the amount of second.
    :type value: int or float

    :return: `True` if value if valid and `None` if it is not.
    """

    try:
        datetime.datetime.fromtimestamp(value)
        return True
    except (OverflowError, ValueError, OSError, TypeError):
        pass


def required_keys_validator(data, keys_required, strict=True):
    """
    Provide required keys validation.

    :param data: data from request.
    :type data: dictionary

    :param keys_required: list of requied keys for method.
    :type keys_required: list

    :param strict: shows the status of strict method of comparing keys
                   in input data with requred keys in method.
    :type strict: Bool

    :return: `True` if data is valid and `False` if it is not valid.
    """
    keys = list(data.keys())

    if strict:
        keys.sort()
        keys_required.sort()
        return keys == keys_required

    for key in keys_required:
        if key not in keys:
            return False

    return True


def list_of_int_validator(value):
    """
    Function that provides list validation

    :param value: list or tuple with integer items
    :type value: list or tuple

    :return: `True` if value if valid and `False` if it is not.
    """
    if not isinstance(value, (list, tuple)):
        return False
    if not value:
        return False
    if not all(isinstance(item, int) for item in value):
        return False
    return True


def email_validator(email):
    """
    Function that provides string validation.

    :param email: String with email data
    :type email: str

    :return: `True` if email if valid and `False` if it is not.
    """


    try:
        email = email.lower().strip()
        validate_email(email)
        return True
    except (ValidationError, AttributeError):
        pass


def registration_validate(data):
    """Validation data from registration request.

    :param data: registration data
    :type data: dict

    :return: `True` if data is valid and `None` if it is not.
    """

    required_keys = ['email', 'password']
    if not required_keys_validator(data, required_keys, strict=False):
        return False
    for key in ('first_name', 'middle_name', 'last_name'):
        if data.get(key) and not string_validator(data[key], 0, 20):
            return False
    if not string_validator(data['email']) and not email_validator(data['email']):
        return False
    if not string_validator(data['password']) and not password_validator(data['password']):
        return False
    return True


def password_validator(password):
    """
    Function that provides password validation.

    Password should consist of: uppercase letters: A-Z, lowercase letters: a-z, numbers: 0-9

    :param password: the password itself.
    :type password: string

    :return: `True` if password if valid and `None` if it is not.
    """

    try:
        template = re.compile(PASSWORD_REG_EXP)
        if template.match(password):
            return True
    except (TypeError, AttributeError):
        pass


def reset_password_validate(data, requred_key):
    """
    Function that validation for ForgetPassword class

    :param data: dict that we need to validate.
    :type data: dict

    :param requred_key: requred_key for required_keys_validator
    :type requred_key: str

    :return: `True` if data is valid and `None` if it is not.
    """

    if data:
        if required_keys_validator(data, [requred_key], False):
            string = data.get(requred_key)
            if string_validator(string, 4):
                return True
