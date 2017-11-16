from django.conf.urls import url, include
from .views import EventView

urlpatterns = [
    url(r'^$', EventView.as_view()),
    url(r'^(?P<event_id>\d+)/$', EventView.as_view()),
    url(r'^(?P<event_id>\d+)/comment/', include('comment.urls')),
    url(r'^(?P<event_id>\d+)/task/', include('task.urls')),
    url(r'^(?P<event_id>\d+)/vote/', include('vote.urls')),
]
