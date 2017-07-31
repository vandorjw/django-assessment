# -*- coding: utf-8 -*-
import logging
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import SurveySerializer
from assessment.models import Survey
from assessment.models import Profile

logger = logging.getLogger(__name__)


@api_view(['POST', ])
def create_survey(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status.HTTP_404_NOT_FOUND)

        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
def update_survey(request, slug):
    """
    """
    if request.method == 'PUT':
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            survey = Survey.objects.get(slug=slug)
        except Survey.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user.is_staff or user is survey.owner or user in [sa.admin for sa in survey.surveyadmin_set.all()]:
            serializer = SurveySerializer(survey, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "un-authorized"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
def retrieve_survey(request, slug):
    """
    """
    if request.method == 'GET':
        try:
            result = Survey.objects.get(slug=slug)
        except Survey.DoesNotExist:
            return Response({"error": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SurveySerializer(result)
        return Response(serializer.data)


@api_view(['GET', ])
def list_surveys(request):
    """
    return available surveys, via assigned and assigned groups.
    Mark surveys as:
        completed
        in progress
        available
        expired
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except (Profile.DoesNotExist, Exception) as error:
        profile = None
        logger.error(error)
    if profile:
        private_surveys = profile.surveys.all()
        private_group_surveys = profile.survey_groups.filter()
        public_surveys = Survey.objects.filter(is_private=False)
        surveys = private_surveys + private_group_surveys + public_surveys
    else:
        surveys = Survey.objects.filter(is_private=False)
    serializer = SurveySerializer(surveys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
