from django.conf.urls import url
from .views import MentorView, get_mentors, get_students

urlpatterns = [
    url(r'^students/$', MentorView.as_view(), name='mentor'),
    url(r'^mentors_list/$', get_mentors, name='mentors_list'),
    url(r'^students_list/$', get_students, name='students_list')
]
