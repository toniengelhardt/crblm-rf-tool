from uuid import uuid4

from django.db import models

from apps.user.models import Profile


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    role = models.ForeignKey(Role, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    reference = models.TextField()

    def __str__(self):
        return self.text[:37] + '...' if len(self.text) > 40 else self.text


class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    role = models.ForeignKey(Role, related_name='assessments', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return self.name


class EmployeeAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    profile = models.ForeignKey(Profile, related_name='employee_assessments', on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, related_name='employee_assessments', on_delete=models.CASCADE)
    completed_dt = models.DateTimeField(null=True, blank=True)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    employee_assessment = models.ForeignKey(EmployeeAssessment, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', null=True, on_delete=models.CASCADE)
    text = models.TextField()
