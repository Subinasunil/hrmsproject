# Generated by Django 5.0.6 on 2024-09-12 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0092_remove_selectedempnotify_selected_ess_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectedempnotify',
            name='selected_ess_users',
        ),
        migrations.AddField(
            model_name='selectedempnotify',
            name='selected_ess_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EmpManagement.emp_master'),
        ),
    ]
