# Generated by Django 5.0.6 on 2024-09-10 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0087_selectedempnotify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedempnotify',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master'),
        ),
    ]
