# Generated by Django 5.0.6 on 2024-07-26 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0021_remove_emp_customfield_date_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_documents',
            name='emp_sl_no',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, unique=True),
        ),
    ]