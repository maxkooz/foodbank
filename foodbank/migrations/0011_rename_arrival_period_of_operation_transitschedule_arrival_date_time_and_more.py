# Generated by Django 4.2.13 on 2024-06-10 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodbank', '0010_alter_vehicle_total_passenger_capacity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transitschedule',
            old_name='arrival_period_of_operation',
            new_name='arrival_date_time',
        ),
        migrations.RenameField(
            model_name='transitschedule',
            old_name='departure_period_of_operation',
            new_name='departure_date_time',
        ),
    ]
