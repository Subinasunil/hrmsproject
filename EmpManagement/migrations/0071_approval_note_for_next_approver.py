# Generated by Django 5.0.6 on 2024-08-21 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0070_emp_customfield_emp_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='note_for_next_approver',
            field=models.TextField(blank=True, null=True),
        ),
    ]
