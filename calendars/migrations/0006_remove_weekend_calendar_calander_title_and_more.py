# Generated by Django 5.0.4 on 2024-07-02 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0011_emp_master_emp_weekend_calendar'),
        ('OrganisationManager', '0005_fiscalyear_end_date'),
        ('calendars', '0005_assign_weekend_employee_remove_assign_weekend_branch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='calander_title',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='friday',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='saturday',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='sunday',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='weekend_calendar',
            name='wednesday',
        ),
        migrations.AddField(
            model_name='assign_holiday',
            name='employee',
            field=models.ManyToManyField(blank=True, null=True, to='EmpManagement.emp_master'),
        ),
        migrations.AddField(
            model_name='holiday',
            name='restricted',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='assign_holiday',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='assign_holiday',
            name='category',
        ),
        migrations.RemoveField(
            model_name='assign_holiday',
            name='department',
        ),
        migrations.AlterField(
            model_name='weekend_calendar',
            name='calendar_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='weekend_calendar',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='weekend_calendar',
            name='year',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='WeekendDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=9)),
                ('day_type', models.CharField(choices=[('leave', 'Leave'), ('work', 'Work'), ('halfday', 'Halfday')], max_length=7)),
                ('week_of_month', models.PositiveIntegerField(blank=True, null=True)),
                ('weekend_calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='calendars.weekend_calendar')),
            ],
        ),
        migrations.AddField(
            model_name='assign_holiday',
            name='branch',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.brnch_mstr'),
        ),
        migrations.AddField(
            model_name='assign_holiday',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.dept_master'),
        ),
        migrations.AddField(
            model_name='assign_holiday',
            name='department',
            field=models.ManyToManyField(blank=True, null=True, to='OrganisationManager.ctgry_master'),
        ),
    ]
