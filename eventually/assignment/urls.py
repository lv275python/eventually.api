from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AssignmentAnswerView.as_view(), name='AssignmentAnswer')
]
