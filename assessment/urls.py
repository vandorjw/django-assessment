from django.conf.urls import patterns, url
from assessment import views

urlpatterns = patterns(
    '',
    url( # OverView
        regex=r'^$',
        view=views.Index.as_view(),
        name='index'
    ),
    url( # Staff  ONLY -- Creates a new Profile
        regex=r'^assign/$',
        view=views.ProfileCreate.as_view(),
        name='profile_create'
    ),
    url( # Staff  ONLY -- Alters
        regex=r'^assign/(?P<user>[-\w]+)/$',
        view=views.ProfileUpdate.as_view(),
        name='profile_update'
    ),
    url( # Staff  ONLY --- See all surveys
        regex=r'^surveys/$',
        view=views.Surveys.as_view(),
        name='survey_list'
    ),
    url( # Staff  ONLY --- See all results
        regex=r'^results/$',
        view=views.Results.as_view(),
        name="result_list"
    ),
    url( # Staff  ONLY --- Filter results by a Survey
        regex=r'^results/survey/(?P<slug>[-\w]+)/$',
        view=views.ResultBySurvey.as_view(),
        name="result_by_survey"
    ),
    url( # Staff  ONLY --- Filter results by a User
        regex=r'^results/user/(?P<user>[-\w]+)/$',
        view=views.ResultByUser.as_view(),
        name="result_by_user"
    ),
    url( # displays over-view for the user.
        regex=r'^profile/(?P<uuid>[-\w]+)/$',
        view=views.ProfileView.as_view(),
        name='profile_detail'
    ),
    url( # show the results of a particular user
        regex=r'^profile/(?P<uuid>[-\w]+)/results/$',
        view=views.ProfileResults.as_view(),
        name='profile_result_list'
    ),
    url( # show the available surveys of a particular user
        regex=r'^profile/(?P<uuid>[-\w]+)/surveys/$',
        view=views.ProfileSurveys.as_view(),
        name='profile_survey_list'
    ),
    url( # detailed result -- ONLY visible to 1 user and  ALL STAFF
        regex=r'^result/(?P<uuid>[-\w]+)/$',
        view=views.ResultDetail.as_view(),
        name="result_detail"
    ),
    url( # complete a survey --> Create a result instance
        regex=r'^survey/(?P<slug>[-\w]+)/$',
        view=views.SurveyDo.as_view(),
        name='survey_do'
    ),
)
