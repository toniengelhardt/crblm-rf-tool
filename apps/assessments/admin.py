from django.contrib import admin

from .models import Answer, Assessment, EmployeeAssessment, Question, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'text', 'reference',)


class QuestionInline(admin.TabularInline):
    model = Assessment.questions.through
    extra = 1
    fields = ('id',)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question_count',)
    # inlines = [QuestionInline]
    filter_horizontal = ('questions',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('questions')

    def question_count(self, obj):
        return obj.questions.count()


@admin.register(EmployeeAssessment)
class EmployeeAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'assessment', 'completed_dt',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_assessment',)
