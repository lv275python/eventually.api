from django.conf.urls import url
from .views import UserView, registration, activate, login_user, logout_user, ForgetPassword

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', UserView.as_view()),
    url(r'^register/$', registration),
    url(r'^activate/(?P<token>.+)$', activate),
    url(r'^login/$', login_user),
    url(r'^logout/$', logout_user),
    url(r'^forget_password/$', ForgetPassword.as_view()),
    url(r'^forget_password/(?P<token>.+)$', ForgetPassword.as_view())

]
