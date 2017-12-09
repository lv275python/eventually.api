from django.conf.urls import url
from .views import TopicView

urlpatterns = [
    url(r'^$', TopicView.as_view())
]
