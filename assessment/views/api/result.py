# -*- coding: utf-8 -*-
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import ResultSerializer
from assessment.models import Result
from assessment.models import Survey


@api_view(['GET', ])
def retrieve_result(request, uuid):
    """
    """
    if request.method == 'GET':
        try:
            result = Result.objects.get(pk=uuid)
        except Result.DoesNotExist:
            return Response({"error": "result not found"}, status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == result.user:
            pass
        else:
            return Response({"error": "un-authorized"}, status.HTTP_401_UNAUTHORIZED)

        serializer = ResultSerializer(result)
        return Response(serializer.data)


@api_view(['POST', ])
def create_result(request):
    """
    """
    if request.method == 'POST':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT', ])
def update_result(request, uuid):
    """
    """
    if request.method == 'PUT':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def list_results(request):
    """
    Generate a list of all survey results for the authenticated user.
    If there is no authenticated user, return 401 UNAUTHORIZED.
    """
    if request.method == 'GET':
        if request.user.is_authenticated():
            results = Result.objects.filter(user=request.user)
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"details": "unauthorized"}, status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
def filter_results(request):
    """

    """
    if request.method == 'GET':
        if request.user.is_authenticated():
            filters = [Q(user=request.user)]
            survey = request.GET.get('survey', None)

            if survey:
                try:
                    survey = Survey.objects.get(slug=survey)
                except Survey.DoesNotExist:
                    return Response({"error": "survey not found"}, status.HTTP_404_NOT_FOUND)
                else:
                    filters.append(Q(survey=survey))

            results_by_filters = Result.objects.filter(*filters)
            serializer = ResultSerializer(results_by_filters, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"details": "unauthorized"}, status.HTTP_401_UNAUTHORIZED)
