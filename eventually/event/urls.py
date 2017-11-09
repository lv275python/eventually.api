from django.conf.urls import url
from .views import EventView

urlpatterns = [
    url(r'^$', EventView.as_view(), name='index'),
    url(r'^(?P<event_id>\d+)/$', EventView.as_view(), name='detail'),
]
