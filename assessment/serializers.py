from rest_framework import serializers
from parler_rest.serializers import (
    TranslatableModelSerializer,
    TranslatedFieldsField,
)
from assessment.models import (
    Survey,
    Question,
    Choice,
    Result,
    Answer,
)


class SurveySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Survey)
    class Meta:
        model = Survey
        fields = (
            'is_active',
            'is_private',
            'start_date_time',
            'end_date_time',
            'admin',
            'users',
            'translations',
        )


class QuestionSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Question)

    class Meta:
        model = Question
        fields = (
            'survey',
            'of_type',
            'translations',
        )


class ChoiceSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Choice)

    class Meta:
        model = Choice
        fields = (
            'question',
            'is_correct',
            'translations',
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
