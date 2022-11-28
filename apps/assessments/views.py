from rest_framework.permissions import AllowAny

from core.views import BaseModelViewSet
from .models import Answer, Assessment, EmployeeAssessment, Question, Role
from .serializers import (
    AnswerSerializer, AssessmentSerializer, EmployeeAssessmentSerializer,
    QuestionSerializer, RoleSerializer,
)


class RolesViewSet(BaseModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Role.objects.all()


class QuestionsViewSet(BaseModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Question.objects.all()


class AssessmentsViewSet(BaseModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Assessment.objects.all()


class EmployeeAssessmentsViewSet(BaseModelViewSet):
    serializer_class = EmployeeAssessmentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return EmployeeAssessment.objects.prefetch_related('answers',)


class AnswersViewSet(BaseModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Answer.objects.all()
