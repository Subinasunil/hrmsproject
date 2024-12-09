# Generated by Django 5.0.6 on 2024-12-05 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrganisationManager', '0015_assetmaster_assettransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmaster',
            name='available_quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='assetmaster',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assetmaster',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='assetmaster',
            name='total_quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
