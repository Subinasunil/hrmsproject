# Generated by Django 5.0.6 on 2024-07-23 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0020_emp_customfield_date_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_customfield',
            name='date_field',
        ),
    ]