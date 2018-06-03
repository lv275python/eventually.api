from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AssignmentAnswerView.as_view(), name='AssignmentAnswer'),
    url(r'^curriculums/$', views.get_curriculum_list, name='curriculums'),
    url(r'^(?P<curriculum_id>\d+)/topics/$', views.get_topic_list, name='topics'),
]
