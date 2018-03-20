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
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from utils.validators import mentor_validator
from utils.topic_views_functions import find_mentors_topics


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
        mentors_topics_ids = [topic.id for topic in find_mentors_topics(mentor.id)]

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

        assigned_students = MentorStudent.get_assigned_students(mentors_topics_ids,
                                                                mentor.id).filter(**filters)
        my_students = MentorStudent.get_my_students(mentors_topics_ids,
                                                    mentor.id).filter(**filters)
        available_students = MentorStudent.get_available_students(mentors_topics_ids)\
            .filter(**filters)

        response = {'my_students': [],
                    'assigned_students': [],
                    'available_students': []}

        for record in assigned_students:
            student = CustomUser.get_by_id(record.student_id)
            topic = Topic.get_by_id(record.topic_id)
            response['assigned_students'].append({'student_id': student.id,
                                                  'first_name': student.first_name,
                                                  'last_name': student.last_name,
                                                  'topic_title': topic.title,
                                                  'topic_id': topic.id})
        for record in my_students:
            student = CustomUser.get_by_id(record.student_id)
            topic = Topic.get_by_id(record.topic_id)
            response['my_students'].append({'student_id': student.id,
                                            'first_name': student.first_name,
                                            'last_name': student.last_name,
                                            'topic_title': topic.title,
                                            'topic_id': topic.id})

        for record in available_students:
            student = CustomUser.get_by_id(record.student_id)
            topic = Topic.get_by_id(record.topic_id)
            response['available_students'].append({'student_id': student.id,
                                                   'first_name': student.first_name,
                                                   'last_name': student.last_name,
                                                   'topic_title': topic.title,
                                                   'topic_id': topic.id})

        return JsonResponse(response, status=200)

    def post(self, request):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: return JsonResponse within record data with status 201 if record was successfully
                create
        """

        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA
        topic_id = data.get('topicId')
        topic = Topic.get_by_id(topic_id)
        if not topic:
            return RESPONSE_400_INVALID_DATA

        user = request.user
        if user in topic.mentors.all() or user == topic.author:
            return RESPONSE_403_ACCESS_DENIED
        if MentorStudent.topic_student_belonging(topic_id=topic_id, student_id=user.id):
            return RESPONSE_403_ACCESS_DENIED

        mentee = MentorStudent.create(student=user, topic=topic)
        if mentee:
            mentee = mentee.to_dict()
            return JsonResponse(mentee, status=201)

        return RESPONSE_400_INVALID_DATA

    def put(self, request):
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

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

        if user not in topic.mentors.all():
            return RESPONSE_403_ACCESS_DENIED

        record = MentorStudent.topic_student_belonging(topic_id=topic.id, student_id=student.id)
        if record:
            record.update(mentor=user,
                          is_done=data.get('is_done') if data.get('is_done') else 0)
            return RESPONSE_200_UPDATED
        return RESPONSE_400_INVALID_DATA

    def delete(self, request, topic_id):
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param topic_id: ID of the certain topic.
        :type topic_id: `int`

        :return: response with status code 200 when mentee was successfully deleted or response with
                 403 or 404 failed status code.
        :rtype: `HttpResponse object."""

        user = request.user
        mentee = MentorStudent.topic_student_belonging(topic_id=topic_id, student_id=user.id)
        if not mentee:
            return RESPONSE_404_OBJECT_NOT_FOUND
        is_deleted = MentorStudent.delete_by_id(mentee.id)
        if is_deleted:
            return RESPONSE_200_DELETED

        return RESPONSE_400_DB_OPERATION_FAILED


def get_mentors(request):
    """
    Function that handle get request for all mentors list for the certain student.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :return: Mentors list
    """
    user_id = request.user.id
    mentors = set([record.mentor_id for record in MentorStudent.get_my_mentors(user_id)])
    receivers = []
    if mentors:
        receivers = [CustomUser.get_by_id(mentor_id).to_dict()
                     for mentor_id in mentors if mentor_id]
    return JsonResponse({'receivers': receivers}, status=200)


def get_students(request):
    """
    Function that handle get request for all students list for the certain mentor.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :return: Students list
    """

    user_id = request.user.id
    mentors_topics_ids = [topic.id for topic in find_mentors_topics(user_id)]
    students = set([record.student_id for record
                    in MentorStudent.get_my_students(mentors_topics_ids, user_id)])
    receivers = []
    if students:
        receivers = [CustomUser.get_by_id(student_id).to_dict() for student_id in students]
    return JsonResponse({'receivers': receivers}, status=200)


def topic_student_permissions(request, topic_id):
    """
    Function that handle get request for students belonging to the certain topic.

    :param request: The accepted HTTP request.
    :type request: HTTPRequest objects.

    :param topic_id: Id of certain topic.
    :type topic_id: integer.

    :return: JsonResponse with data whether student made request for studying topic and
    whether he have mentor approve
    """
    student = request.user
    mentee_instance = MentorStudent.topic_student_belonging(topic_id=topic_id,
                                                            student_id=student.id)
    is_requested_student = False
    have_mentor = False
    if mentee_instance:
        is_requested_student = True
        if mentee_instance.mentor:
            have_mentor = True
    return JsonResponse({'is_requested_student': is_requested_student,
                         'have_mentor': have_mentor},
                        status=200)
