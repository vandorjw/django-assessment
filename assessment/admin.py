from django import forms
from django.contrib import admin
from assessment.models import Survey, SurveyGroup, Question, Choice, Result
from assessment.models import Profile


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        end_date_time = cleaned_data.get("end_date_time")
        start_date_time = cleaned_data.get("start_date_time")
        if end_date_time is not None:
            if end_date_time < start_date_time:
                raise forms.ValidationError(
                    "Publication Date: %(start_date_time)s, must not be AFTER the Due Date: %(end_date_time)s",
                    code='date_error',
                    params={'start_date_time': start_date_time,
                            'end_date_time': end_date_time, },
                )
        return cleaned_data


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_display = (
        'question',
        'survey',
        'of_type', )


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    inlines = [
        QuestionInline,
    ]
    prepopulated_fields = {'slug': ('name',), }
    list_display = (
        'name',
        'slug',
        'start_date_time',
        'end_date_time',
        'is_active', )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SurveyGroup)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Result)
