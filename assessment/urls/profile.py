# -*- coding: utf-8 -*-
from django.conf.urls import url
from assessment.views import profile


urlpatterns = [
    url(
        regex=r'^$',
        view=profile.list_profiles,
        name='list_profiles',
    ),
    url(
        regex=r'^create/$',
        view=profile.create_profile,
        name='create_profile',
    ),
    url(
        regex=r'^update/(?P<uuid>[-\w]+)/$',
        view=profile.update_profile,
        name='update_profile',
    ),
    url(
        regex=r'^(?P<uuid>[-\w]+)/$',
        view=profile.retrieve_profile,
        name='retrieve_profile',
    ),
]
