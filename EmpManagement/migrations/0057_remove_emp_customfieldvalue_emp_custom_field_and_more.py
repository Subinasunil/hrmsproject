# Generated by Django 5.0.6 on 2024-08-14 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0056_alter_emp_customfieldvalue_emp_custom_field'),
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
