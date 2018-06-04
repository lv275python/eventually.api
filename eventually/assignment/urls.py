from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AssignmentAnswerView.as_view(), name='AssignmentAnswer'),
    url(r'^curriculums/$', views.get_curriculum_list, name='curriculums'),
    url(r'^(?P<curriculum_id>\d+)/topics/$', views.get_topic_list, name='topics'),
    url(r'^mentor/curriculum/$', views.AssigmentsMentorView.as_view(), name='mentorlabla'),
    url(r'^(?P<topic_id>\d+)$', views.get_assignment_list, name='assignment_list_students'),
    url(r'^(?P<topic_id>\d+)/(?P<user_id>\d+)$', views.get_assignment_list, name='assignment_list'),
]
