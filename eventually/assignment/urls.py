from django.conf.urls import url
from . import views
from assignment.views import send_answer

urlpatterns = [

    url(r'^$', views.AssignmentStudentView.as_view(), name='AssignmentStudent'),
    url(r'^(?P<assignment_id>\d+)/$', views.AssignmentStudentView.as_view(), name='AssignmentStudentDetail'),
    url(r'^mentor/(?P<assignment_id>\d+)$', views.AssignmentsMentorView.as_view(), name='complete'),
    url(r'^mentor/curriculum/$', views.AssignmentsMentorView.as_view(), name='mentorlabla'),
    url(r'^curriculums/$', views.get_curriculum_list, name='curriculums'),
    url(r'^(?P<curriculum_id>\d+)/topics/$', views.get_topic_list, name='topics'),
    url(r'^list/(?P<topic_id>\d+)$', views.get_assignment_list, name='assignment_list_students'),
    url(r'^list/(?P<topic_id>\d+)/(?P<user_id>\d+)$', views.get_assignment_list, name='assignment_list'),
    url(r'^mentor/send_answer/$', send_answer, name='SendAnswer'),
    url(r'^answer/$', views.AssignmentAnswerView.as_view(), name='AssignmentAnswer'),
]
