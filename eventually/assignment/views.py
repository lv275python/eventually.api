"""Views"""

from datetime import datetime

from django.views.generic.base import View
from django.http import JsonResponse

from eventually.settings import FRONT_HOST
from assignment.models import Assignment
from authentication.models import CustomUser
from item.models import Item
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_200_OK,
                                  RESPONSE_201_CREATED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from utils.send_mail import send_email

STATUS_IN_PROCESS = 1
STATUS_IS_DONE = 2
FORM_THEORETIC = 0
FORM_PRACTICE = 1


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
    """Assignment view that handles GET, POST, PUT requests."""

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
        assignments = Assignment.get_assignments_by_student_topic_item_ids(student_id=student.id, topic_id=topic_id)
        data = {'assignments': [assignment.to_dict() for assignment in assignments]}
        return JsonResponse(data, status=200)

    def post(self, request):
        """

        :param request:
        :return:
        """

        data = request.body

        student = CustomUser.get_by_id(data.get('student'))
        items = Item.get_items_by_topic_id(data.get('topic'))

        if not items:
            return RESPONSE_404_OBJECT_NOT_FOUND

        for item in items:
            if not item.get_item_superiors()[1]:
                Assignment.create(user=student, item=item)

        return RESPONSE_201_CREATED

    def put(self, request, assignment_id=None):
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
        grade = data.get('grade')
        if not status and not grade:
            return RESPONSE_400_INVALID_DATA

        if status == STATUS_IN_PROCESS:
            new_data = {'status': status,
                        'started_at': datetime.now()}
            assignment.update(**new_data)
            return RESPONSE_200_UPDATED

        if status == STATUS_IS_DONE:
            if assignment.item.form == FORM_THEORETIC:
                new_data = {'status': status,
                            'finished_at': datetime.now()}
                assignment.update(**new_data)

            elif assignment.item.form == FORM_PRACTICE:

                statement = data.get('statement')
                if not statement:
                    return RESPONSE_400_INVALID_DATA

                new_data = {'status': status,
                            'statement': statement,
                            'finished_at': datetime.now()}
                assignment.update(**new_data)
                return RESPONSE_200_UPDATED

        user = CustomUser.get_by_id(assignment.user_id)
        current_item_id = assignment.item_id
        if grade is True:
            new_data = {'grade': grade,
                        'finished_at': datetime.now()}
            assignment.update(**new_data)

            # create next assignments for subordinate items
            new_assignments = []
            subordinates = Item.get_subordinate_items(superior_item_id=current_item_id)
            for subordinate_item in subordinates:
                superiors_ids = subordinate_item.get_item_superiors()[1]
                for superior_item_id in superiors_ids:
                    superior_assignment = Assignment.\
                        get_assignments_by_student_topic_item_ids(student_id=user.id, item_id=superior_item_id)
                    if not superior_assignment or not superior_assignment.status == 2\
                                or superior_assignment.grade is not True:
                        break
                    else:
                        new_assignment = Assignment.create(user=user, item=subordinate_item)
                        new_assignments.append(new_assignment.to_dict())
            return RESPONSE_200_UPDATED

        elif grade is False:
            new_data = {'status': STATUS_IN_PROCESS}
            assignment.update(**new_data)
            return RESPONSE_200_UPDATED


class AssignmentsMentorView(View):
    """Assignment view that handles GET, POST, PUT, DELETE requests."""

    def get(self, request, curriculum_id=None):
        """
        """
        mentor = request.user
        if curriculum_id:
            topics = Assignment.get_topics_by_mentor_id(mentor)
            response = {'topics': [topics.to_dict() for topic in topics]}
            return JsonResponse(response, status=200)
        else:
            curriculums = Assignment.get_curriculums_by_mentor_id(mentor)
            response = {'curriculums': [curriculum.to_dict() for curriculum in curriculums]}
            return JsonResponse(response, status=200)

    def put(self, request, assignment_id=None):
        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA
        assignment = Assignment.get_by_id(assignment_id)
        if not assignment:
            return RESPONSE_404_OBJECT_NOT_FOUND
        grade = data.get('grade')

        if grade:
            response = {
                'grade' : True
            }
            assignment.update(**response)

        status = data.get('status')
        if status:
            response = {
                'status' : status
            }
            assignment.update(**response)

        return RESPONSE_200_UPDATED


def get_curriculum_list(request):
    if request.method == "GET":
        student = request.user
        curriculums = Assignment.get_curriculums(student)
        if curriculums:
            data = {'curriculums': [curriculum.to_dict() for curriculum in curriculums]}
            return JsonResponse(data, status=200)
        else:
            return RESPONSE_404_OBJECT_NOT_FOUND


def get_topic_list(request, curriculum_id=None):
    if request.method == "GET":
        student = request.user
        topics = Assignment.get_topics(student, curriculum_id)
        if topics:
            data = {'topics': [topic.to_dict() for topic in topics]}
            return JsonResponse(data, status=200)
        else:
            return RESPONSE_404_OBJECT_NOT_FOUND


def get_assignment_list(request, topic_id, user_id=None):
    if request.method == "GET":
        if user_id:
            user = CustomUser.get_by_id(user_id)
            assignments = Assignment.get_assignments_by_mentor_id(user, topic_id)
        else:
            user = request.user
            assignments = Assignment.get_assignments_by_student_topic_item_ids(student_id=user, topic_id=topic_id)
        if assignments:
            data = {'assignments': [{'assignment': assignment.to_dict(), 'item': assignment.item.to_dict()}
                                    for assignment in assignments]}
            return JsonResponse(data, status=200)
        else:
            return RESPONSE_404_OBJECT_NOT_FOUND


def send_answer(request):
    if request.method == 'POST':
        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA
        id = data.get('userId')
        user = CustomUser.get_by_id(id)
        if not user:
            return RESPONSE_400_INVALID_DATA
        answer = data.get('message')
        ctx = {
            'user_name': user.first_name,
            'response': answer,
            'domain': FRONT_HOST,
        }
        message = 'mentor answer'
        subject = 'rejected answer'
        send_email(subject, message, [user.email], 'mentor_answer.html', ctx)
        return RESPONSE_200_OK
    return RESPONSE_400_INVALID_DATA
