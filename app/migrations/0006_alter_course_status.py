# Generated by Django 3.2.25 on 2024-12-05 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20241204_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(blank=True, choices=[('compulsory', 'C'), ('elective', 'E'), ('recommendation', 'R')], default='C', max_length=40, null=True),
        ),
    ]