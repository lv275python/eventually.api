"""
JWT Token
=========

The module that provides creating and handling JWT tokens.
"""

import jwt
from django.conf import settings
from django.utils import timezone

SECRET_KEY = settings.JWT_TOKEN_KEY
ALGORITHM = settings.JWT_ALGORITHM


def create_token(data, expiration_time=None, not_before_time=None):
    """
    Function that creates JWT token with received date and certain expiration time.

    :param data: The data that will be contained inside token's payload.
    :type data: dict

    :param expiration_time: A number of seconds while the current token will be valid.
    :type expiration_time: int

    :param not_before_time: A number of seconds before time when token will become valid.
    :type not_before_time: int

    :return: JWT token if it is possible to create token with the received date or
             `None` if the data has incorrect format.
    """

    try:
        if expiration_time:
            exp = int(timezone.now().timestamp()) + expiration_time
            data['exp'] = exp

        if not_before_time:
            nbf = int(timezone.now().timestamp()) + not_before_time
            data['nbf'] = nbf

        token = jwt.encode(data, SECRET_KEY, ALGORITHM)
        return token

    except TypeError:
        pass


def handle_token(jwt_token):
    """
    Function that handle the received JWT token.

    :param jwt_token: the certain JWT token.
    :type jwt_token: string

    :return: `dict` with tokens' data or `None` if the token has an incorrect format or his
             expiration time went out.
    """

    try:
        return jwt.decode(jwt_token, SECRET_KEY, ALGORITHM)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        pass
