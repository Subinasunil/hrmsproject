# Generated by Django 5.0.4 on 2024-05-22 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0002_remove_emp_master_emp_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_master',
            name='emp_marital_status',
            field=models.CharField(blank=True, choices=[('Married', 'Married'), ('Single', 'Single'), ('Other', 'Other')], max_length=10, null=True),
        ),
    ]
