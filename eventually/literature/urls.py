from django.conf.urls import url
from .views import LiteratureItemView

urlpatterns = [
    url(r'^$', LiteratureItemView.as_view(), name='literature'),
    url(r'^(?P<literature_id>\d+)/$', LiteratureItemView.as_view(), name='literature_details'),
]
