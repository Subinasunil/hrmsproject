# Generated by Django 5.0.6 on 2024-10-25 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveManagement', '0037_rejectionreason_leaveapproval_rejection_reason'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RejectionReason',
            new_name='LvRejectionReason',
        ),
    ]
