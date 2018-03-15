from django.conf.urls import url, include
from .views import ItemView

urlpatterns = [
    url(r'^$', ItemView.as_view(), name="index"),
    url(r'^(?P<item_id>\d+)/$', ItemView.as_view(), name="detail"),
    url(r'^(?P<item_id>\d+)/delete/$', ItemView.as_view(), name="delete"),
    url(r'^(?P<item_id>\d+)/literature/', include('literature.urls', namespace='literature'))
]
