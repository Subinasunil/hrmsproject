# Generated by Django 5.0.6 on 2024-08-09 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0044_emailtemplate_requesttype_email_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_master',
            name='custom_fields',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
