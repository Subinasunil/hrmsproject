# Generated by Django 5.0.4 on 2024-07-04 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0007_weekenddetail_month_of_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='weekend_calendar',
            name='friday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
        migrations.AddField(
            model_name='weekend_calendar',
            name='monday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
        migrations.AddField(
            model_name='weekend_calendar',
            name='saturday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
        migrations.AddField(
            model_name='weekend_calendar',
            name='sunday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
        migrations.AddField(
            model_name='weekend_calendar',
            name='thursday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
        migrations.AddField(
            model_name='weekend_calendar',
            name='tuesday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
        migrations.AddField(
            model_name='weekend_calendar',
            name='wednesday',
            field=models.CharField(choices=[('leave', 'Leave'), ('fullday', 'fullday'), ('halfday', 'Halfday')], default='fullday'),
        ),
    ]
