# Generated by Django 2.2.4 on 2019-10-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0013_visitors_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry_schedule',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
