# Generated by Django 5.0.6 on 2024-07-26 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0026_emp_customfieldvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_customfield',
            name='field_value',
        ),
    ]
