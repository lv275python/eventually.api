"""
Mentor view module
==================

The module that provides basic logic for getting, creating, updating and deleting
of MentorStudent's model objects.
"""

from django.http import JsonResponse
from django.views.generic.base import View
from authentication.models import CustomUser
from mentor.models import MentorStudent
from topic.models import Topic
from utils.responsehelper import RESPONSE_400_INVALID_DATA
from utils.validators import mentor_validator

class MentorView(View):
    """Mentor view handles GET, POST, PUT, DELETE requests."""

    def post(self, request, mentor_id=None, student_id=None, topic_id=None):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param mentor_id: ID of the certain mentor.
        :type mentor_id: `int`

        :param student_id: ID of the certain student.
        :type student_id: `int`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: return JsonResponse within record data with status 201 if record was successfully
                 create
        """

        user = request.user
        data = request.body
        if not mentor_validator(data, request.body):
            return RESPONSE_400_INVALID_DATA

        student = CustomUser.get_by_id(data.get("student"))
        topic = Topic.get_by_id(data.get("topic"))
        mentor = MentorStudent.create(mentor=user,
                                      student=student,
                                      topic=topic,
                                      is_done=data.get("is_done") if data.get("is_done") else
                                      False)
        print(mentor)
        if mentor:
            mentor = mentor.to_dict()
            return JsonResponse(mentor, status=201)
        return RESPONSE_400_INVALID_DATA
