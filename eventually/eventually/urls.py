"""Root urls"""

from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/user/', include('authentication.urls')),
    url(r'^api/v1/events/', include('event.urls', namespace='events')),
    url(r'^api/v1/team/', include('team.urls')),
    url(r'^api/v1/upload/', include('amazons3.urls')),
    url(r'^api/v1/chat/', include('chat.urls')),
    url(r'^api/v1/mentor/', include('mentor.urls', namespace='mentor')),
    url(r'^api/v1/curriculums/', include('curriculum.urls', namespace='curriculums')),
    url(r'^api/v1/literature/', include('literature.urls')),
    url(r'^api/v1/item/', include('item.urls', namespace='item')),
    url(r'^api/v1/assignment/', include('assignment.urls', namespace='assignment')),
    url(r'^api/v1/suggestedtopics/', include('suggestedtopics.urls')),
    url(r'^api/v1/topic/', include('topic.urlshelp')),
    url(r'.*', include('home.urls')),
]
