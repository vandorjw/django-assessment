from django.views import generic
from braces.views import LoginRequiredMixin
from assessment.models import Survey, Result, Question, Answer
from assessment.forms import ResultCreateForm
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class AssessmentIndex(LoginRequiredMixin, generic.TemplateView):
    """alternative - redirect to SurveyListView"""
    template_name = 'assessment/index.html'

    def get_context_data(self, **kwargs):
        context = super(AssessmentIndex, self).get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        context['survey_list'] = Survey.objects.all()
        return context


class SurveyListView(LoginRequiredMixin, generic.ListView):
    template_name = 'assessment/survey_list.html'
    model = Survey

    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        context['incomplete_surveys'] = Survey.objects.filter(
            is_active=True).exclude(
                results__in=self.request.user.results.all()
        )
        context['user_results'] = self.request.user.results.all()
        return context


class UserResultListView(LoginRequiredMixin, generic.ListView):
    model = Result
    template_name = 'assessment/user_results.html'

    def get_context_data(self, **kwargs):
        context = super(UserResultListView, self).get_context_data(**kwargs)
        context['results'] = Result.objects.filter(user=self.kwargs['pk'])
        return context


class ResultListView(LoginRequiredMixin, generic.ListView):
    model = Result
    template_name = 'assessment/result_list.html'


class SurveyResultListView(LoginRequiredMixin, generic.ListView):
    model = Result
    template_name = 'assessment/survey_result_list.html'

    def get_context_data(self, **kwargs):
        context = super(SurveyResultListView, self).get_context_data(**kwargs)
        context['results'] = Result.objects.filter(
            survey__in=Survey.objects.filter(slug=self.kwargs['slug']))
        return context


class ResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = Result
    template_name = 'assessment/survey_result.html'


class ResultCreateView(LoginRequiredMixin, generic.CreateView):
    """
    If this form is required in another view, the arguments can also be
    passed to the form as followes:

    >> def get_context_data(self, **kwargs):
    >>    context = super(ResultCreateView, self).get_context_data(**kwargs)
    >>    survey = Survey.objects.get(slug=self.kwargs['slug'])
    >>    user = self.request.user
    >>    answer_form = ResultCreateForm(survey, user)
    >>    context['my_form'] = answer_form

    """
    model = Result
    template_name = 'assessment/survey_do.html'
    form_class = ResultCreateForm

    def get_form_kwargs(self):
        kwargs = super(ResultCreateView, self).get_form_kwargs()
        kwargs['survey'] = Survey.objects.get(slug=self.kwargs['slug'])
        kwargs['user'] = self.request.user
        return kwargs
