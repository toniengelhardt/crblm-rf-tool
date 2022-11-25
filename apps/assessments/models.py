from uuid import uuid4

from django.db import models

from apps.user.models import Profile


class Role(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Question(models.Model):
    role = models.ForeignKey(Role, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    reference = models.TextField()

    def __str__(self):
        return self.text[:8] + '...'


class Assessment(models.Model):
    name = models.CharField(max_length=80)
    questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return self.name


class EmployeeAssessment(models.Model):
    uid = models.UUIDField(default=uuid4)
    profile = models.ForeignKey(Profile, related_name='employee_assessments', on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, related_name='employee_assessments', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uid)


class Answer(models.Model):
    employee_assessment = models.ForeignKey(EmployeeAssessment, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
