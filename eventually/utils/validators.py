"""
Project validators
==================

Module that provides validation functions for all kinds of project's data.
"""
import datetime
import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

PASSWORD_REG_EXP = r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$'
STR_MIN_LENGTH = 0
STR_MAX_LENGTH = None

def string_validator(value, min_length=STR_MIN_LENGTH, max_length=STR_MAX_LENGTH):
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

    :param keys_required: set or list or tuple of requied keys for method.
    :type keys_required: set or list or tuple

    :param strict: shows the status of strict method of comparing keys
                   in input data with requred keys in method.
    :type strict: Bool

    :return: `True` if data is valid and `False` if it is not valid.
    """
    keys = set(data.keys())
    keys_required = set(keys_required)
    if strict:
        return not keys.symmetric_difference(keys_required)

    return not keys_required.difference(keys)


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


def updating_password_validate(data, new_password):
    """
    Function that validation for ForgetPassword class

    :param data: dict that we need to validate.
    :type data: dict

    :param requred_key: requred_key for required_keys_validator
    :type requred_key: str

    :return: `True` if data is valid and `None` if it is not.
    """

    if data:
        if not required_keys_validator(data, [new_password], False):
            return None
        string = data.get(new_password)
        if not string_validator(string, 4):
            return None
        if password_validator(string):
            return True


def updating_email_validate(data, email):
    """
    Function that validation for ForgetPassword class

    :param data: dict that we need to validate.
    :type data: dict

    :param requred_key: requred_key for required_keys_validator
    :type requred_key: str

    :return: `True` if data is valid and `None` if it is not.
    """
    if data:
        if not required_keys_validator(data, [email], False):
            return None
        if not string_validator(data.get(email), 4):
            return None
        if email_validator(data.get(email)):
            return True

def event_data_validate(data, required_keys):
    """
    Function that provides complete event model data validation

    :param data: the data that is received by event view.
    :type data: dict

    :param required_keys: the list of necessary keys of event data schema.
    :type required_keys: `list`

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """

    errors = []
    if not required_keys_validator(data=data, keys_required=required_keys, strict=False):
        errors.append('required keys error')

    event_model_fields = ['name',
                          'owner',
                          'description',
                          'start_at',
                          'duration',
                          'longitude',
                          'latitude',
                          'budget',
                          'status']

    filtered_data = {key: data.get(key) for key in event_model_fields}
    validation_rules = {'name': lambda val: string_validator(val, min_length=1, max_length=255),
                        'owner': lambda val: isinstance(val, int) and val > 0,
                        'description': string_validator,
                        'start_at': timestamp_validator,
                        'duration': duration_validator,
                        'longitude': lambda val: isinstance(val, float),
                        'latitude': lambda val: isinstance(val, float),
                        'budget': lambda val: isinstance(val, int) and val >= 0,
                        'status': lambda val: isinstance(val, int) and val in range(0, 4)}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid

def login_validate(data):
    """
    Function that provides login data validation.

    :param data: dict that we need to validate.
    :type data: dict

    :return: `True` if data is valid and `None` if it is not.
    :rtype: bool
    """

    if not data:
        return False
    if not required_keys_validator(data, ['email', 'password']):
        return False
    if not email_validator(data['email']):
        return False
    return True
