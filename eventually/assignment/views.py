"""Views"""

from datetime import datetime

from django.views.generic.base import View
from django.http import JsonResponse

from eventually.settings import FRONT_HOST
from assignment.models import Assignment
from authentication.models import CustomUser
from item.models import Item
from mentor.models import MentorStudent
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

        :param topic_id: topic id
        :type request: int

        :return: return JsonResponse with data and status 200
                 or HttpRequest with error if parameters are bad.

        """

        student = CustomUser.get_by_id(request.user)
        assignments = Assignment.get_assignments_by_student_topic_item_ids(student_id=student.id, topic_id=topic_id)
        data = {'assignments': [assignment.to_dict() for assignment in assignments]}
        return JsonResponse(data, status=200)

    def post(self, request):
        """
        Handle POST request

        :param request: the accepted HTTP request. Is required
        :type request: HttpRequest

        :return: return Response with status 201
                 or Response with error if parameters are bad.
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

        :param assignment_id: assignment id
        :type assignment_id: int

        :return: return JsonResponse with statement data and status 200
                 or HttpRequest with error if parameters are bad.
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

        if status == STATUS_IN_PROCESS:
            new_data = {'status': status,
                        'started_at': datetime.now()}
            assignment.update(**new_data)
            return RESPONSE_200_UPDATED

        if status == STATUS_IS_DONE:
            if assignment.item.form == FORM_THEORETIC:
                new_data = {'status': status,
                            'grade': True,
                            'finished_at': datetime.now()}
                assignment.update(**new_data)
                create_assignments_for_subordinate_items(assignment)

            elif assignment.item.form == FORM_PRACTICE:

                statement = data.get('statement')
                if not statement:
                    return RESPONSE_400_INVALID_DATA

                new_data = {'status': status,
                            'statement': statement,
                            'finished_at': datetime.now()}
                assignment.update(**new_data)
            return RESPONSE_200_UPDATED


class AssignmentsMentorView(View):
    """Assignment view that handles GET, PUT requests."""

    def get(self, request):
        """
        Handle GET request

        :param request: the accepted HTTP request. Is required
        :type request: HttpRequest

        :return: return JsonResponse within status and statement data with status 200
                 or HttpRequest with error if parameters are bad.
        """
        mentor = request.user
        curriculums = Assignment.get_curriculums_by_mentor_id(mentor)
        response = {'curriculums': [curriculum.to_dict() for curriculum in curriculums]}
        return JsonResponse(response, status=200)

    def put(self, request, assignment_id=None):
        """
        Handle PUT request

        :param request: the accepted HTTP request. Is required
        :type request: HttpRequest

        :param assignment_id:
        :type assignment_id: int

        :return: HttpResponse object with status 200, if parameters are ok,
        HttpResponse object with status 404, if assignment_id is not defined and
        HttpResponse object with status 400, if data is invalid

        """
        data = request.body
        if not data:
            return RESPONSE_400_INVALID_DATA
        assignment = Assignment.get_by_id(assignment_id)
        if not assignment:
            return RESPONSE_404_OBJECT_NOT_FOUND
        grade = data.get('grade')

        if grade:
            response = {
                'grade': True,
                'finished_at': datetime.now()
            }
            assignment.update(**response)
            create_assignments_for_subordinate_items(assignment)

        status = data.get('status')
        if status:
            response = {
                'status': status
            }
            assignment.update(**response)

        return RESPONSE_200_UPDATED


def get_curriculum_list(request):
    """
    Handle GET request

    :param request: the accepted HTTP request. Is required
    :type request: HttpRequest

    :return: JsonResponse within status and statement data with status 200
                 or HttpRequest with error if parameters are bad.
    """
    if request.method == "GET":
        student = request.user
        curriculums = Assignment.get_curriculums(student)
        if curriculums:
            data = {'curriculums': [curriculum.to_dict() for curriculum in curriculums]}
            return JsonResponse(data, status=200)
        else:
            return RESPONSE_404_OBJECT_NOT_FOUND


def get_topic_list(request, curriculum_id=None):
    """
    Handle GET request

    :param request: the accepted HTTP request. Is required
    :type request: HttpRequest

    :param curriculum_id: curriculum_id
    type curriculum_id: int


    :return: JsonResponse within status and statement data with status 200
                 or HttpRequest with error if parameters are bad.
    """
    if request.method == "GET":
        student = request.user
        topics = Assignment.get_topics(student, curriculum_id)
        if topics:
            data = {'topics': [topic.to_dict() for topic in topics]}
            return JsonResponse(data, status=200)
        else:
            return RESPONSE_404_OBJECT_NOT_FOUND

def get_assignment_list(request, topic_id, user_id=None):
    """
    Handle GET request

    :param request: the accepted HTTP request. Is required
    :type request: HttpRequest

    :param topic_id: topic_id
    :type topic_id: int

    :param user_id: user_id
    :type user_id: int

    :return: JsonResponse within status and statement data with status 200
                 or HttpRequest with error if parameters are bad.
    """
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
    """
    Handle POST request

    :param request:the accepted HTTP request. Is required
    :type request: HttpRequest

    :return: HttpResponse object with status 200, if parameters are ok,
        HttpResponse object with status 400 if data is invalid or if request method is not POST
    """
    if request.method == 'POST':
        data = request.body
        id = data.get('userId')
        if not data:
            return RESPONSE_400_INVALID_DATA
        user = CustomUser.get_by_id(id)
        if not user:
            return RESPONSE_400_INVALID_DATA,
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


def create_assignment_for_new_item(new_item):
    """
    Create assignment for items added after students are approved for topic

    :param new_item: item added after students are approved for topic
    :type new_item: Item object

    :return: None
    """

    topic_students = MentorStudent.get_topic_all_students(new_item.topic_id)
    superiors_ids = new_item.get_item_superiors()[1]

    for mentor_student in topic_students:
        student_id = mentor_student.student_id
        student_user = CustomUser.get_by_id(student_id)
        if not superiors_ids:
            Assignment.create(user=student_user, item=new_item)
        else:
            for superior_item_id in superiors_ids:
                superior_assignment = Assignment.\
                    get_assignments_by_student_topic_item_ids(student_id=student_id, item_id=superior_item_id)
                if not superior_assignment or not superior_assignment.status == STATUS_IS_DONE \
                        or superior_assignment.grade is not True:
                    break
                else:
                    Assignment.create(user=student_user, item=new_item)


def create_assignments_for_subordinate_items(assignment):
    """
    Create next assignments for subordinate items after superior assignment is finished

    :param assignment: Finished superior assignment object
    :type assignment: Assignment object

    :return: List of created subordinate assignments' dictionaries
    """

    user = CustomUser.get_by_id(assignment.user_id)
    current_item_id = assignment.item_id
    subordinates = Item.get_subordinate_items(superior_item_id=current_item_id)
    new_assignments = []

    for subordinate_item in subordinates:
        superiors_ids = subordinate_item.get_item_superiors()[1]
        for superior_item_id in superiors_ids:
            superior_assignment = Assignment.get_assignments_by_student_topic_item_ids(
                student_id=user.id, item_id=superior_item_id)
            if not superior_assignment or not superior_assignment.status == STATUS_IS_DONE \
                    or superior_assignment.grade is not True:
                break
            else:
                new_assignment = Assignment.create(user=user, item=subordinate_item)
                new_assignments.append(new_assignment.to_dict())

    return new_assignments
