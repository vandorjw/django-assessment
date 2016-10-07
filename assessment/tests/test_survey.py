# -*- coding: utf-8 -*-
import datetime
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from assessment.models import Survey
from assessment.models import Profile


class SurveyTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='top_secret')
        Profile.objects.create(user=self.admin)
        self.client.login(username='admin', password='top_secret')

    def test_create_survey(self):
        """
        Ensure we can create a new survey object.
        """
        url = reverse('assessment:api:create_survey')
        data = {
            "translations": {
                "de": {
                    "name": "Hallo Welt",
                    "slug": "hallo-welt",
                    "description": "Wie sage ich; 'Hello World', auf Deutsch?",
                },
                "en": {
                    "name": "Hello World",
                    "slug": "hello-world",
                    "description": "How do I say; 'Hello world', in English?",
                },
                "nl": {
                    "name": "Hallo Wereld",
                    "slug": "hallo-wereld",
                    "description": "Hoe zeg ik; 'Hello World', in Nederlandse?",
                }
            },
            'is_active': True,
            'start_date_time': datetime.datetime.now(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 1)
        self.assertEqual(Survey.objects.get().name, 'Hello World')

    def test_getlist(self):
        response = self.client.get(reverse('assessment:api:list_surveys'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)