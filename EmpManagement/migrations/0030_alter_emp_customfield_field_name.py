# Generated by Django 5.0.6 on 2024-07-27 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0029_emp_customfieldvalue_emp_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_customfield',
            name='field_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]