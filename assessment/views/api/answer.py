# -*- coding: utf-8 -*-
import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import AnswerSerializer
from assessment.models import Answer


@api_view(['GET', ])
def retrieve_answer(request, uuid):
    """
    """
    if request.method == 'GET':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_answer(request):
    """
    """
    if request.user.is_authenticated:
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as error:
                return Response("Valid but failed to save", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response({"error": "please login"}, status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', ])
def update_answer(request, uuid):
    """
    """
    if request.method == 'PUT':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def list_answers(request):
    """
    """
    if request.method == 'GET':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def filter_answers(request):
    """
    """
    if request.method == 'GET':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE', ])
def delete_answer(request, uuid):
    """
    delete a single answer if the request is from the answer owner
    """

    if request.user.is_authenticated:
        try:
            answer = Answer.objects.get(pk=uuid, admin=request.user)
        except (Answer.DoesNotExist, ValueError):
            return Response({"error": "Answer not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            answer.delete()
            return Response({"msg": f"Answer {uuid} deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as error:
            logging.exception(error)
            return Response({"error": "Unable to delete answer."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "please login"}, status.HTTP_401_UNAUTHORIZED)