# Generated by Django 5.0.6 on 2024-11-13 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0114_alter_emp_master_users'),
        ('LeaveManagement', '0050_remove_weeklyshiftschedule_designation_and_more'),
        ('OrganisationManager', '0013_brnch_mstr_branc_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklyshiftschedule',
            name='weekly_patterns',
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='designation',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.desgntn_master'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='friday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friday_shift', to='LeaveManagement.shift'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='monday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monday_shift', to='LeaveManagement.shift'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='role',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.ctgry_master'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='rotation_pattern',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='saturday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saturday_shift', to='LeaveManagement.shift'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='sunday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sunday_shift', to='LeaveManagement.shift'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='thursday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thursday_shift', to='LeaveManagement.shift'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='tuesday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tuesday_shift', to='LeaveManagement.shift'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='wednesday_shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wednesday_shift', to='LeaveManagement.shift'),
        ),
        migrations.RemoveField(
            model_name='weeklyshiftschedule',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='weeklyshiftschedule',
            name='department',
        ),
        migrations.AlterField(
            model_name='weeklyshiftschedule',
            name='employee',
            field=models.ManyToManyField(blank=True, null=True, to='EmpManagement.emp_master'),
        ),
        migrations.AlterField(
            model_name='weeklyshiftschedule',
            name='rotation_cycle_weeks',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='branch',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.brnch_mstr'),
        ),
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='department',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.dept_master'),
        ),
    ]
