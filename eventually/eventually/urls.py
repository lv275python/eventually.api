"""Root urls"""

from django.conf.urls import url, include
from event.views import EventView

urlpatterns = [
    url(r'^api/v1/user/', include('authentication.urls')),
    url(r'^api/v1/events/', include('event.urls', namespace='events')),
    # url(r'^api/v1/events/', EventView.as_view()),
    url(r'^api/v1/team/', include('team.urls')),
    url(r'^api/v1/img/', include('amazons3.urls')),
    url(r'^api/v1/chat/', include('chat.urls')),
    url(r'^api/v1/mentor/', include('mentor.urls')),
    url(r'^api/v1/events/', EventView.as_view()),
    url(r'.*', include('home.urls')),
]
