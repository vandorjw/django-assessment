# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views.api import survey


urlpatterns = [
    url(
        regex=r'^$',
        view=survey.list_surveys,
        name='list_surveys',
    ),
    url(
        regex=r'^create/$',
        view=survey.create_survey,
        name='create_survey',
    ),
    url(
        regex=r'^update/(?P<uuid>[-\w]+)/$',
        view=survey.update_survey,
        name='update_survey',
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=survey.retrieve_survey,
        name='retrieve_survey',
    ),
]
