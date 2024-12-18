# Generated by Django 5.0.6 on 2024-11-06 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0045_compensatoryleaverequest_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='compensatoryleaverequest',
            name='request_type',
            field=models.CharField(choices=[('work_request', 'Work Request'), ('leave_request', 'Compensatory Leave Request')], default='work_request', max_length=15),
        ),
    ]
