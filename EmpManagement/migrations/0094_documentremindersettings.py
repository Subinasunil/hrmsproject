# Generated by Django 5.0.6 on 2024-09-12 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0093_remove_selectedempnotify_selected_ess_users_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentReminderSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_reminder_days_before_expiry', models.IntegerField(default=7)),
                ('second_reminder_days_before_expiry', models.IntegerField(default=5)),
                ('final_reminder_days_after_expiry', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
            ],
        ),
    ]