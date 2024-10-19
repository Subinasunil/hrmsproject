# Generated by Django 5.0.6 on 2024-08-14 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0057_remove_emp_customfieldvalue_emp_custom_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_customfieldvalue',
            name='field_name',
        ),
        migrations.AddField(
            model_name='emp_customfieldvalue',
            name='emp_custom_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_values', to='EmpManagement.emp_customfield'),
        ),
    ]
