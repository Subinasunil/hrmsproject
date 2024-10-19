# Generated by Django 5.0.6 on 2024-10-04 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0110_emailtemplate_use_common_template'),
        ('LeaveManagement', '0010_remove_employeeshift_employee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('days_of_week', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LeaveManagement.shift')),
            ],
            options={
                'unique_together': {('employee', 'shift', 'start_date')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('total_hours', models.DurationField(blank=True, null=True)),
                ('employee_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LeaveManagement.employeeshift')),
            ],
        ),
    ]