"""
Chat application view module.

This module provide logic for the comments model which is the base of chat communication.
"""

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.base import View
from authentication.models import CustomUser
from comment.models import Comment
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_400_DB_OPERATION_FAILED)
from utils.validators import paginator_page_validator, chat_message_validator
from utils.redishelper import REDIS_HELPER as redis

MESSAGES_PER_PAGE = 20

class ChatView(View):
    """
    Chat view that handles GET and POST requests and provides logic for getting and creating of
    chat messages.
    """

    def get(self, request, receiver_id, page_number):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param receiver_id: ID of the certain user.
        :type receiver_id: `int`

        :param page_number: the number of the certain page of chat messages pagination.
        :type page_number: `int`

        :return: the list of chat messages that belong to the certain conversation (messages list
                 that considers for some two users.)
        :rtype: `HttpResponse object`.
        """

        user = request.user
        interlocutor = CustomUser.get_by_id(receiver_id)

        if not interlocutor:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if user.id == interlocutor.id:
            return RESPONSE_400_INVALID_DATA

        user_messages = Comment.objects.filter(Q(author=user) | Q(receiver=user))
        chat_messages = user_messages.filter(Q(author=interlocutor) | Q(receiver=interlocutor))
        ordered_messages = chat_messages.order_by('-created_at')

        messages_paginator = Paginator(ordered_messages, MESSAGES_PER_PAGE)

        if not paginator_page_validator(page_number, messages_paginator.num_pages):
            return RESPONSE_400_INVALID_DATA

        messages_page = messages_paginator.page(page_number)
        next_page = messages_page.next_page_number() if messages_page.has_next() else -1
        messages = []
        for message in messages_page:
            msg = message.to_dict()
            msg['author'] = message.author.to_dict()
            messages.append(msg)
        data = {'messages': messages,
                'next_page': next_page,
                'per_page': MESSAGES_PER_PAGE}

        return JsonResponse(data, status=200)

    def post(self, request, receiver_id):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param receiver_id: ID of the certain user.
        :type receiver_id: `int`

        :return: the response with certain message information when the message was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object.
        """

        author = request.user
        data = request.body

        if not data:
            return RESPONSE_400_EMPTY_JSON

        receiver = CustomUser.get_by_id(receiver_id)
        if not receiver:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if author.id == receiver.id:
            return RESPONSE_400_INVALID_DATA

        if not chat_message_validator(data, required_keys=['text']):
            return RESPONSE_400_INVALID_DATA

        message = Comment.create(author=author, receiver=receiver, text=data.get('text'))

        if not message:
            return RESPONSE_400_DB_OPERATION_FAILED

        return JsonResponse(message.to_dict(), status=201)

class OnlineStatusView(View):
    """Chat view that handles POST requests and provides logic for getting online users"""

    def post(self, request):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: the response with certain online status users.

        """
        data = request.body
        ids = data.get('users')
        users_online = {id: redis.get(id).decode('utf-8') if redis.get(id) else None for id in ids}

        return JsonResponse(users_online, status=200)
