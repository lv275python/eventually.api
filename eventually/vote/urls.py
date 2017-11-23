from django.conf.urls import url, include
from .views import VoteView

urlpatterns = [
    url(r'^$', VoteView.as_view()),
    url(r'^(?P<vote_id>\d+)/$', VoteView.as_view()),
    url(r'^(?P<vote_id>\d+)/comment/', include('comment.urls', namespace='comment')),
]
