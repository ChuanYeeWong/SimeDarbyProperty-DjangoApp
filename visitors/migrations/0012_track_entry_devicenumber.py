# Generated by Django 2.2.4 on 2019-09-16 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security_guards', '0001_initial'),
        ('visitors', '0011_auto_20190916_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='track_entry',
            name='deviceNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='security_guards.DeviceNumber'),
        ),
    ]
