# Generated by Django 5.0.4 on 2024-06-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign_weekend',
            name='target_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
