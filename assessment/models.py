import datetime
import uuid
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from assessment.managers import SurveyManager


class Survey(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    name = models.CharField(
        max_length=160
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    description = models.TextField()
    start_date_time = models.DateTimeField(
        auto_now=False,
        default=datetime.datetime.now,
    )
    end_date_time = models.DateTimeField(
        auto_now=False,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assessment_surveys",
    )

    objects = models.Manager()
    surveys = SurveyManager()

    class Meta:
        app_label = 'assessment'
        ordering = ['is_active', 'start_date_time']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assessment:survey_do',
                       kwargs={'slug': self.slug})


class SurveyAdmin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    survey = models.ForeignKey(
        Survey,
    )

    class Meta:
        app_label = 'assessment'

    def __str__(self):
        return "{user_name} is admin on: {survey_name}".format(
            user_name=self.admin.username,
            survey_name=self.survey.name,
        )


class SurveyGroup(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    name = models.CharField(
        max_length=160,
    )
    surveys = models.ManyToManyField(
        Survey,
        related_name='surveygroups',
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        app_label = 'assessment'
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="assessment_profile",
    )
    surveys = models.ManyToManyField(
        Survey,
        related_name='profile_surveys',
        blank=True,
    )
    survey_groups = models.ManyToManyField(
        SurveyGroup,
        related_name='profile_surveygroups',
        blank=True,
    )

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('assessment:profile_detail',
                       kwargs={'id': self.id})


class Question(models.Model):
    TRUEFALSE = 1
    MULTICHOICE = 2
    TEXT = 3

    QUESTION_TYPE = (
        (TRUEFALSE, 'True or False'),
        (MULTICHOICE, 'Multiple Choice'),
        (TEXT, 'Text'),
    )
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    survey = models.ForeignKey(Survey)
    question = models.CharField(max_length=255)
    of_type = models.IntegerField(
        choices=QUESTION_TYPE,
        default=TRUEFALSE,
    )

    class Meta:
        app_label = 'assessment'
        ordering = ['survey', 'id']

    def __str__(self):
        return self.question


class Choice(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    question = models.ForeignKey(Question, related_name='choices')
    choice_value = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        app_label = 'assessment'
        ordering = ['id']

    def __str__(self):
        return self.choice_value


class Result(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    survey = models.ForeignKey(
        Survey,
        related_name='results',
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='results',
        editable=False,
    )
    completed_on = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        app_label = 'assessment'
        unique_together = ('survey', 'user')

    def __str__(self):
        return "%s, %s" % (self.survey, self.user)

    def get_absolute_url(self):
        return reverse('assessment:result_detail',
                       kwargs={'id': self.id})

    def score(self):
        if self.completed_on:
            return 0
        else:
            return 0

    def score_percentage(self):
        if self.completed_on:
            return "{percentage} %".format(percentage=0)
        else:
            return "{percentage} %".format(percentage=0)


class Answer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    result = models.ForeignKey(
        Result,
        related_name='answers',
        editable=False,
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        editable=False,
    )
    answer = models.TextField()

    class Meta:
        app_label = 'assessment'
        unique_together = ('result', 'question')

    def __str__(self):
        return "{}".format(str(self.answer))
