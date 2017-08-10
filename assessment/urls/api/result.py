# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views.api import result


urlpatterns = [
    url(
        regex=r'^$',
        view=result.list_results,
        name='list_results',
    ),
    url(
        regex=r'^create/$',
        view=result.create_result,
        name='create_result',
    ),
    url(
        regex=r'^update/(?P<uuid>[-\w]+)/$',
        view=result.update_result,
        name='update_result',
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=result.retrieve_result,
        name='retrieve_result',
    ),
]
