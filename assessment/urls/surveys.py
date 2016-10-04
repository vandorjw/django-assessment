# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views import surveys


urlpatterns = [
    url(
        regex=r'^$',
        view=surveys.list_surveys,
        name='surveys_list',
    ),
    url(
        regex=r'^create/$',
        view=surveys.create_surveys,
        name='surveys_create',
    ),
    url(
        regex=r'^update/(?P<slug>[-\w]+)/$',
        view=surveys.update_surveys,
        name='surveys_update',
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=surveys.retrieve_surveys,
        name='surveys_retrieve',
    ),
]