import sys
from django.core.management.base import NoArgsCommand
from assessment.models import Survey, Question, Choice

class Command(NoArgsCommand):

    survey_instance = {
        'name': 'Sample Survey',
        'slug': 'sample-survey',
        'description': "This is a sample Survey. There are no rules.",
        'pub_date': '2010-1-1',
        'due_date': '2016-1-1',
        'is_active': 'True', }

    question_instance_true_false = {
        'question': 'The Moon is bigger than a star.',
        'of_type': '1', }

    choice_instance_true = {
        'choice_value': 'This statement is True',
        'is_correct': False, }

    choice_instance_false = {
        'choice_value': 'This statement is False',
        'is_correct': True, }

    help = 'Creates a sample survey.'

    def handle_noargs(self, *args, **options):
        try:
            survey = Survey( **self.survey_instance)
            survey.save()
            q1 = Question(survey=survey, **self.question_instance_true_false)
            q1.save()
            c1 = Choice(question=q1, **self.choice_instance_true)
            c1.save()
            c2 = Choice(question=q1, **self.choice_instance_false)
            c2.save()
            self.stdout.write(
                "Successfully created sample survey: '%s'" % survey.slug)
        except IntegrityError:
            err = sys.exc_info()[0]
            self.stdout.write(
                "FAILED to create sample survey: %s'" % err )
