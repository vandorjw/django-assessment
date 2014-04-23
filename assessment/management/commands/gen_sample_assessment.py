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
        'question': 'My true/false question?',
        'of_type':'1', }

    help = 'Creates a sample survey.'

    def handle_noargs(self, *args, **options):
        try:
            survey = Survey( **self.survey_instance)
            survey.save()
            q1 = Question(survey=survey, **self.question_instance_true_false)
            q1.save()
            self.stdout.write(
                "Successfully created sample survey: '%s'" % survey.slug)
        except:
            self.stdout.write(
                "FAILED to create sample survey, does it already exist?")
