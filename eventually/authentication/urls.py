from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', UserView.as_view()),
    url(r'^register/$', registration_user, name="add_user")
]
