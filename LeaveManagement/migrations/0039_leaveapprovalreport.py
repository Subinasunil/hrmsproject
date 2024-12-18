# Generated by Django 5.0.6 on 2024-10-26 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0038_rename_rejectionreason_lvrejectionreason'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveApprovalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, null=True, unique=True)),
                ('report_data', models.FileField(blank=True, null=True, upload_to='leave_approval_report/')),
            ],
            options={
                'permissions': (('export_report', 'Can export report'),),
            },
        ),
    ]
