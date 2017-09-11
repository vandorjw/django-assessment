# -*- coding: utf-8 -*-
import datetime
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from django.utils.translation import ugettext as _


class Survey(TranslatableModel):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    translations = TranslatedFields(
        name=models.CharField(_("name"), max_length=160),
        description=models.TextField(_("description")),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    is_private = models.BooleanField(
        _("private"),
        default=False,
    )

    start_date_time = models.DateTimeField(
        _("start time"),
        auto_now=False,
        default=datetime.datetime.now,
    )

    end_date_time = models.DateTimeField(
        _("end time"),
        auto_now=False,
        null=True,
        blank=True,
    )

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assessment_admin_surveys",
        verbose_name=_('owner'),
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="assessment_user_surveys",
        blank=True,
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return self.name


class Question(TranslatableModel):

    TRUEFALSE = 1
    MULTIPLE_CHOICE = 2
    TEXT = 3

    QUESTION_TYPE = (
        (TRUEFALSE, _('true or false')),
        (MULTIPLE_CHOICE, _('multiple choice')),
        (TEXT, _('text')),
    )

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    translations = TranslatedFields(
        question=models.CharField(_("question"), max_length=512),
    )

    survey = models.ForeignKey(
        Survey,
        related_name='questions',
        verbose_name=_("survey")
    )

    is_required = models.BooleanField(
        _("required"),
        default=False,
    )

    of_type = models.IntegerField(
        _("type"),
        choices=QUESTION_TYPE,
        default=TRUEFALSE,
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.question


class Choice(TranslatableModel):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    translations = TranslatedFields(
        value=models.CharField(_("value"), max_length=512),
    )

    question = models.ForeignKey(
        Question,
        related_name='choices',
        verbose_name=_("question"),
    )

    is_correct = models.BooleanField(
        _("correct"),
        default=False,
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _('choice')
        verbose_name_plural = _('choices')

    def __str__(self):
        return self.value


class Result(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    timestamp = models.DateTimeField(
        editable=False,
        default=datetime.datetime.now,
    )

    survey = models.ForeignKey(
        Survey,
        related_name='results',
        verbose_name=_("survey"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='results',
        verbose_name=_("user"),
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _('result')
        verbose_name_plural = _('results')
        unique_together = ('survey', 'user')

    def __str__(self):
        return str(self.pk)

    def clean(self, *args, **kwargs):
        if self.survey.is_private:
            if self.user == self.survey.admin or self.user in self.survey.users.all():
                # The user is allowed to answer this survey.
                # sonarqube complains about how this is structured...
                pass
            else:
                raise ValidationError("User attempted to answer private survey!")


class Answer(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    result = models.ForeignKey(
        Result,
        related_name='answers',
        verbose_name=_("result"),
    )

    question = models.ForeignKey(
        Question,
        related_name='answers',
        verbose_name=_("question"),
    )

    answer = models.TextField(
        _("answer"),
    )

    class Meta:
        app_label = 'assessment'
        unique_together = ('result', 'question')
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __str__(self):
        return self.answer

    def clean(self, *args, **kwargs):
        if self.question not in self.result.survey.questions.all():
            raise ValidationError("User attempted to answer a question not part of this survey!")
