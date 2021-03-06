# Generated by Django 2.2.4 on 2019-10-06 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security_guards', '0002_security_identity_no'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicenumber',
            options={'verbose_name': 'Tracking Device', 'verbose_name_plural': 'Tracking Devices'},
        ),
        migrations.AlterModelOptions(
            name='passnumber',
            options={'verbose_name': 'Visitor Pass', 'verbose_name_plural': 'Visiter Pass'},
        ),
        migrations.AlterModelOptions(
            name='security',
            options={'verbose_name': 'Security Guard', 'verbose_name_plural': 'Security Guards'},
        ),
        migrations.AlterField(
            model_name='devicenumber',
            name='device_no',
            field=models.CharField(max_length=150, verbose_name='Device No.'),
        ),
        migrations.AlterField(
            model_name='passnumber',
            name='pass_no',
            field=models.CharField(max_length=150, verbose_name='Pass No.'),
        ),
    ]
