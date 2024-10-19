# Generated by Django 5.0.4 on 2024-07-12 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0011_emp_master_emp_weekend_calendar'),
        ('calendars', '0010_alter_weekenddetail_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_master',
            name='holiday_calendar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendars.holiday_calendar'),
        ),
    ]
