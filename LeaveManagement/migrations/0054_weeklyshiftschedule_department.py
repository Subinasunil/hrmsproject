# Generated by Django 5.0.6 on 2024-11-18 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0053_remove_weeklyshiftschedule_branch_and_more'),
        ('OrganisationManager', '0013_brnch_mstr_branc_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklyshiftschedule',
            name='department',
            field=models.ManyToManyField(blank=True, to='OrganisationManager.dept_master'),
        ),
    ]