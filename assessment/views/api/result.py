# -*- coding: utf-8 -*-
import logging
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
    if request.user.is_authenticated:
        results = Result.objects.filter(user=request.user)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    return Response({"details": "please log in"}, status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE', ])
def delete_result(request, uuid):
    """
    delete a single result if the request is from the result owner
    """

    if request.user.is_authenticated:
        try:
            result = Result.objects.get(pk=uuid, admin=request.user)
        except (Result.DoesNotExist, ValueError):
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            result.delete()
            return Response({"msg": f"Result {uuid} deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as error:
            logging.exception(error)
            return Response({"error": "Unable to delete result."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "please login"}, status.HTTP_401_UNAUTHORIZED)