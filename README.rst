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
            r'^assessment/',
            include('assessment.urls',
                    namespace = 'assessment',
                    app_name = 'assessment', )
            ),
        ...
    )

# Requirements

 - Python 3+
 - django-braces
 - Django 1.5+
