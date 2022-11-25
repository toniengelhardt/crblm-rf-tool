from rest_framework.routers import DefaultRouter

from .views import AnswersViewSet, AssessmentsViewSet, EmployeeAssessmentsViewSet, QuestionsViewSet, RolesViewSet


app_name = 'assessments'


router = DefaultRouter()
router.register(r'answers', AnswersViewSet, basename='answers')
router.register(r'assessments', AssessmentsViewSet, basename='assessments')
router.register(r'employee-assessments', EmployeeAssessmentsViewSet, basename='employee_assessments')
router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'roles', RolesViewSet, basename='roles')

urlpatterns = router.urls + [
    # ...
]
