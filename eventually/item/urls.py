from django.conf.urls import url, include
from .views import ItemView

urlpatterns = [
    url(r'^(?P<item_id>\d+)/literature/', include('literature.urls', namespace='literature'))
]
