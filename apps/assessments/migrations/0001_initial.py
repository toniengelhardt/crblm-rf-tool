# Generated by Django 4.1.3 on 2022-11-25 18:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('reference', models.TextField()),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='assessments.role')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAssessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('completed_dt', models.DateTimeField(blank=True, null=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_assessments', to='assessments.assessment')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_assessments', to='user.profile')),
            ],
        ),
        migrations.AddField(
            model_name='assessment',
            name='questions',
            field=models.ManyToManyField(blank=True, to='assessments.question'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='assessments.role'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('employee_assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='assessments.employeeassessment')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='assessments.question')),
            ],
        ),
    ]
