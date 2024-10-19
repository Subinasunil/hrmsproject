# Generated by Django 5.0.4 on 2024-05-22 05:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='brnch_mstr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=100)),
                ('notification_period_days', models.IntegerField()),
                ('br_is_active', models.BooleanField(default=True)),
                ('br_city', models.CharField(max_length=50)),
                ('br_pincode', models.CharField(max_length=20)),
                ('br_branch_nmbr_1', models.CharField(max_length=20, unique=True)),
                ('br_branch_nmbr_2', models.CharField(blank=True, max_length=20, null=True)),
                ('br_branch_mail', models.EmailField(max_length=254, unique=True)),
                ('br_created_at', models.DateTimeField(auto_now_add=True)),
                ('br_updated_at', models.DateTimeField(auto_now=True)),
                ('br_country', models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='Core.cntry_mstr')),
                ('br_created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('br_state_id', models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='Core.state_mstr')),
                ('br_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cmpny_mastr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmpny_name', models.CharField(max_length=100, unique=True)),
                ('cmpny_is_active', models.BooleanField(default=True)),
                ('cmpny_city', models.CharField(max_length=50)),
                ('cmpny_pincode', models.CharField(max_length=20)),
                ('cmpny_nmbr_1', models.CharField(max_length=20, unique=True)),
                ('cmpny_nmbr_2', models.CharField(blank=True, max_length=20, null=True)),
                ('cmpny_mail', models.EmailField(max_length=254, unique=True)),
                ('cmpny_logo', models.ImageField(null=True, upload_to='logos')),
                ('cmpny_fax', models.CharField(blank=True, max_length=100, null=True)),
                ('cmpny_gst', models.CharField(blank=True, max_length=100, null=True)),
                ('cmpny_created_at', models.DateTimeField(auto_now_add=True)),
                ('cmpny_updated_at', models.DateTimeField(auto_now=True)),
                ('cmpny_country', models.ForeignKey(default='1', on_delete=django.db.models.deletion.SET_DEFAULT, to='Core.cntry_mstr')),
                ('cmpny_created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('cmpny_state_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.state_mstr')),
                ('cmpny_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ctgry_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catogary_title', models.CharField(max_length=50)),
                ('ctgry_description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='dept_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='OrganisationManager.brnch_mstr')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='desgntn_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FiscalYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrganisationManager.cmpny_mastr')),
            ],
        ),
        migrations.CreateModel(
            name='FiscalPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_number', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fiscal_periods', to='OrganisationManager.cmpny_mastr')),
                ('fiscal_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrganisationManager.fiscalyear')),
            ],
            options={
                'unique_together': {('fiscal_year', 'period_number')},
            },
        ),
    ]