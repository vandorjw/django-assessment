import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from assessment.managers import SurveyManager


@python_2_unicode_compatible
class Survey(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    pub_date = models.DateTimeField(
        auto_now=False, default=datetime.datetime.now)
    due_date = models.DateTimeField(
        auto_now=False, default=datetime.datetime.now)
    visible_for = models.ManyToManyField(
        Group,
        blank=True,
        null=True,
        help_text="When no groups are assigned"
                  " the survey will be available to all users."
     )

    objects = models.Manager()
    surveys = SurveyManager()

    class Meta:
        app_label = 'assessment'
        ordering = ['pub_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assessment:survey_do',
                       kwargs={'slug': self.slug})


@python_2_unicode_compatible
class Question(models.Model):
    TRUEFALSE = 1
    MULTICHOICE = 2
    TEXT = 3

    QUESTION_TYPE = (
        (TRUEFALSE, 'True or False'),
        (MULTICHOICE, 'Multiple Choice'),
        (TEXT, 'Text'),
    )

    survey = models.ForeignKey(Survey)
    question = models.CharField(max_length=255)
    of_type = models.IntegerField(
        max_length=1,
        choices=QUESTION_TYPE,
        default=TRUEFALSE)

    class Meta:
        app_label = 'assessment'
        ordering = ['survey', 'id']

    def __str__(self):
        return self.question


@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    choice_value = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        app_label = 'assessment'
        ordering = ['id']

    def __str__(self):
        return self.choice_value


@python_2_unicode_compatible
class Result(models.Model):
    survey = models.ForeignKey(
        Survey, related_name='results', editable=False)
    user = models.ForeignKey(
        User, related_name='results', editable=False)
    completed_on = models.DateTimeField(
        auto_now=True, default=datetime.datetime.now)
    score = models.CharField(
        max_length=10, default=0, editable=False)
    score_percentage = models.PositiveIntegerField(
        max_length=3, default=0, editable=False)

    class Meta:
        app_label = 'assessment'
        unique_together = ('survey', 'user')

    def __str__(self):
        return "%s, %s" % (self.survey, self.user)

    def get_absolute_url(self):
        return reverse('assessment:survey_result',
                       kwargs={'pk': self.id})


@python_2_unicode_compatible
class Answer(models.Model):
    result = models.ForeignKey(
        Result, related_name='answers', editable=False)
    question = models.ForeignKey(
        Question, related_name='answers', editable=False)
    answer = models.TextField()

    class Meta:
        app_label = 'assessment'
        unique_together = ('result', 'question')

    def __str__(self):
        return "%s" % (self.answer)
