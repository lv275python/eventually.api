# pylint: disable=missing-docstring
from django.conf.urls import url
from .views import get_all_topics_title

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^all_title/$', get_all_topics_title, name='all_title'),
]
