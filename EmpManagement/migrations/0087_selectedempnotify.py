# Generated by Django 5.0.6 on 2024-09-10 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0086_notification_s_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedEmpNotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receive_notifications', models.BooleanField(default=False)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
            ],
        ),
    ]
