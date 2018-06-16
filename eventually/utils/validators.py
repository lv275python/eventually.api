"""
Project validators
==================

Module that provides validation functions for all kinds of project's data.
"""
import datetime
import re
import imghdr
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.datastructures import MultiValueDictKeyError

PASSWORD_REG_EXP = r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$'
STR_MIN_LENGTH = 0
STR_MAX_LENGTH = None
MAX_IMAGE_FILESIZE = 8 * 1024 * 1024
MAX_FILESIZE = 1024 * 1024 * 1024

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
                   in input data with required keys in method.
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
    if not (string_validator(data['email']) and email_validator(data['email'])):
        return False
    if not (string_validator(data['password']) and password_validator(data['password'])):
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

def event_paginator_validate_limit(request):
    """
    Function that provides event paginator limit validation

    :param request: the data with events limit for pagination
    that is received from event view.
    :type request: QueryDict

    :return: `True` if valid data, else `False`
    :rtype `bool`
    """
    try:
        int(request['limit'])
    except (MultiValueDictKeyError, KeyError):
        return False
    return True

def event_paginator_validate_number(request):
    """
    Function that provides event paginator limit validation

    :param request: the data with events limit for pagination
    that is received from event view.
    :type request: QueryDict

    :return: `True` if valid data, else `False`
    :rtype `bool`
    """
    try:
        int(request['number'])
    except (MultiValueDictKeyError, KeyError):
        return False

    return True

def event_paginator_validate(request):
    """
    Function that provides event paginator number validation

    :param request: the data with number for pagination
    that is received from event view.
    :type request: QueryDict

    :return: `True` if valid data, else `False`
    :rtype `bool`
    """
    number = _request_get_param(request, "number")
    limit = _request_get_param(request, "limit")
    if (number and limit) or (not number and not limit):
        return True
    return False

def event_from_date_param_validate(request):
    """
    Function that provides event paginator number validation

    :param request: the data with number for pagination
    that is received from event view.
    :type request: QueryDict

    :return: `True` if valid data, else `False`
    :rtype `bool`
    """
    try:
        request['from_date']
    except (MultiValueDictKeyError, KeyError):
        return False
    return True

def _request_get_param(request, key):
    """
    Function that provides event paginator number validation

    :param request: the data with number for pagination
    that is received from event view.
    :type request: QueryDict

    :return: `True` if valid data, else `False`
    :rtype `bool`
    """
    try:
        return request[key]
    except (MultiValueDictKeyError, KeyError):
        pass

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

def comment_data_validator(data, required_keys):
    """
    Function that provides complete comment model data validation

    :param data: the data that is received by comment view.
    :type data: dict

    :param required_keys: the list of necessary keys of comment data schema.
    :type required_keys: `list`

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """

    errors = []
    if not required_keys_validator(data=data, keys_required=required_keys, strict=False):
        errors.append('required keys error')

    comment_model_fields = ['text',
                            'team',
                            'event',
                            'vote',
                            'task',
                            'author']

    filtered_data = {key: data.get(key) for key in comment_model_fields}
    validation_rules = {'text': lambda val: string_validator(val, min_length=1, max_length=255),
                        'team': lambda val: isinstance(val, int) and val > 0,
                        'event': lambda val: isinstance(val, int) and val > 0,
                        'vote': lambda val: isinstance(val, int) and val > 0,
                        'task': lambda val: isinstance(val, int) and val > 0,
                        'author': lambda val: isinstance(val, int) and val > 0}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid

def valid_date_type(date):
    """custom argparse *date* type for user dates values given from the command line"""
    if not isinstance(date, str):
        return False
    for mask in ['%Y%m%d', '%Y-%m-%d', '%d%m%Y', '%m%d%Y']:
        try:
            datetime.datetime.strptime(date, mask)
            return True
        except ValueError:
            pass

def profile_data_validator(data):
    """
    Function that validation incoming request.body
    :param request_body: data that need to validate.
    :type data: HttpRequest
    :return: return True not data.
    """

    is_hobby_valid = string_validator(data.get("hobby")) if data.get('hobby') else True
    if not is_hobby_valid:
        return

    is_birthday_valid = valid_date_type(data.get("birthday")) if data.get('birthday') else True
    if not is_birthday_valid:
        return

    is_photo_valid = string_validator(data.get("photo")) if data.get('photo') else True
    if not is_photo_valid:
        return

    return True

def vote_data_validator(data, required_keys):
    """
    Function that validation incoming request.body

    :param data: data
    :type data: HttpRequest

    :param required_keys: data that need to validate.
    :type required_keys: HttpRequest

    :return: data if data is valid and `None` if it is not.
    """

    if not data:
        return False

    errors = []
    if not required_keys_validator(data=data, keys_required=required_keys, strict=False):
        errors.append('required keys error')

    vote_fields = ["event", "is_active", "is_extended", "title", "vote_type"]

    filtered_data = {key: data.get(key) for key in vote_fields}

    validation_rules = {'event': lambda val: isinstance(val, int),
                        'is_active': lambda val: isinstance(val, bool),
                        'is_extended': lambda val: isinstance(val, bool),
                        'title': lambda val: string_validator(val, min_length=1, max_length=100),
                        'vote_type': lambda val: isinstance(val, int) and val in range(0, 2)}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid

def answer_data_validator(data, required_keys):
    """
    Function that validation incoming request.body

    :param data: data
    :type data: HttpRequest

    :param required_keys: data that need to validate.
    :type required_keys: HttpRequest

    :return: data if data is valid and `None` if it is not.
    """

    if not data:
        return False

    errors = []
    if not required_keys_validator(data=data, keys_required=required_keys, strict=False):
        errors.append('required keys error')

    vote_fields = ["vote", "text", "members"]

    filtered_data = {key: data.get(key) for key in vote_fields}

    validation_rules = {'vote': lambda val: isinstance(val, int),
                        'text': lambda val: string_validator(val, min_length=1, max_length=100),
                        'members': lambda val: True if not val else list_of_int_validator(val)}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid

def task_data_validate_create(data):
    """
    Function that provides complete task model data validation

    :param data: the data that is received by task view.
    :type data: dict

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """
    status = data.get('status')
    status_range = range(0, 3)
    required_keys = ['title', 'description', 'status']

    if not required_keys_validator(data, required_keys, False):
        return False
    if not string_validator(data.get('title'), max_length=255):
        return False
    if not string_validator(data.get('description'), max_length=1024):
        return False
    if data.get('users'):
        if not list_of_int_validator(data.get('users')):
            return False
    if not(isinstance(status, int) and status in status_range):
        return False
    return True

def task_data_validate_update(data):
    """
    Function that provides complete task model data validation

    :param data: the data that is received by task view.
    :type data: dict

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """

    errors = []
    task_model_fields = ['title', 'description', 'status', 'add_users', 'remove_users']

    filtered_data = {key: data.get(key) for key in task_model_fields}
    validation_rules = {'title': lambda val: string_validator(val, max_length=255),
                        'description': lambda val: string_validator(val, max_length=1024),
                        'add_users': list_of_int_validator,
                        'remove_users': list_of_int_validator,
                        'status': lambda val: isinstance(val, int) and val in range(0, 3)}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid

def mentor_validator(data, required_keys):
    """
    Function that provides complete mentorStudent model data validation

    :param data: the data that is received by task view.
    :type data: dict

    :return: data if data is valid and `None` if it is not
    """

    if not data:
        return False

    errors = []
    if not required_keys_validator(data=data, keys_required=required_keys, strict=False):
        errors.append('required keys error')

    vote_fields = ['student', 'topic']

    filtered_data = {key: data.get(key) for key in vote_fields}

    validation_rules = {'student': lambda val: isinstance(val, int),
                        'topic': lambda val: isinstance(val, int)}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid

def image_validator(image_file):
    """
    Checks if the uploaded file is a valid image file.
    A valid image file has to be of gif, png, jpg/jpeg or bmp file type.
    Maximum file size allowed is 8 MB.

    :param image_file: image file
    :type image_file: UploadedFile object

    :return: string image extension or False
    """

    valid_extensions = ('gif', 'png', 'jpg', 'jpeg', 'bmp')

    if image_file.size > MAX_IMAGE_FILESIZE:
        return False

    file_extension = imghdr.what(image_file)
    if not file_extension in valid_extensions:
        return False

    return file_extension


def file_validator(file):
    """
    Checks if the file has acceptable size.
    Maximum file size allowed is 1Gb.

    :param file: file
    :type file: MultiValueDict

    :return: True if file is valid and False if not
    :rtype: bool
    """

    if file.size > MAX_FILESIZE:
        return False
    else:
        return True


def paginator_page_validator(page_number, pages_amount):
    """
    Function that provides validation for chat view paginator pages.

    :param page_number: number of the accepted page.
    :type page_number: `int`

    :param pages_amount: the amount of all of the currently existed pages.
    :type pages_amount: `int`

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """

    return int(page_number) in range(1, (pages_amount + 1))

def chat_message_validator(data, required_keys):
    """
    Function that provides complete chat messages view data validation

    :param data: the data that is received by chat view.
    :type data: `dict`

    :param required_keys: the list of necessary keys of message data schema.
    :type required_keys: `list`

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """

    errors = []

    if not required_keys_validator(data=data, keys_required=required_keys, strict=False):
        errors.append('required keys error')

    if not string_validator(value=data.get('text'), max_length=1024, min_length=1):
        errors.append('text field error')

    is_data_valid = len(errors) == 0
    return is_data_valid
