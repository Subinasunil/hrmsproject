# Generated by Django 5.0.4 on 2024-06-07 07:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0009_alter_employeeskill_emp_id'),
        ('OrganisationManager', '0003_brnch_mstr_br_start_date_brnch_mstr_branch_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_number', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('reason', models.CharField(max_length=200)),
                ('total', models.IntegerField(null=True)),
                ('approved', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrganisationManager.brnch_mstr')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
                ('request_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.requesttype')),
            ],
        ),
    ]
