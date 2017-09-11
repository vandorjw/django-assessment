# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import SurveySerializer
from assessment.models import Survey


@api_view(['POST', ])
def create_survey(request):
    if request.user.is_authenticated:
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "please login"}, status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', ])
def update_survey(request, uuid):
    """
    """
    if request.user.is_authenticated:
        try:
            survey = Survey.objects.get(pk=uuid)
        except Survey.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user == survey.admin:
            serializer = SurveySerializer(survey, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "un-authorized"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
def retrieve_survey(request, uuid):
    """
    return a single survey.
    """
    try:
        result = Survey.objects.get(pk=uuid)
    except (Survey.DoesNotExist, ValueError):
        return Response({"error": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

    if result.is_private:
        if request.user.is_authenticated:
            if request.user == result.admin or request.user in result.users.all():
                serializer = SurveySerializer(result, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({"error": "This is a private survey."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Please login."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = SurveySerializer(result, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', ])
def list_surveys(request):
    """
    return a list of surveys.
    """
    if request.user.is_authenticated:
        public_surveys = Q(is_private=False)
        private_surveys = Q(is_private=True, pk__in=request.user.assessment_user_surveys.all())
        admin_surveys = Q(admin=request.user)
        surveys = Survey.objects.filter(public_surveys | private_surveys | admin_surveys)
    else:
        surveys = Survey.objects.filter(is_private=False)
    serializer = SurveySerializer(surveys, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
