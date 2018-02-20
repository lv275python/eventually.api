from django.conf.urls import url
from .views import MentorView, get_mentors, get_students, is_topic_student


urlpatterns = [
    url(r'^$', MentorView.as_view(), name='index'),
    url(r'^delete/(?P<topic_id>\d+)/$', MentorView.as_view(), name='delete'),
    url(r'^is_student/(?P<topic_id>\d+)/$', is_topic_student, name='is_topic_student'),
    url(r'^students/$', MentorView.as_view(), name='mentor'),
    url(r'^mentors_list/$', get_mentors, name='mentors_list'),
    url(r'^students_list/$', get_students, name='students_list')
]
