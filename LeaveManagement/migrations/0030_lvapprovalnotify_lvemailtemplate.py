# Generated by Django 5.0.6 on 2024-10-21 11:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0113_delete_emailverification'),
        ('LeaveManagement', '0029_leaveapproval_leaveapprovallevels'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LvApprovalNotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('recipient_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
                ('recipient_user_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LvEmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(choices=[('request_created', 'Request Created'), ('request_approved', 'Request Approved'), ('request_rejected', 'Request Rejected')], max_length=50)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('request_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_templates', to='LeaveManagement.leave_type')),
            ],
        ),
    ]
