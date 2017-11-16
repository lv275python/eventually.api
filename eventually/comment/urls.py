"""Route rls."""

from django.conf.urls import url
from .views import CommentView

urlpatterns = [
    url(r'^$', CommentView.as_view()),
    url(r'^(?P<comment_id>\d+)$', CommentView.as_view()),
]
