"""Route rls."""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CommentView.as_view()),
    url(r'^(?P<comment_id>[0-9]+)$', views.CommentView.as_view()),
]
