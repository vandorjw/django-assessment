# -*- coding: utf-8 -*-
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


class QuestionSerializer(TranslatableModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    translations = TranslatedFieldsField(shared_model=Question)
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='assessment:api:retrieve_question',
        lookup_field='pk',
        lookup_url_kwarg='uuid',
    )

    class Meta:
        model = Question
        fields = (
            '_uid',
            'survey',
            'of_type',
            'translations',
            'url',
        )


class SurveySerializer(TranslatableModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    translations = TranslatedFieldsField(shared_model=Survey)
    questions = QuestionSerializer(many=True, read_only=True)

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
            'questions',
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

    def validate(self, attrs):
        instance = Result(**attrs)
        instance.clean()
        return attrs


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

    def validate(self, attrs):
        instance = Answer(**attrs)
        instance.clean()
        return attrs

    def validate_result(self, result):
        try:
            user = self.context.get('request').user
        except Exception:
            raise serializers.ValidationError('Could not access request.user')

        if not result.user == user:
            raise serializers.ValidationError('result does not belong to current user!')
        else:
            return result
