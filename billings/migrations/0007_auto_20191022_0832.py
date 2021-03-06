# Generated by Django 2.2.4 on 2019-10-22 00:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0006_auto_20191013_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='bill_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='receipt',
            field=models.ImageField(upload_to='bankSlip/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'png'])], verbose_name='Bank Slip'),
        ),
    ]
