from django.views import generic
from django.shortcuts import redirect
from braces.views import LoginRequiredMixin
from braces.views import GroupRequiredMixin
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
        context['incomplete_surveys'] = Survey.surveys.exclude(
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

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(ResultDetailView, self).get(request, *args, **kwargs)
        else:
            return redirect('assessment:assessment_surveys')

    def get_context_data(self, **kwargs):
        context = super(SurveyResultListView, self).get_context_data(**kwargs)
        context['results'] = Result.objects.filter(
            survey__in=Survey.objects.filter(slug=self.kwargs['slug']))
        return context


class ResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = Result
    template_name = 'assessment/survey_result.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.user == self.request.user or
            self.request.user.is_staff ):
            return super(ResultDetailView, self).get(request, *args, **kwargs)
        else:
            return redirect('assessment:assessment_surveys')


class ResultCreateView(LoginRequiredMixin, generic.CreateView):
    model = Result
    template_name = 'assessment/survey_do.html'
    form_class = ResultCreateForm

    def get(self, request, *args, **kwargs):
        if Result.objects.filter(
            survey = Survey.objects.get(slug=self.kwargs['slug']),
            user = self.request.user).exists():
            return redirect('assessment:survey_list')
        return super(ResultCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if Result.objects.filter(
            survey = Survey.objects.get(slug=self.kwargs['slug']),
            user = self.request.user).exists():
            return redirect('assessment:survey_list')
        return super(ResultCreateView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ResultCreateView, self).get_form_kwargs()
        kwargs['survey'] = Survey.objects.get(slug=self.kwargs['slug'])
        kwargs['user'] = self.request.user
        return kwargs

