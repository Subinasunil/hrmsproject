# Generated by Django 5.0.6 on 2024-10-05 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0018_remove_weeklyshiftschedule_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='LeaveManagement.shift'),
        ),
    ]
