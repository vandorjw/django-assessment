from math import floor
from django import forms
from assessment.models import Survey, Result, Question, Answer, Choice


class ResultCreateForm(forms.ModelForm):
    """
    This form creates a Result object. When initializing the form, it
    needs to know which survey instance it is dealing with and the user.
    For each question in the survey instance an answer field is created.
    If the question has a single, predetermined answer, such as a true
    false, or a multiple choice answer, the field for the question must
    be a ModelChoiceField.

    If the question is a fill-in-the-blank, the field associated with
    that question is Charfield.

    Please also note that every field in the Result Model is not
    editable. No field for the result instance is to be changed by the
    user, when the form is rendered.

    """
    def __init__(self, survey, user, *args, **kwargs):
        super(ResultCreateForm, self).__init__(*args, **kwargs)
        # required for the save method.
        self.user = user
        # required for the save method.
        self.survey = survey
        for q in survey.question_set.all():
            if q.of_type == Question.MULTICHOICE:
                self.fields.insert(
                    len(self.fields),
                    str(q.id),
                    forms.ModelChoiceField(
                        widget=forms.RadioSelect(attrs={'class': 'multichoice'}),
                        queryset=Choice.objects.filter(question=q),
                        empty_label=None
                    ),
                )
                self.fields[str(q.id)].label = str(q)
            elif q.of_type == Question.TRUEFALSE:
                self.fields.insert(
                    len(self.fields),
                    str(q.id),
                    forms.ModelChoiceField(
                        widget=forms.RadioSelect(attrs={'class': 'truefalse'}),
                        queryset=Choice.objects.filter(question=q),
                        empty_label=None
                    ),
                )
                self.fields[str(q.id)].label = str(q)
            else:
                self.fields.insert(len(self.fields),
                    str(q.id),
                    forms.CharField(
                        widget=forms.Textarea(attrs={'class': 'textarea', 
                                                     'style':'width:100%'}),
                        max_length=500
                    ),
                )
                self.fields[str(q.id)].label = str(q)

    def save(self, *args, **kwargs):
        """
        This form creates a Result Instance. Since survey, user, and
        score are not editable when the form is filled out, we must add
        this data to the result instance ourself.

        We already collected the user and survey instance when the form
        initialized. The super method grabs the 'completed_on' field
        with the submission time, but does not save to the database.
        The user and survey fields are filled in.

        We then count the number of questions the user answered
        correctly. If a question is not of type TRUE/False or
        MultipleChoice, we do not count it towards the total.

        We loop through the choices, and FIRST check if the choice a
        correct choice, and then we check if this was what the user
        selected. Only once we have tallied the score do we save the
        result.instance

        ----------------------------------------------------------------
        Saving the Answers:
        Since saving each answer with an individual database query,
        would put ENORMOUS strain on our database, the answers are saved
        in bulk.

        Each answer instance must have the folllowing:

        >> result: This is the id of the Result instance we just saved.
        >> question: This is id of each question in the survey.
        >> answer: This is the CLEANED input entered into each field.

        NOTE: Please remember that each field.id is is the same as the
        question.id

        FINAL NOTICE:
        bulk_create() - Although effiecient, it does not auto-increment
        the primary key (id) of each item saved. To ensure each primary
        key is unique, the primary keys are created from the following:

        >> int(result.id)*1000 + question.count

        EXAMPLE: 5 Questions, and result_id == 17
          answer.id = 17000
          answer.id = 17001
          answer.id = 17002
          answer.id = 17003
          answer.id = 17004

        Finally, the result instance is returned.

        """
        instance = super(ResultCreateForm, self).save(commit=False)
        instance.user = self.user
        instance.survey = self.survey
        q_correct = 0
        q_total = 0
        for q in self.survey.question_set.all():
            if (q.of_type == Question.TRUEFALSE or
                    q.of_type == Question.MULTICHOICE):
                q_total += 1
                for choice in q.choices.all():
                    if (choice.is_correct and
                            choice == self.cleaned_data[str(q.id)]):
                        q_correct += 1
        instance.score = "%s out of %s" % (q_correct, q_total)
        if(q_total == 0):
            instance.score_percentage = 000
        else:
            instance.score_percentage = floor((q_correct/q_total) * 100)
        instance.save()
        # The response has been saved. We now save the answers.
        result_id = instance.id
        start_ans_id = result_id * 1000
        end_ans_id = start_ans_id + self.survey.question_set.count()
        ans_ids = list(range(start_ans_id, end_ans_id))
        q_answers = []
        for question in self.survey.question_set.all():
            # always append the 'cleaned_data', never the raw post data!
            q_answers.append(self.cleaned_data[str(question.id)])
        zipped = zip(ans_ids, self.survey.question_set.all(), q_answers)
        data = [Answer(id=answer_id,
                       result=instance,
                       question=q_obj,
                       answer=ans_value)
                for answer_id, q_obj, ans_value in zipped]
        Answer.objects.bulk_create(data)
        # The answers are saved.
        return instance

    class Meta:
        model = Result
        fields = '__all__'
