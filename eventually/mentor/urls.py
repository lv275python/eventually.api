from django.conf.urls import url
from topic.views import mentors_topics
from .views import MentorView, get_mentors, get_students, topic_student_permissions


urlpatterns = [
    url(r'^$', MentorView.as_view(), name='index'),
    url(r'^delete/(?P<topic_id>\d+)/$', MentorView.as_view(), name='delete'),
    url(r'^is_student/(?P<topic_id>\d+)/$', topic_student_permissions,
        name='topic_student_permissions'),
    url(r'^students/$', MentorView.as_view(), name='mentor'),
    url(r'^mentors_list/$', get_mentors, name='mentors_list'),
    url(r'^students_list/$', get_students, name='students_list'),
    url(r'^topics/$', mentors_topics, name='mentors_topics')
]
