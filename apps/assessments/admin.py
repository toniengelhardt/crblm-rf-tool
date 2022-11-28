from django.contrib import admin
from django import forms

from .models import Answer, Assessment, EmployeeAssessment, Question, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'text', 'reference',)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question_count',)
    filter_horizontal = ('questions',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('questions')

    def question_count(self, obj):
        return obj.questions.count()


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('question', 'text',)

    # def question_text(self, obj):
    #     return obj.question.text

    # question_text.short_description = 'Question'


@admin.register(EmployeeAssessment)
class EmployeeAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'assessment', 'completed_dt',)

    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'employee_assessment',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'question', 'employee_assessment',  'employee_assessment__profile',
            'employee_assessment__assessment',
        )
