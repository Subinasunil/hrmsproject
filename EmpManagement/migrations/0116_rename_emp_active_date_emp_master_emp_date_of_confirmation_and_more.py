# Generated by Django 5.0.6 on 2024-12-03 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0115_alter_docexpemailtemplate_template_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emp_master',
            old_name='emp_active_date',
            new_name='emp_date_of_confirmation',
        ),
        migrations.RenameField(
            model_name='emp_master',
            old_name='emp_hired_date',
            new_name='emp_joined_date',
        ),
    ]