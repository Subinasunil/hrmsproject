# Generated by Django 5.0.4 on 2024-05-22 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_master',
            name='emp_languages',
        ),
    ]
