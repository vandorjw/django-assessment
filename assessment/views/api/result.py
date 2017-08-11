# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import ResultSerializer
from assessment.models import Result


@api_view(['GET', ])
def retrieve_result(request, uuid):
    if request.user.is_authenticated:
        try:
            result = Result.objects.get(pk=uuid)
        except Result.DoesNotExist:
            return Response({"error": "result not found"}, status.HTTP_404_NOT_FOUND)

        if request.user == result.user or request.user == result.survey.admin:
            serializer = ResultSerializer(result)
            return Response(serializer.data)
        else:
            return Response({"error": "un-authorized"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"error": "please log in"}, status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
def create_result(request):
    """
    API endpoint to respond to a survery.
    """
    if request.user.is_authenticated:
        request.data['user'] = request.user.pk
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "please log in"}, status.HTTP_401_UNAUTHORIZED)


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
    if request.user.is_authenticated():
        results = Result.objects.filter(user=request.user)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    return Response({"details": "please log in"}, status.HTTP_401_UNAUTHORIZED)
