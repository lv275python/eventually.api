from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.VoteView.as_view()),
    url(r'^(?P<vote_id>\d+)/$', views.VoteView.as_view()),
]
