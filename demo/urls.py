"""Urls for the demo of django-assessment"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include

from django.views.static import serve
from django.views.defaults import bad_request
from django.views.defaults import server_error
from django.views.defaults import page_not_found
from django.views.defaults import permission_denied

from rest_framework.authtoken import views as authtoken_views


urlpatterns = [
    url(r'^', include('assessment.urls', namespace='assessment')),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
]

urlpatterns += [
    url(r'^400/$', bad_request),
    url(r'^403/$', permission_denied),
    url(r'^404/$', page_not_found),
    url(r'^500/$', server_error),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT})
]
