# Generated by Django 2.2.4 on 2019-12-02 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0016_track_entry_security'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track_entry',
            name='with_vehicle',
            field=models.BooleanField(default=True),
        ),
    ]
