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


class AccountTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='top_secret')
        self.client.login(username='admin', password='top_secret')

    def test_create_survey(self):
        """
        Ensure we can create a new survey object.
        """
        url = reverse('assessment:surveys_create')
        data = {
            'name': 'Test Survey 1',
            'slug': 'test-survey-1',
            'is_active': True,
            'description': 'Test description',
            'start_date_time': datetime.datetime.now(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 1)
        self.assertEqual(Survey.objects.get().name, 'Test Survey 1')