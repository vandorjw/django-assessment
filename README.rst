django-assessment
=================

A django vote application which allows users to answer surveys.

To use it, clone this repository as 'assessment'.

Add 'assessment' to your installed_applications

    INSTALLED_APPS = (
        ...
        'assessment',
        ...
    )

Modify your urls.py file to inlude

    urlpatterns = patterns(
        '',
        ...
        url(r'^assessment/', include('assessment.urls', namespace='assessment', app_name='assessment')),
        ...
    )

# Requirements

 - Python3
 - Django 1.5+
