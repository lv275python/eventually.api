"""team URL Configuration
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TeamView.as_view()),
    url(r'^(?P<team_id>\d+)/$', views.TeamView.as_view()),
]
