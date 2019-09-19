"""Defaults urls for the django-assessment project"""
from django.conf.urls import url
from django.conf.urls import include
from assessment.views.version import details


urlpatterns = [
    url(
        regex=r'^version/$',
        view=details,
        name='get_version',
    ),
    url(r'^api/', include(('assessment.urls.api', 'assessment-api'), namespace='assessment-api')),
]
