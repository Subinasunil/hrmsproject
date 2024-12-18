# Generated by Django 5.0.6 on 2024-09-21 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0100_remove_selectedempnotify_selected_ess_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='approvallevel',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='approvallevel',
            name='common_workflow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requesttype',
            name='use_common_workflow',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='approvallevel',
            name='request_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_levels', to='EmpManagement.requesttype'),
        ),
        migrations.AlterUniqueTogether(
            name='approvallevel',
            unique_together={('level', 'request_type', 'common_workflow')},
        ),
    ]
