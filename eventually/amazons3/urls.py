from django.conf.urls import url
from amazons3.views import ImageManagement

urlpatterns = [
    url(r'^handle/$', ImageManagement.as_view(), name='handle_image'),
]
