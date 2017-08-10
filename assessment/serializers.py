# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
    _uid = serializers.UUIDField(label='ID', read_only=True)
    translations = TranslatedFieldsField(shared_model=Survey)
    question_set = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='assessment:api:retrieve_question',
        lookup_field='pk',
        lookup_url_kwarg='uuid',
    )
    class Meta:
        model = Survey
        fields = (
            '_uid',
            'is_active',
            'is_private',
            'start_date_time',
            'end_date_time',
            'admin',
            'users',
            'translations',
            'question_set',
        )


class QuestionSerializer(TranslatableModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    translations = TranslatedFieldsField(shared_model=Question)

    class Meta:
        model = Question
        fields = (
            '_uid',
            'survey',
            'of_type',
            'translations',
        )


class ChoiceSerializer(TranslatableModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    translations = TranslatedFieldsField(shared_model=Choice)

    class Meta:
        model = Choice
        fields = (
            '_uid',
            'question',
            'is_correct',
            'translations',
        )


class ResultSerializer(serializers.ModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    class Meta:
        model = Result
        fields = (
            '_uid',
            'survey',
            'user',
        )


class AnswerSerializer(serializers.ModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    class Meta:
        model = Answer
        fields = (
            '_uid',
            'result',
            'question',
            'answer',
        )
