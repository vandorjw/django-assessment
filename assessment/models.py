import datetime
from uuid import uuid4
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from assessment.managers import SurveyManager


class Survey(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    pub_date = models.DateTimeField(
        auto_now=False, default=datetime.datetime.now)
    due_date = models.DateTimeField(
        auto_now=False, null=True, blank=True)

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


class SurveyGroup(models.Model):
    name = models.CharField(max_length=254)
    surveys = models.ManyToManyField(Survey, related_name='surveygroups', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'assessment'
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile")
    surveys = models.ManyToManyField(
        Survey, related_name='profile_surveys', null=True, blank=True)
    surveygroups = models.ManyToManyField(
        SurveyGroup, related_name='profile_surveygroups', null=True, blank=True)
    uuid = models.CharField(
        max_length=36, editable=False, unique=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('assessment:profile_detail',
                       kwargs={'uuid': self.uuid})

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if not self.uuid:
            self.uuid = str(uuid4())
            super(Profile, self).save(*args, **kwargs)


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


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    choice_value = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        app_label = 'assessment'
        ordering = ['id']

    def __str__(self):
        return self.choice_value


class Result(models.Model):
    survey = models.ForeignKey(
        Survey, related_name='results', editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='results', editable=False)
    completed_on = models.DateTimeField(
        auto_now=True, default=datetime.datetime.now)
    score = models.CharField(
        max_length=10, default=0, editable=False)
    score_percentage = models.PositiveIntegerField(
        max_length=3, default=0, editable=False)
    uuid = models.CharField(
        max_length=36, editable=False, unique=True, blank=True)

    class Meta:
        app_label = 'assessment'
        unique_together = ('survey', 'user')

    def __str__(self):
        return "%s, %s" % (self.survey, self.user)

    def get_absolute_url(self):
        return reverse('assessment:result_detail',
                       kwargs={'uuid': self.uuid})

    def save(self, *args, **kwargs):
        super(Result, self).save(*args, **kwargs)
        if not self.uuid:
            self.uuid = str(uuid4())
            super(Result, self).save(*args, **kwargs)
        

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
