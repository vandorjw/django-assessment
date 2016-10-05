# -*- coding: utf-8 -*-
from django.contrib import admin
from parler.admin import TranslatableAdmin
from assessment.models import (
    Choice,
    Profile,
    Question,
    Survey,
    SurveyAdmin,
    SurveyGroup,
)


@admin.register(Choice)
class ChoiceAdminConf(TranslatableAdmin):
    list_display = [
        'pk', 'question', 'value', 'is_correct',
    ]


@admin.register(Profile)
class ProfileAdminConf(admin.ModelAdmin):
    list_display = [
        'pk', 'user',
    ]


@admin.register(Question)
class QuestionAdminConf(TranslatableAdmin):
    list_display = [
        'pk', 'survey', 'question', 'of_type',
    ]



@admin.register(Survey)
class SurveyAdminConf(TranslatableAdmin):
    list_display = [
        'pk', 'name', 'slug', 'owner', 'is_active', 'start_date_time', 'end_date_time',
    ]


@admin.register(SurveyAdmin)
class SurveyAdminAdminConf(admin.ModelAdmin):
    list_display = [
        'pk', 'admin', 'survey',
    ]


@admin.register(SurveyGroup)
class SurveyGroupAdminConf(admin.ModelAdmin):
    list_display = [
        'pk', 'name', 'is_active',
    ]
