# Generated by Django 4.2.13 on 2024-06-10 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodbank', '0009_rename_individualshift_volunteer_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='total_passenger_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(default='', max_length=255),
        ),
    ]