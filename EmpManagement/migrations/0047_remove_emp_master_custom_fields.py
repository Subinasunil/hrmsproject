# Generated by Django 5.0.6 on 2024-08-09 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0046_remove_emp_customfieldvalue_emp_master_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_master',
            name='custom_fields',
        ),
    ]
