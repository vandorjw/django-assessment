"""Defaults urls for the django-assessment project"""
from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(r'^api/results/', include('assessment.urls.results')),
    url(r'^api/surveys/', include('assessment.urls.surveys')),
]