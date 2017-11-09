"""team URL Configuration
"""
from django.conf.urls import url, include
from .views import TeamView

urlpatterns = [
    url(r'^$', TeamView.as_view()),
    url(r'^(?P<team_id>\d+)/$', TeamView.as_view()),
    url(r'^(?P<team_id>\d+)/comment/', include('comment.urls')),
    url(r'^(?P<team_id>\d+)/event/', include('event.urls')),
]
