"""Defaults urls for the django-assessment project"""
from django.conf.urls import url
from django.conf.urls import include


urlpatterns = [
    url(r'^api/answer/', include('assessment.urls.answer')),
    url(r'^api/choice/', include('assessment.urls.choice')),
    url(r'^api/profile/', include('assessment.urls.profile')),
    url(r'^api/question/', include('assessment.urls.question')),
    url(r'^api/result/', include('assessment.urls.result')),
    url(r'^api/survey/', include('assessment.urls.survey')),
]