from django.conf.urls import url
from .views import ChatView
from .views import OnlineStatusView

urlpatterns = [
    url(r'^(?P<receiver_id>\d+)/$', ChatView.as_view()),
    url(r'^(?P<receiver_id>\d+)/(?P<page_number>\d+)/$', ChatView.as_view()),
    url(r'^online/$', OnlineStatusView.as_view())
]
