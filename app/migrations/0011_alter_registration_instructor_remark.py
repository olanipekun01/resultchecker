# Generated by Django 3.2.25 on 2025-01-03 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_result_total_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='instructor_remark',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default='pending', max_length=50, null=True),
        ),
    ]
