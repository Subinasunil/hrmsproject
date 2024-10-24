# Generated by Django 5.0.4 on 2024-05-30 06:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrganisationManager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fiscalyear',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='fiscalperiod',
            name='company',
        ),
        migrations.AddField(
            model_name='fiscalperiod',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fiscal_periods', to='OrganisationManager.brnch_mstr'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fiscalyear',
            name='branch_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='OrganisationManager.brnch_mstr'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='cmpny_mastr',
        ),
    ]
