# Generated by Django 5.0.6 on 2024-07-19 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0013_doc_report_generalrequestreport_report_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_master',
            name='emp_mobile_number_1',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emp_master',
            name='emp_mobile_number_2',
            field=models.CharField(blank=True, null=True),
        ),
    ]