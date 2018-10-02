# -*- coding: utf-8 -*-
import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from assessment.serializers import ChoiceSerializer
from assessment.models import Choice


@api_view(['GET', ])
def retrieve_choice(request, uuid):
    """
    """
    if request.method == 'GET':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_choice(request):
    """
    """
    if request.method == 'POST':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT', ])
def update_choice(request, uuid):
    """
    """
    if request.method == 'PUT':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def list_choices(request):
    """
    """
    if request.method == 'GET':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE', ])
def delete_choice(request, uuid):
    """
    delete a single choice if the request is from the choice owner
    """

    if request.user.is_authenticated:
        try:
            choice = Choice.objects.get(pk=uuid, admin=request.user)
        except (Choice.DoesNotExist, ValueError):
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            choice.delete()
            return Response({"msg": f"Choice {uuid} deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as error:
            logging.exception(error)
            return Response({"error": "Unable to delete choice."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "please login"}, status.HTTP_401_UNAUTHORIZED)