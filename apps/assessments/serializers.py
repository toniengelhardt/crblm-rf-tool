from core.serializers import BaseModelSerializer
from apps.user.serializers import ProfileSerializer
from .models import Answer, Assessment, EmployeeAssessment, Question, Role


class RoleSerializer(BaseModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name',)


class QuestionSerializer(BaseModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'role', 'text',)


class AssessmentSerializer(BaseModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ('id', 'name', 'questions',)


class EmployeeAssessmentSerializer(BaseModelSerializer):
    profile = ProfileSerializer()
    assessment = AssessmentSerializer()

    class Meta:
        model = EmployeeAssessment
        fields = ('id', 'profile', 'assessment', 'completed_dt',)


class AnswerSerializer(BaseModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'employee_assessment', 'text',)
