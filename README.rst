django-assessment
=================

A django vote application which allows users to answer surveys.

To use it in your project:

    pip install git+https://github.com/vandorjw/django-assessment

Add 'assessment' to your installed_applications

    INSTALLED_APPS = (
        ...
        'braces',
        'assessment',
        ...
    )

Modify your urls.py file to inlude

    urlpatterns = patterns(
        '',
        ...
        url(
            regex=r'^assessment/',
            include(module = 'assessment.urls',
                    namespace = 'assessment',
                    app_name = 'assessment', )
            ),
        ...
    )

# Requirements

 - Python 3.4
 - Django 1.5+
