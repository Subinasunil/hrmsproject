# Generated by Django 5.0.6 on 2024-07-27 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0028_remove_emp_customfieldvalue_emp_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_customfieldvalue',
            name='emp_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_field_values', to='EmpManagement.emp_master'),
        ),
    ]