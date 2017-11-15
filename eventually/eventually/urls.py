"""Root urls"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/user/', include('authentication.urls')),
    url(r'^api/v1/team/', include('team.urls'))
]
