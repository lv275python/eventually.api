"""Views"""

from django.views.generic.base import View
from django.http import JsonResponse
from assignment.models import Assignment

from utils.responsehelper import (RESPONSE_404_OBJECT_NOT_FOUND)


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
