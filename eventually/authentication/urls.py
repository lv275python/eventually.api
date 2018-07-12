from django.conf.urls import url
from .views import (UserView,
                    registration,
                    activate,
                    login_user,
                    logout_user,
                    ForgetPassword,
                    get_all_users,
                    change_password)
from customprofile.views import CustomProfileView

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', UserView.as_view(), name="manage_user"),
    url(r'^register/$', registration, name='register'),
    url(r'^activate/(?P<token>.+)$', activate, name='activate'),
    url(r'^login/$', login_user, name="login_user"),
    url(r'^logout/$', logout_user, name="logout_user"),
    url(r'^forget_password/$', ForgetPassword.as_view(), name="forget_password"),
    url(r'^forget_password/(?P<token>.+)$', ForgetPassword.as_view(), name="forget_password_token"),
    url(r'^(?P<user_id>[0-9]+)/profile/$', CustomProfileView.as_view(), name='profile'),
    url(r'^(?P<user_id>[0-9]+)/change_password/$', change_password, name='change_password'),
    url(r'^profile/$', CustomProfileView.as_view(), name='profile_del'),
    url(r'^all/$', get_all_users, name='all_users')
]
