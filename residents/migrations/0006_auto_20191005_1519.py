# Generated by Django 2.2.4 on 2019-10-05 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0005_auto_20190930_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='residents.Community'),
        ),
    ]
