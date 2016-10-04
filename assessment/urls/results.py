# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views import results


urlpatterns = [
    url(
        regex=r'^$',
        view=results.list_results,
        name='results_list'
    ),
    url(
        regex=r'^filter/$',
        view=results.filter_results,
        name='results_filter'
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=results.retrieve_results,
        name='results_retrieve'
    ),
]