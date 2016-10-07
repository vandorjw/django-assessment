# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ChoiceTests(APITestCase):
    def test_getlist(self):
        response = self.client.get(reverse('assessment:api:list_choices'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
