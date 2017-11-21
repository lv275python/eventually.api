from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LiteratureItemView.as_view())
]
