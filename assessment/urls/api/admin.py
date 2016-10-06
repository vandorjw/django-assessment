# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views.api import admin


urlpatterns = [
    url(
        regex=r'^$',
        view=admin.noop,
        name='noop_admin',
    )
]
