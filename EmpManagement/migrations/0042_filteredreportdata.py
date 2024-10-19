# Generated by Django 5.0.6 on 2024-08-07 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0041_delete_filtereddata'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteredReportData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filtered_data', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.doc_report')),
            ],
        ),
    ]
