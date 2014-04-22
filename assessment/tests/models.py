from django.test import TestCase
from assessment.models import Survey, Result, Question, Answer, Choice

# Keep these out of the class, as they are needed often.
survey_instance_active = {
    'name': 'My First Survey',
    'slug': 'my-first-survey',
    'description': "Nobody cares, it's just a test.",
    'pub_date': '2014-1-1',
    'due_date': '2014-2-1',
    'is_active': 'True', }
survey_instance_inactive = {
    'name': 'My First Survey',
    'slug': 'my-first-survey',
    'description': "Nobody cares, it's just a test.",
    'pub_date': '2014-1-1',
    'due_date': '2014-2-1',
    'is_active': 'True', }
question_instance_true_false = {
    'survey':'1',
    'question': 'My true/false question?',
    'of_type':'1', }
question_instance_multichoice = {
    'survey':'1',
    'question': 'My multichoice question?',
    'of_type':'2', }
question_instance_textarea = {
    'survey':'1',
    'question': 'My textarea question?',
    'of_type':'3', }
choice_instance_correct = {
    'question': '1',
    'choice_value': 'The answer to the question is True',
    'is_correct': 'True', }
choice_instance_incorrect = {
    'question': '1',
    'choice_value': 'The answer to the question is False',
    'is_correct': 'False', }


class SurveyModelTests(TestCase):

    def setUp(self):
        Survey.objects.create(survey_instance_active)
        Survey.objects.create(survey_instance_inactive)

    def test___str__(self):
        survey0 = Survey.objects.get(slug="my-first-survey")
        self.assertEqual(survey0.__str__(), 'My First Survey')



class QuestionModelTests(TestCase):

    def setUp(self):
        Survey.objects.create(survey_instance_active)
        Question.objects.create(question_instance_true_false)
        Question.objects.create(question_instance_multichoice)
        Question.objects.create(question_instance_textarea)


class ChoiceModelTests(TestCase):

    def setUp(self):
        Survey.objects.create(survey_instance_active)
        Question.objects.create(question_instance_true_false)
        Question.objects.create(question_instance_multichoice)
        Question.objects.create(question_instance_textarea)



