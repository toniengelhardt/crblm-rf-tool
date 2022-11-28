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
    role = RoleSerializer()

    class Meta:
        model = Assessment
        fields = ('id', 'role', 'name',)


class AnswerSerializer(BaseModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'employee_assessment', 'question', 'text',)


class EmployeeAssessmentSerializer(BaseModelSerializer):
    profile = ProfileSerializer()
    assessment = AssessmentSerializer()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = EmployeeAssessment
        fields = ('id', 'profile', 'assessment', 'answers', 'completed_dt',)
