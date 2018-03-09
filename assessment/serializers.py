# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
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
    text = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='assessment-api:retrieve_question',
        lookup_field='pk',
        lookup_url_kwarg='uuid',
    )

    class Meta:
        model = Question
        fields = (
            '_uid',
            'survey',
            'result',
            'of_type',
            'translations',
            'url',
            'text',
        )

    def get_result(self, obj):
        try:
            user = self.context.get('request').user
        except Exception:
            return None

        if user.id is None:
            return None

        try:
            result = Result.objects.get(survey=obj.survey, user=user)
        except Result.DoesNotExist:
            return None
        else:
            return str(result.pk)

    def get_text(self, obj):
        try:
            return obj.question
        except ObjectDoesNotExist:
            return _("Translation does not exist for your current language.")


class SurveySerializer(TranslatableModelSerializer):
    _uid = serializers.UUIDField(label='ID', read_only=True)
    translations = TranslatedFieldsField(shared_model=Survey)
    questions = QuestionSerializer(many=True, read_only=True)
    is_admin = serializers.SerializerMethodField()
    in_users = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Survey
        fields = (
            '_uid',
            'is_active',
            'is_private',
            'start_date_time',
            'end_date_time',
            'translations',
            'questions',
            'is_admin',
            'in_users',
            'result',
            'name',
            'description',
        )

    def get_result(self, obj):
        """
        When an authenticated user request survey details,
        it should include if the survey has been started, completed, etc.
        """
        try:
            user = self.context.get('request').user
        except Exception:
            return {
                "status": "error",
                "result_id": None
            }

        if user.id is None:
            return {
                "status": "anonymous",
                "result_id": None
            }

        try:
            result = Result.objects.get(survey=obj, user=user)
        except Result.DoesNotExist:
            return {
                "status": "unstarted",
                "result_id": None
            }

        if result.answers.count() == obj.questions.count():
            return {
                "status": "complete",
                "result_id": str(result.pk)
            }
        else:
            return {
                "status": "incomplete",
                "result_id": str(result.pk)
            }

    def get_is_admin(self, obj):
        """
        The application should never directly report who the admin is.
        This method reports if the current authenticated user is the admin.
        """
        try:
            user = self.context.get('request').user
        except Exception:
            # raise serializers.ValidationError('Could not access request.user')
            return False
        if user == obj.admin:
            return True
        else:
            return False

    def get_in_users(self, obj):
        """
        The application should never directly report the entire user group.
        This method reports if the current authenticated user is users.
        """
        try:
            user = self.context.get('request').user
        except Exception:
            # raise serializers.ValidationError('Could not access request.user')
            return False
        if user in obj.users.all():
            return True
        else:
            return False

    def get_name(self, obj):
        try:
            return obj.name
        except ObjectDoesNotExist:
            return str(obj.pk)

    def get_description(self, obj):
        try:
            return obj.description
        except ObjectDoesNotExist:
            return str(obj.pk)


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
