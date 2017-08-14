"""Defaults urls for the django-assessment project"""
from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(r'^api/', include('assessment.urls.api', namespace='api')),
]
