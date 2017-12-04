from django.conf.urls import url
from .views import ItemView

urlpatterns = [
    url(r'^$', ItemView.as_view())
]
