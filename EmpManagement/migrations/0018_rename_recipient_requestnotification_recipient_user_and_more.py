# Generated by Django 5.0.6 on 2024-07-20 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0017_remove_notification_recipient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestnotification',
            old_name='recipient',
            new_name='recipient_user',
        ),
        migrations.AddField(
            model_name='requestnotification',
            name='recipient_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master'),
        ),
    ]