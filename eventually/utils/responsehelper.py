"""
Response helper
===============

Module that provides various HttResponse objects for project.
"""

from django.http import HttpResponse

# status code 2xx
RESPONSE_200_OK = HttpResponse('operation was successful provided', status=200)
RESPONSE_200_UPDATED = HttpResponse('object was successfully updated', status=200)
RESPONSE_200_DELETED = HttpResponse('object was successfully deleted', status=200)
RESPONSE_200_ACTIVATED = HttpResponse('user was successfully activated', status=200)
RESPONSE_201_CREATED = HttpResponse('object was successfully created', status=201)

# status code 4xx
RESPONSE_400_EMPTY_JSON = HttpResponse('empty json received', status=400)
RESPONSE_400_INVALID_DATA = HttpResponse('received data is not valid', status=400)
RESPONSE_400_INVALID_EMAIL = HttpResponse('received email is not valid', status=400)
RESPONSE_400_INVALID_EMAIL_OR_PASSWORD = HttpResponse('email or password is not valid', status=400)
RESPONSE_400_EXISTED_EMAIL = HttpResponse('received email is already exist', status=400)
RESPONSE_400_INVALID_PASSWORD = HttpResponse('received password is not valid', status=400)
RESPONSE_400_INVALID_HTTP_METHOD = HttpResponse('invalid HTTP method', status=400)
RESPONSE_400_DB_OPERATION_FAILED = HttpResponse('database operation is failed', status=400)
RESPONSE_403_ACCESS_DENIED = HttpResponse('access denied', status=403)
RESPONSE_403_USER_NOT_ACTIVE = HttpResponse('user has not active status', status=403)
RESPONSE_403_USER_NOT_AUTHENTICATED = HttpResponse('user is not authenticated', status=403)
RESPONSE_404_OBJECT_NOT_FOUND = HttpResponse('object not found', status=404)
RESPONSE_498_INVALID_TOKEN = HttpResponse('invalid or expired token', status=498)
