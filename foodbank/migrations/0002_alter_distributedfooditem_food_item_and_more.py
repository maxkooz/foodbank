# Generated by Django 4.2.10 on 2024-06-07 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodbank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributedfooditem',
            name='food_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.fooditem'),
        ),
        migrations.AlterField(
            model_name='distributedfooditem',
            name='recipient_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.recipientorganization'),
        ),
        migrations.AlterField(
            model_name='foodbank',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.volunteer'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='associated_food_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.foodbank'),
        ),
        migrations.AlterField(
            model_name='individualshift',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.task'),
        ),
        migrations.AlterField(
            model_name='individualshift',
            name='volunteer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.volunteer'),
        ),
        migrations.AlterField(
            model_name='recipientorganization',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='associated_food_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.foodbank'),
        ),
        migrations.AlterField(
            model_name='transitschedule',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.vehicle'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='driver_volunteer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodbank.volunteer'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
