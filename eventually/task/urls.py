from django.conf.urls import url, include
from .views import TaskView

urlpatterns = [
    url(r'^$', TaskView.as_view()),
    url(r'^(?P<task_id>\d+)/$', TaskView.as_view()),
    url(r'^(?P<task_id>\d+)/comment/', include('comment.urls')),
]
