from django.contrib import admin
from assessment.models import Survey, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
