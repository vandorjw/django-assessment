# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import QuestionSerializer
from assessment.models import Question


@api_view(['GET', ])
def retrieve_question(request, uuid):
    """
    """
    try:
        question = Question.objects.get(pk=uuid)
    except (Question.DoesNotExist, ValueError):
        response_data = {
            "error": {
                "state": "not found",
                "details": "Question object with ID {} could not be found.".format(uuid)
            }
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    if question.survey.is_private:
        if request.user.is_authenticated:
            if request.user == question.survey.admin or request.user in question.survey.users.all():
                serializer = QuestionSerializer(question, context={'request': request})
                response_data = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "This question is part of a private survey."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Please login."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = QuestionSerializer(question, context={'request': request})
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_question(request):
    """
    create a question for a survey
    """
    if request.user.is_authenticated:
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "please login"}, status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', ])
def update_question(request, uuid):
    """
    """
    if request.method == 'PUT':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def list_questions(request):
    """
    """
    if request.method == 'GET':
        response_data = {"details": "not implemented"}
        return Response(response_data, status=status.HTTP_200_OK)
