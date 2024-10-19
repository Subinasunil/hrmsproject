# Generated by Django 5.0.4 on 2024-06-04 06:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrganisationManager', '0002_remove_fiscalyear_company_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='brnch_mstr',
            name='br_start_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='brnch_mstr',
            name='branch_code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='brnch_mstr',
            name='branch_users',
            field=models.ManyToManyField(related_name='branches', to=settings.AUTH_USER_MODEL),
        ),
    ]