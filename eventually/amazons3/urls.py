from django.conf.urls import url
from amazons3.views import ImageManagement, PracticalAssignmentManagement

urlpatterns = [
    url(r'^img_handle/$', ImageManagement.as_view(), name='handle_image'),
    url(r'^doc_handle/$', PracticalAssignmentManagement.as_view(), name='handle_practical_assignment')
]
