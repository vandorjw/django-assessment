from rest_framework import serializers
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


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = (
            'name',
            'slug',
            'is_active',
            'description',
            'start_date_time',
            'end_date_time',
            'owner',

)


class SurveyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAdmin
        fields = (
            'admin',
            'survey',
        )


class SurveyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyGroup
        fields = (
            'name',
            'surveys',
            'is_active',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'user',
            'surveys',
            'survey_groups',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'survey',
            'question',
            'of_type',
        )


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'question',
            'choice_value',
            'is_correct',
        )


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            'survey',
            'user',
            'completed_on',
        )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'result',
            'question',
            'answer',
        )
