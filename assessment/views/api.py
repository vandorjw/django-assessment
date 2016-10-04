from rest_framework import viewsets
from assessment.models import (
    Survey,
    SurveyAdmin,
    SurveyGroup,
    Profile,
    Question,
    Choice,
    Result,
    Answer,
)
from assessment.serializers import (
    SurveySerializer,
    SurveyAdminSerializer,
    SurveyGroupSerializer,
    ProfileSerializer,
    QuestionSerializer,
    ChoiceSerializer,
    ResultSerializer,
    AnswerSerializer,
)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyAdminViewSet(viewsets.ModelViewSet):
    queryset = SurveyAdmin.objects.all()
    serializer_class = SurveyAdminSerializer


class SurveyGroupViewSet(viewsets.ModelViewSet):
    queryset = SurveyGroup.objects.all()
    serializer_class = SurveyGroupSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
