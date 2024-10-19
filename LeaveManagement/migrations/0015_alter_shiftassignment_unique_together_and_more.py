# Generated by Django 5.0.6 on 2024-10-04 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0110_emailtemplate_use_common_template'),
        ('LeaveManagement', '0014_shift_shiftassignment_attendance_shift_assignment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shiftassignment',
            unique_together={('employee', 'shift')},
        ),
        migrations.RemoveField(
            model_name='shiftassignment',
            name='date',
        ),
    ]
