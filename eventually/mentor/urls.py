from django.conf.urls import url
from .views import MentorView

urlpatterns = [
    url(r'^students/$', MentorView.as_view())
]
