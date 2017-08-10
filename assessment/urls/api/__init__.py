"""API urls for the django-assessment project"""
from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(r'^answer/', include('assessment.urls.api.answer')),
    url(r'^choice/', include('assessment.urls.api.choice')),
    url(r'^question/', include('assessment.urls.api.question')),
    url(r'^result/', include('assessment.urls.api.result')),
    url(r'^survey/', include('assessment.urls.api.survey')),
]
