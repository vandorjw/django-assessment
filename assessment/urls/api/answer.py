# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views.api import answer


urlpatterns = [
    url(
        regex=r'^$',
        view=answer.list_answers,
        name='list_answers',
    ),
    url(
        regex=r'^create/$',
        view=answer.create_answer,
        name='create_answer',
    ),
    url(
        regex=r'^update/(?P<uuid>[-\w]+)/$',
        view=answer.update_answer,
        name='update_answer',
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=answer.retrieve_answer,
        name='retrieve_answer',
    ),
]
