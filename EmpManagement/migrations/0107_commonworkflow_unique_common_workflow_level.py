# Generated by Django 5.0.6 on 2024-09-24 04:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0106_remove_approvallevel_is_common_workflow_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='commonworkflow',
            constraint=models.UniqueConstraint(fields=('level',), name='unique_common_workflow_level'),
        ),
    ]
