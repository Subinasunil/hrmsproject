# Generated by Django 5.0.6 on 2024-09-03 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0084_delete_generalrequestreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralRequestReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, null=True, unique=True)),
                ('report_data', models.FileField(blank=True, null=True, upload_to='general_report/')),
            ],
            options={
                'permissions': (('export_general_request_report', 'Can export general request report'),),
            },
        ),
    ]