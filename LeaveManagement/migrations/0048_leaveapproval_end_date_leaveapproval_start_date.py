# Generated by Django 5.0.6 on 2024-11-08 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0047_leaveapproval_employee_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapproval',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leaveapproval',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]