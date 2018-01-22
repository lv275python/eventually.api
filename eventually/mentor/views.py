"""
Mentor view module
==================

The module that provides basic logic for getting, creating, updating and deleting
of MentorStudent's model objects.
"""
from datetime import datetime
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
        """
        mentor = CustomUser.get_by_id(request.user.id)
        topics_id = [record.id for record in mentor.topic_set.all()]

        all_students = MentorStudent.objects.exclude(mentor_id=request.user.id)
        all_students = all_students.exclude(mentor_id=None)

        my_students = MentorStudent.objects.filter(mentor_id=request.user.id)

        available_students = MentorStudent.objects.filter(mentor_id=None)

        # is_done = True if request.GET.get('topic', "") == 'true' else False

        if request.GET.get('topic', None):
            topic = request.GET.get('topic')
            all_students = all_students.filter(topic_id=str(topic))
            my_students = my_students.filter(topic_id=str(topic))
            available_students = available_students.filter(topic_id=str(topic))

        if request.GET.get('is_done', None):
            all_students = all_students.filter(is_done=True)
            my_students = my_students.filter(is_done=True)
            available_students = available_students.filter(is_done=True)

        if request.GET.get('from', None):

            from_date = request.GET.get('from', None)
            from_date = datetime.fromtimestamp(int(from_date))

            all_students = all_students.filter(created_at__gte=from_date)
            my_students = my_students.filter(created_at__gte=from_date)
            available_students = available_students.filter(created_at__gte=from_date)

        if request.GET.get('to', None):
            to_date = request.GET.get('to', None)
            to_date = datetime.fromtimestamp(int(to_date))

            all_students = all_students.filter(created_at__lte=to_date)
            my_students = my_students.filter(created_at__lte=to_date)
            available_students = available_students.filter(created_at__lte=to_date)



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

        record = list(MentorStudent.objects.filter(student_id=student.id, topic_id=topic.id))[0]

        if record:
            record.update(mentor=user)
            return RESPONSE_200_UPDATED

        mentor = MentorStudent.create(mentor=user,
                                      student=student,
                                      topic=topic)

        if mentor:
            mentor = mentor.to_dict()
            return JsonResponse(mentor, status=201)
        return RESPONSE_400_INVALID_DATA
