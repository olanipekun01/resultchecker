# Generated by Django 3.2.25 on 2025-01-01 12:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_course_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='carried_over',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='grade_remark',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='grade_type',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='instructor_remark',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='passed',
        ),
        migrations.AddField(
            model_name='confirmregister',
            name='gpa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attempt_number', models.PositiveIntegerField(default=1)),
                ('grade', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('grade_type', models.CharField(blank=True, max_length=5, null=True)),
                ('grade_remark', models.CharField(choices=[('passed', 'passed'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=20)),
                ('passed', models.BooleanField(default=False)),
                ('carried_over', models.BooleanField(default=False)),
                ('result_date', models.DateField(auto_now_add=True)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='app.registration')),
            ],
            options={
                'unique_together': {('registration', 'attempt_number')},
            },
        ),
    ]