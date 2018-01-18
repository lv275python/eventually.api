"""
Mentor view module
==================

The module that provides basic logic for getting, creating, updating and deleting
of MentorStudent's model objects.
"""
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from mentor.models import MentorStudent
from authentication.models import CustomUser
from mentor.models import MentorStudent
from topic.models import Topic
from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from utils.validators import mentor_validator

class MentorView(View):
    """Mentor view handles GET, POST, PUT, DELETE requests."""

    def get(self, request):
        """
        Method that handles GET request.
        """
        mentor = CustomUser.get_by_id(request.user.id)
        mentor_topics = mentor.topic_set.all()
        mentor_topics = [record.id for record in mentor_topics]


        all_students = MentorStudent.objects.exclude(mentor_id=request.user.id)
        all_students = all_students.exclude(mentor_id=None)
        all_students = [record for record in all_students if record.topic_id in mentor_topics]
        all_students = set([record.student_id for record in all_students])
        all_students = [CustomUser.get_by_id(id).to_dict() for id in all_students]


        my_students = MentorStudent.objects.filter(mentor_id=request.user.id)
        my_students = set([item.student_id for item in my_students])
        my_students = [CustomUser.get_by_id(id).to_dict() for id in my_students]


        available_students = MentorStudent.objects.filter(mentor_id=None)
        available_students = [record.student_id for record in available_students]
        available_students = [CustomUser.get_by_id(id).to_dict() for id in available_students]
        response = {'my_students': my_students,
                    'all_students': all_students,
                    'available_students': available_students}


        return JsonResponse(response, status=200)



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

        student = CustomUser.get_by_id(data.get('student'))
        topic = Topic.get_by_id(data.get('topic'))

        if not student or not topic:
            return RESPONSE_404_OBJECT_NOT_FOUND

        mentor = MentorStudent.create(mentor=user,
                                      student=student,
                                      topic=topic)

        if mentor:
            mentor = mentor.to_dict()
            return JsonResponse(mentor, status=201)
        return RESPONSE_400_INVALID_DATA
