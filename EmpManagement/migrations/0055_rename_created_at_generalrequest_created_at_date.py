# Generated by Django 5.0.6 on 2024-08-12 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0054_rename_created_at_date_generalrequest_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalrequest',
            old_name='created_at',
            new_name='created_at_date',
        ),
    ]
