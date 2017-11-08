from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CustomProfileView.as_view()),
    url(r'^(?P<profile_id>\d+)/$', views.CustomProfileView.as_view()),
]
