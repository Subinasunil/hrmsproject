# Generated by Django 5.0.6 on 2024-09-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0109_alter_emailtemplate_template_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='use_common_template',
            field=models.BooleanField(default=False),
        ),
    ]