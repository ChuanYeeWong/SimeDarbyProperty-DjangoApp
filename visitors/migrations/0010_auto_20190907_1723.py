# Generated by Django 2.2.4 on 2019-09-07 09:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0009_entry_schedule_lot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry_schedule',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
