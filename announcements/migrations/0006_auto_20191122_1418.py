# Generated by Django 2.2.4 on 2019-11-22 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0005_auto_20191110_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='title',
            field=models.CharField(help_text='Not more than 150 characters.', max_length=150),
        ),
    ]
