from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.AssignmentAnswerView.as_view(), name='AssignmentAnswer'),
    url(r'^$', views.AssignmentStudentView.as_view(), name='AssignmentStudent'),
    url(r'^(?P<assignment_id>\d+)/$', views.AssignmentStudentView.as_view(), name='AssignmentStudentDetail'),
]
