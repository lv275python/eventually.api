from django.conf.urls import url, include
from .views import CurriculumView


urlpatterns = [
    url(r'^$', CurriculumView.as_view(), name='index'),
    url(r'^(?P<curriculum_id>\d+)/$', CurriculumView.as_view(), name='detail'),
    url(r'^(?P<curriculum_id>\d+)/topics/', include('topic.urls', namespace='topics')),
]
