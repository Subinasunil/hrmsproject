# Generated by Django 5.0.6 on 2024-10-03 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrganisationManager', '0011_alter_attendance_total_hours'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]