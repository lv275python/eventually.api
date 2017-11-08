from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TaskView.as_view()),
    url(r'^(?P<task_id>\d+)/$', views.TaskView.as_view()),
]
