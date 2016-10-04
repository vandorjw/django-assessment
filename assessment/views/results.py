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
def retrieve_results(request, uuid):
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


@api_view(['GET', ])
def list_results(request):
    """
    """
    if request.method == 'GET':
        if request.user.is_staff:
            results = Result.objects.all()
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)
        else:
            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                return Response({"error": "user not found"}, status.HTTP_404_NOT_FOUND)
            results = Result.objects.filter(user=user)
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET', ])
def filter_results(request):
    """

    """
    if request.method == 'GET':
        filters = []
        survey = request.GET.get('survey', None)
        username = request.GET.get('username', None)

        if request.user.is_staff or request.user.username == username:
            pass
        elif username is None:
            username = request.user.username
        else:
            return Response({"error": "un-authorized"}, status.HTTP_401_UNAUTHORIZED)

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "user not found"}, status.HTTP_404_NOT_FOUND)
            filters.append(Q(user=user))

        if survey:
            try:
                survey = Survey.objects.get(slug=survey)
            except Survey.DoesNotExist:
                return Response({"error": "survey not found"}, status.HTTP_404_NOT_FOUND)
            filters.append(Q(survey=survey))

        results_by_filters = Result.objects.filter(*filters)
        serializer = ResultSerializer(results_by_filters, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
