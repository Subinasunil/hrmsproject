# Generated by Django 5.0.6 on 2024-09-10 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0089_rename_employee_selectedempnotify_selected_ess_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedempnotify',
            name='selected_ess_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EmpManagement.emp_master'),
        ),
    ]