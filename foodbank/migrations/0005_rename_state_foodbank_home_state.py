# Generated by Django 4.2.13 on 2024-06-07 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodbank', '0004_foodbank_zip_code_alter_foodbank_manager'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodbank',
            old_name='state',
            new_name='home_state',
        ),
    ]
