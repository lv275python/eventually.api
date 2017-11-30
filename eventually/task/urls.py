from django.conf.urls import url, include

from task import views
from .views import TaskView

urlpatterns = [
    url(r'^$', views.TaskView.as_view(), name='index'),
    url(r'^(?P<task_id>\d+)/$', views.TaskView.as_view(), name='detail'),
    url(r'^(?P<task_id>\d+)/comment/', include('comment.urls', namespace='comment')),
]
