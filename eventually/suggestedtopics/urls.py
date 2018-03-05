from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SuggestedTopicsView.as_view(), name='suggested_topics'),
    url(r'^(?P<suggested_topic_id>\d+)/$', views.SuggestedTopicsView.as_view())
]
