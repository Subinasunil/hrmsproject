# Generated by Django 5.0.6 on 2024-10-03 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0005_shift_employeeshift_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeshift',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='employeeshift',
            name='shift',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='EmployeeShift',
        ),
        migrations.DeleteModel(
            name='Shift',
        ),
    ]
