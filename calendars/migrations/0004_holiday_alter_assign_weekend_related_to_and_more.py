# Generated by Django 5.0.4 on 2024-06-28 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrganisationManager', '0005_fiscalyear_end_date'),
        ('calendars', '0003_remove_assign_weekend_target_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='assign_weekend',
            name='related_to',
            field=models.CharField(choices=[('branch', 'branch'), ('department', 'department'), ('category', 'category'), ('employee', 'employee')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='holiday_calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_title', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('holiday', models.ManyToManyField(to='calendars.holiday')),
            ],
        ),
        migrations.CreateModel(
            name='assign_holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_to', models.CharField(choices=[('branch', 'Branch'), ('department', 'Department'), ('category', 'Category'), ('employee', 'Employee')], max_length=20, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='OrganisationManager.brnch_mstr')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='OrganisationManager.dept_master')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='OrganisationManager.ctgry_master')),
                ('holiday_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendars.holiday_calendar')),
            ],
        ),
    ]
