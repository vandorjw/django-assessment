from rest_framework import routers
from assessment.views.api import (
    SurveyViewSet,
    SurveyAdminViewSet,
    SurveyGroupViewSet,
    ProfileViewSet,
    QuestionViewSet,
    ChoiceViewSet,
    ResultViewSet,
    AnswerViewSet,

)

router = routers.SimpleRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'survey-admins', SurveyAdminViewSet)
router.register(r'survey-groups', SurveyGroupViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'results', ResultViewSet)
router.register(r'answers', AnswerViewSet)
urlpatterns = router.urls
