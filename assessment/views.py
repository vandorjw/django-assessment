from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from braces.views import LoginRequiredMixin
from braces.views import StaffuserRequiredMixin
from assessment.models import Survey, Result, Question, Answer, Profile
from assessment.forms import SurveyDoForm, ProfileForm

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
   

class Index(LoginRequiredMixin,
            generic.TemplateView):
    template_name = 'assessment/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
          return context
        else:
          return context


class ProfileCreate(LoginRequiredMixin,
                   StaffuserRequiredMixin,
                   generic.CreateView):
    model = Profile
    template_name = 'assessment/profile_form.html'
    form_class = ProfileForm


class ProfileUpdate(LoginRequiredMixin,
                   StaffuserRequiredMixin,
                   generic.UpdateView):
    model = Profile
    template_name = 'assessment/profile_form.html'
    form_class = ProfileForm

    def get_object(self, **kwargs):
        return Profile.objects.get(
            user__in=User.objects.filter(username=self.kwargs['user']))


class Surveys(LoginRequiredMixin,
              StaffuserRequiredMixin,
              generic.ListView):
    template_name = 'assessment/survey_list.html'
    model = Survey


class Results(LoginRequiredMixin,
              StaffuserRequiredMixin,
              generic.ListView):
    template_name = 'assessment/result_list.html'
    model = Result


class ResultBySurvey(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     generic.TemplateView):
    template_name = 'assessment/result_by_survey.html'

    def get_context_data(self, **kwargs):
        context = super(ResultBySurvey, self).get_context_data(**kwargs)
        context['results'] = Result.objects.filter(
            survey__in=Survey.objects.filter(slug=self.kwargs['slug']))
        return context


class ResultByUser(LoginRequiredMixin,
                   StaffuserRequiredMixin,
                   generic.TemplateView):
    template_name = 'assessment/result_by_user.html'

    def get_context_data(self, **kwargs):
        context = super(ResultByUser, self).get_context_data(**kwargs)
        context['results'] = Result.objects.filter(
            user__in=User.objects.filter(username=self.kwargs['user']))
        return context


class ProfileView(LoginRequiredMixin,
              generic.DetailView):
    template_name = 'assessment/profile_detail.html'
    model = Profile
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.user == self.request.user or
            self.request.user.is_staff ):
            return super(ProfileView, self).get(request, *args, **kwargs)
        else:
            return redirect('assessment:index')


class ProfileResults(LoginRequiredMixin, generic.ListView):
    model = Result
    template_name = 'assessment/profile_result_list.html'

    def get(self, request, *args, **kwargs):
        self.profile = Profile.objects.get(uuid=self.kwargs['uuid'])
        if (self.profile.user == self.request.user or
            self.request.user.is_staff ):
            return super(ProfileResults, self).get(request, *args, **kwargs)
        else:
            return redirect('assessment:index')

    def get_context_data(self, **kwargs):
        context = super(ProfileResults, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(uuid=self.kwargs['uuid'])
        return context

class ProfileSurveys(LoginRequiredMixin, generic.ListView):
    model = Surveys
    template_name = 'assessment/profile_survey_list.html'

    def get(self, request, *args, **kwargs):
        self.profile = Profile.objects.get(uuid=self.kwargs['uuid'])
        if (self.profile.user == self.request.user or
            self.request.user.is_staff ):
            return super(ProfileSurveys, self).get(request, *args, **kwargs)
        else:
            return redirect('assessment:index')

    def get_context_data(self, **kwargs):
        context = super(ProfileResults, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(uuid=self.kwargs['uuid'])
        return context


class ResultDetail(LoginRequiredMixin, generic.DetailView):
    model = Result
    template_name = 'assessment/result_detail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.user == self.request.user or
            self.request.user.is_staff ):
            return super(ResultDetail, self).get(request, *args, **kwargs)
        else:
            return redirect('assessment:index')


class SurveyDo(LoginRequiredMixin, generic.CreateView):
    model = Result
    template_name = 'assessment/survey_do.html'
    form_class = SurveyDoForm

    def get(self, request, *args, **kwargs):
        if Result.objects.filter(
            survey = Survey.objects.get(slug=self.kwargs['slug']),
            user = self.request.user).exists():
            return redirect('assessment:index')
        return super(SurveyDo, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if Result.objects.filter(
            survey = Survey.objects.get(slug=self.kwargs['slug']),
            user = self.request.user).exists():
            return redirect('assessment:index')
        return super(SurveyDo, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SurveyDo, self).get_form_kwargs()
        kwargs['survey'] = Survey.objects.get(slug=self.kwargs['slug'])
        kwargs['user'] = self.request.user
        return kwargs

