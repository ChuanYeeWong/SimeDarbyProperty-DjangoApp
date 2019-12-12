# Generated by Django 2.2.4 on 2019-11-27 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security_guards', '0003_auto_20191006_1603'),
        ('visitors', '0015_track_entry_with_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='track_entry',
            name='security',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='security_guards.Security'),
        ),
    ]