# Generated by Django 5.0.6 on 2024-10-03 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0110_emailtemplate_use_common_template'),
        ('LeaveManagement', '0006_remove_employeeshift_employee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_name', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField()),
                ('employee', models.ManyToManyField(to='EmpManagement.emp_master')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LeaveManagement.shift')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('check_in_time', models.TimeField(blank=True, null=True)),
                ('check_out_time', models.TimeField(blank=True, null=True)),
                ('total_hours', models.DurationField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
                ('shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LeaveManagement.shift')),
            ],
        ),
    ]