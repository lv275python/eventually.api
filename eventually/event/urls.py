from django.conf.urls import url, include
from .views import EventView

urlpatterns = [
    url(r'^$', EventView.as_view(), name='index'),
    url(r'^(?P<event_id>\d+)/$', EventView.as_view(), name='detail'),
    url(r'^(?P<event_id>\d+)/comment/', include('comment.urls', namespace='event_comment')),
    url(r'^(?P<event_id>\d+)/task/', include('task.urls', namespace='task')),
    url(r'^(?P<event_id>\d+)/vote/', include('vote.urls', namespace='vote')),
]
