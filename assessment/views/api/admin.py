# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', ])
def noop(request):
    """
    """
    if request.method == 'GET':
        if request.user.is_staff:
            response_data = {"details": "Hello world"}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {"details": "Goodbye world"}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
