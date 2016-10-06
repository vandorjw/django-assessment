# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views.api import question


urlpatterns = [
    url(
        regex=r'^$',
        view=question.list_questions,
        name='list_questions',
    ),
    url(
        regex=r'^create/$',
        view=question.create_question,
        name='create_question',
    ),
    url(
        regex=r'^update/(?P<uuid>[-\w]+)/$',
        view=question.update_question,
        name='update_question',
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=question.retrieve_question,
        name='retrieve_question',
    ),
]
