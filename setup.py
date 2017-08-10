"""Setup script of django-assessment"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_packages

import assessment

setup(
    name="django-assessment",
    version=assessment.__version__,

    description="Django Assessment package",
    long_description="Django Assessment package",
    keywords="django, assessment, quiz",

    author=assessment.__author__,
    author_email=assessment.__email__,
    url=assessment.__url__,

    packages=find_packages(exclude=("docs*", "tests*")),
    classifiers=[
        "Framework :: Django",
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license=assessment.__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        "Django>=1.8",
        "djangorestframework>=3.4",
        "Markdown>=2.6",
        "django-filter>=1.0",
        "django_parler>=1.8",
        "django-parler-rest>=1.4",
        "django-cors-headers>=2.0",
    ],
)
