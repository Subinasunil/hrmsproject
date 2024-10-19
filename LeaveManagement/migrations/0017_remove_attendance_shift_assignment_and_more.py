# Generated by Django 5.0.6 on 2024-10-05 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0110_emailtemplate_use_common_template'),
        ('LeaveManagement', '0016_shiftassignment_end_date_shiftassignment_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='shift_assignment',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='check_in',
            new_name='check_in_time',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='check_out',
            new_name='check_out_time',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='break_time',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='total_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='WeeklyShiftSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
                ('friday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friday_shift', to='LeaveManagement.shift')),
                ('monday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monday_shift', to='LeaveManagement.shift')),
                ('saturday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saturday_shift', to='LeaveManagement.shift')),
                ('sunday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sunday_shift', to='LeaveManagement.shift')),
                ('thursday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thursday_shift', to='LeaveManagement.shift')),
                ('tuesday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tuesday_shift', to='LeaveManagement.shift')),
                ('wednesday_shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wednesday_shift', to='LeaveManagement.shift')),
            ],
        ),
        migrations.DeleteModel(
            name='ShiftAssignment',
        ),
    ]
