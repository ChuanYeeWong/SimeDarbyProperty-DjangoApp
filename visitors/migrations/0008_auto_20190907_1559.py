# Generated by Django 2.2.4 on 2019-09-07 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0007_auto_20190907_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry_schedule',
            name='days',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
