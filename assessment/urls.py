from django.conf.urls import patterns, url
from assessment import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.AssessmentIndex.as_view(),
        name='index'
    ),
    url(
        regex=r'^surveys/$',
        view=views.SurveyListView.as_view(),
        name='survey_list'
    ),
    url(
        regex=r'^surveys/(?P<slug>[-\w]+)/$',
        view=views.ResultCreateView.as_view(),
        name='survey_do'
    ),
    url(
        regex=r'^surveys/result/(?P<pk>\d+)/$',
        view=views.ResultDetailView.as_view(),
        name="survey_result"
    ),
    url(
        regex=r'^results/$',
        view=views.ResultListView.as_view(),
        name="result_list"
    ),
    url(
        regex=r'^results/(?P<slug>[-\w]+)/$',
        view=views.SurveyResultListView.as_view(),
        name="survey_result_list"
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/results/$',
        view=views.UserResultListView.as_view(),
        name='user_results'
    ),
)
