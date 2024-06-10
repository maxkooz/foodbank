# Generated by Django 4.2.13 on 2024-06-10 22:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodbank', '0011_rename_arrival_period_of_operation_transitschedule_arrival_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitschedule',
            name='arrival_date_time',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 9, 0)),
        ),
        migrations.AlterField(
            model_name='transitschedule',
            name='current_available_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transitschedule',
            name='departure_date_time',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 12, 0)),
        ),
    ]