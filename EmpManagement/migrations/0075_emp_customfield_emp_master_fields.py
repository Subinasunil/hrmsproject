# Generated by Django 5.0.6 on 2024-08-22 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0074_emp_master_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_customfield',
            name='emp_master_fields',
            field=models.JSONField(blank=True, null=True),
        ),
    ]