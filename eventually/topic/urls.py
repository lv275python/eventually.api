from django.conf.urls import url, include
from .views import TopicView, is_topic_mentor

urlpatterns = [
    url(r'^$', TopicView.as_view(), name='index'),
    url(r'^(?P<topic_id>\d+)/$', TopicView.as_view(), name='detail'),
    url(r'^(?P<topic_id>\d+)/items/', include('item.urls', namespace='items')),
    url(r'^(?P<topic_id>\d+)/is_mentor/$', is_topic_mentor, name='is_topic_mentor'),
]
