# Generated by Django 5.0.6 on 2024-07-29 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0038_alter_doc_report_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doc_report',
            options={'permissions': (('export_document_report', 'Can export doc report'),)},
        ),
        migrations.AlterModelOptions(
            name='generalrequestreport',
            options={'permissions': (('export_general_request_report', 'Can export general request report'),)},
        ),
    ]
