"""Views"""

from django.views.generic.base import View
from django.http import JsonResponse
from assignment.models import Assignment
from authentication.models import CustomUser
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from curriculum.models import Curriculum
from mentor.models import MentorStudent


class AssignmentAnswerView(View):
    """AssignmentAnswer view handles GET, POST, PUT, DELETE requests."""
    def get(self, request):
        """
        Handle GET request.

        :param request: client HttpRequest. Is required
        :type request: HttpRequest

        :return: return JsonResponse within status and statement data with status 201
                 or HttpRequest with error if parameters are bad.

        """
        user = request.user
        assignments = Assignment.objects.filter(user=user)
        if assignments:
            new_date = []
            for ass in assignments:
                new_date.append({
                    'statuses':ass.status,
                    'statements':ass.statement
                })
            data = {'new_date': new_date[::-1]}
            return JsonResponse(data, status=201)
        return RESPONSE_404_OBJECT_NOT_FOUND


class AssignmentStudentView(View):
    """Assignment view that handles GET, POST, PUT, DELETE requests."""

    def get(self, request, topic_id=None):
        """
        Handle GET request

        :param request: the accepted HTTP request. Is required
        :type request: HttpRequest

        :param topic_id: topic_id
        :type request: int

        :return: return JsonResponse within status and statement data with status 200
                 or HttpRequest with error if parameters are bad.

        """

        student = CustomUser.get_by_id(request.user)
        assignments = Assignment.get_assignmets_by_student_id(student.id, topic_id)
        data = {'assignments': [assignment.to_dict() for assignment in assignments]}
        return JsonResponse(data, status=200)

    def post(self, request):
        """

        :param request:
        :return:
        """

        data = request.body

        response = {}

        Assignment.create(**response)

    def put(self, request, assignment_id):
        """
        Handle PUT request

        :param request: the accepted HTTP request.
        :type request: HttpRequest

        :param assignment_id:
        :type assignment_id: int

        # :return:
        # :rtype: HttpResponse object
        """

        assignment = Assignment.get_by_id(assignment_id)

        if not assignment:
            return RESPONSE_404_OBJECT_NOT_FOUND

        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA

        status = data.get('status')
        if not status:
            return RESPONSE_400_INVALID_DATA

        if status == 1:
            assignment.update({"status": 1})

        if status == 2:
            response = {'status': status,
                        'statement': data.get('statement')
                        # 'started_at': ,
                        }
            assignment.update(**response)

        return RESPONSE_200_UPDATED


def get_curriculum_list(request):
    student = request.user
    curriculums = Assignment.get_curriculums(student)
    data = {'curriculums': [curriculum.to_dict() for curriculum in curriculums]}
    return JsonResponse(data, status=200)


def get_topic_list(request, curriculum_id=None):
    student = request.user
    topics =Assignment.get_curriculums(studen MentorStudent.get_student_topics(student, curriculum_id)
    data = {'topics': [topic.to_dict() for topic in topics]}
    return JsonResponse(data, status=200)


def get_assignment_list(request, topic_id):
    user = request.user
    assignments = Assignment.get_assignments_by_student_id(user, topic_id)
    data = {'assignments': [{'assignment':assignment.to_dict(), 'item':assignment.item.to_dict()}
            for assignment in assignments]}
    return JsonResponse(data, status=200)
