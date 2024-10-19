# Generated by Django 5.0.6 on 2024-08-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0064_remove_emp_customfieldvalue_emp_custom_field_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_customfieldvalue',
            name='emp_custom_field',
        ),
        migrations.AddField(
            model_name='emp_customfieldvalue',
            name='field_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
