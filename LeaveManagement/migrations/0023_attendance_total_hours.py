# Generated by Django 5.0.6 on 2024-10-07 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0022_remove_attendance_total_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='total_hours',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
