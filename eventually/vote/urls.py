from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^(?P<vote_id>\d+)/comment/', include('comment.urls', namespace='comment')),
    url(r'^$', views.VoteView.as_view(), name='index'),
    url(r'^(?P<vote_id>\d+)/$', views.VoteView.as_view(), name='detail'),

    url(r'^(?P<vote_id>\d+)/answer/$', views.AnswerView.as_view(), name='answer'),
    url(r'^(?P<vote_id>\d+)/answer/(?P<answer_id>\d+)/$', views.AnswerView.as_view(), name='answer_detail'),
]
