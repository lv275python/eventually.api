"""
Mentor view module
==================

The module that provides basic logic for getting, creating, updating and deleting
of MentorStudent's model objects.
"""
from datetime import datetime
import pytz

from django.http import JsonResponse
from django.views.generic.base import View
from authentication.models import CustomUser
from mentor.models import MentorStudent
from topic.models import Topic
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from utils.validators import mentor_validator

class MentorView(View):
    """Mentor view handles GET, POST, PUT, DELETE requests."""

    def get(self, request):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: return JsonResponse within filtered students data
        """
        mentor = CustomUser.get_by_id(request.user.id)
        topics_id = [record.id for record in mentor.topic_set.all()]

        filters = {}
        if request.GET.get('topic', None):
            filters['topic_id'] = request.GET.get('topic')
        if request.GET.get('is_done', None):
            filters['is_done'] = True if request.GET.get('is_done') == 'true' else False
        if request.GET.get('from', None):
            from_date = request.GET.get('from')
            from_date = datetime.fromtimestamp(int(from_date), tz=pytz.UTC)
            filters['created_at__gte'] = from_date
        if request.GET.get('to', None):
            to_date = request.GET.get('to')
            to_date = datetime.fromtimestamp(int(to_date), tz=pytz.UTC)
            filters['created_at__lte'] = to_date

        all_students = MentorStudent.get_all_students(mentor.id).filter(**filters)
        my_students = MentorStudent.get_my_students(mentor.id).filter(**filters)
        available_students = MentorStudent.get_available_students().filter(**filters)

        all_students = [record for record in all_students if record.topic_id in topics_id]
        all_students = set([record.student_id for record in all_students])
        all_students = [CustomUser.get_by_id(id).to_dict() for id in all_students]

        my_students = set([item.student_id for item in my_students])
        my_students = [CustomUser.get_by_id(id).to_dict() for id in my_students]

        available_students = set([record.student_id for record in available_students])
        available_students = [CustomUser.get_by_id(id).to_dict() for id in available_students]

        response = {'my_students': my_students,
                    'all_students': all_students,
                    'available_students': available_students}

        return JsonResponse(response, status=200)



    def post(self, request):
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

        record = list(MentorStudent.objects.filter(student_id=student.id, topic_id=topic.id))

        if record:
            record[0].update(mentor=user)
            return RESPONSE_200_UPDATED

        mentor = MentorStudent.create(mentor=user,
                                      student=student,
                                      topic=topic)

        if mentor:
            mentor = mentor.to_dict()
            return JsonResponse(mentor, status=201)
        return RESPONSE_400_INVALID_DATA

def get_mentors(request):
    """
    Function that handle get request for all mentors list for the certain student.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :return: Mentors list
    """
    user_id = request.user.id
    mentors = set([record.mentor_id for record in MentorStudent.get_my_mentors(user_id)])
    mentors = [CustomUser.get_by_id(id).to_dict() for id in mentors]
    return JsonResponse({'receivers': mentors}, status=200)

def get_students(request):
    """
    Function that handle get request for all students list for the certain mentor.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :return: Students list
    """

    user_id = request.user.id
    students = set([record.student_id for record in MentorStudent.get_my_students(user_id)])
    students = [CustomUser.get_by_id(id).to_dict() for id in students]

    return JsonResponse({'receivers': students}, status=200)
