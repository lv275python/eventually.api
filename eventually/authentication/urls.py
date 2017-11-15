from django.conf.urls import url
from .views import UserView, registration_user, login_user, logout_user, ForgetPassword

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', UserView.as_view()),
    url(r'^register/$', registration_user, name="add_user"),
    url(r'^login/$', login_user),
    url(r'^logout/$', logout_user),
    url(r'^forget_password/$', ForgetPassword.as_view()),
    url(r'^forget_password/(?P<token>.+)$', ForgetPassword.as_view())

]
