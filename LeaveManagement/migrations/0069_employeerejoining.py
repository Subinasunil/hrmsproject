# Generated by Django 5.0.6 on 2024-12-06 06:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0118_alter_emp_master_emp_gender_and_more'),
        ('LeaveManagement', '0068_delete_employeerejoining'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeRejoining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rejoining_date', models.DateField()),
                ('unpaid_leave_days', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
                ('leave_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='LeaveManagement.employee_leave_request')),
            ],
        ),
    ]
