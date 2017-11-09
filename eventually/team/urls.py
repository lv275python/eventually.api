"""team URL Configuration
"""
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.TeamView.as_view()),
    url(r'^(?P<team_id>\d+)/$', views.TeamView.as_view()),
    url(r'^(?P<team_id>\d+)/event/', include('event.urls', namespace='event')),
    url(r'^(?P<team_id>\d+)/comment/', include('comment.urls')),

]
