from datetime import datetime
from django.db import models


class SurveyManager(models.Manager):
    """
    How to use this manager:

    1. Retrieve all active surveys:
    >> survey_list = Survey.surveys.all()

    2. Retrieve all surveys where the over 50% failed:
    >> survey_list = Survey.surveys.avg_failed()

    3. Retrieve all surveys where the over 50% passed:
    >> survey_list = Survey.surveys.avg_passed()

    """
    def get_queryset(self):
        """ Only return active surveys, where the pub_date is before today,
        and the survey is not past the due_date. """
        return super(SurveyManager, self).get_queryset().filter(
            is_active = True).exclude(
            start_date_time__gte=datetime.now()).exclude(
            end_date_time__lte=datetime.now())

    def avg_failed(self):
        """
        1. Count all results from a survey.
        2. Count all results where the score_percentage < 50
        3. If this was more than half, add the survey to the queryset.
        """
        raise NotImplementedError

    def avg_passed(self):
        """
        1. Get all surveys.
        2. Exclude results from avg_failed
        """
        raise NotImplementedError
