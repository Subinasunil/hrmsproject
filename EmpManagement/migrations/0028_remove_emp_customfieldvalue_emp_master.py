# Generated by Django 5.0.6 on 2024-07-27 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0027_remove_emp_customfield_field_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_customfieldvalue',
            name='emp_master',
        ),
    ]