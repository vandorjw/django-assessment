# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views.api import choice


urlpatterns = [
    url(
        regex=r'^$',
        view=choice.list_choices,
        name='list_choices',
    ),
    url(
        regex=r'^create/$',
        view=choice.create_choice,
        name='create_choice',
    ),
    url(
        regex=r'^update/(?P<uuid>[-\w]+)/$',
        view=choice.update_choice,
        name='update_choice',
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=choice.retrieve_choice,
        name='retrieve_choice',
    ),
]
