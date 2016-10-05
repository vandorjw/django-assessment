# -*- coding: utf-8 -*-
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessment.serializers import QuestionSerializer
from assessment.models import Question


@api_view(['GET', ])
def retrieve_question(request, uuid):
    """
    """
    if request.method == 'GET':
        try:
            result = Question.objects.get(pk=uuid)
        except Question.DoesNotExist:
            return Response({"error": "result not found"}, status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == result.user:
            pass
        else:
            return Response({"error": "un-authorized"}, status.HTTP_401_UNAUTHORIZED)

        serializer = QuestionSerializer(result)
        return Response(serializer.data)
