# Generated by Django 5.0.6 on 2024-10-07 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0021_remove_weeklyshiftschedule_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='total_hours',
        ),
    ]