from django import forms
from django.contrib import admin
from assessment.models import Survey, SurveyGroup, Question, Choice
from assessment.models import Profile


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        due_date = cleaned_data.get("due_date")
        pub_date = cleaned_data.get("pub_date")
        if due_date is not None:
            if due_date < pub_date:
                raise forms.ValidationError(
                    "Publication Date: %(pub_date)s, must not be AFTER the Due Date: %(due_date)s",
                    code='date_error',
                    params={'pub_date': pub_date, 
                            'due_date': due_date, },
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
        'pub_date',
        'due_date',
        'is_active', )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SurveyGroup)
admin.site.register(Profile, ProfileAdmin)
