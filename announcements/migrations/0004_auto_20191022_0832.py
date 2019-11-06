# Generated by Django 2.2.4 on 2019-10-22 00:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0003_auto_20191006_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='thumbnail',
            field=models.ImageField(upload_to='announcement/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])]),
        ),
    ]
