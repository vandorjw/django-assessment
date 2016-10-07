# -*- coding: utf-8 -*-
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
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        surveys = Survey.objects.filter(is_active=True)
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
