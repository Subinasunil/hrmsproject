# Generated by Django 5.0.6 on 2024-09-11 06:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0002_selectedessuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectedessuser',
            name='selected_ess_user',
        ),
        migrations.AddField(
            model_name='selectedessuser',
            name='selected_ess_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]