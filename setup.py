"""Setup script of django-assessment"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_packages

import assessment

setup(
    name='assessment',
    version=assessment.__version__,

    description='Django Assessment package',
    long_description='Django Assessment package',
    keywords='django, assessment, quiz',

    author=assessment.__author__,
    author_email=assessment.__email__,
    url=assessment.__url__,

    packages=find_packages(exclude=['docs']),
    classifiers=[
        'Framework :: Django',
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: Non-Free',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license=assessment.__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django==1.10.1',
        'djangorestframework==3.4.7',
        'Markdown==2.6.7',
        'django-filter==0.15.0',
        'django_parler==1.6.5',
        'django-parler-rest==1.4.2',
    ],
)
