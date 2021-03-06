# Generated by Django 2.2.4 on 2019-12-09 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security_guards', '0005_post_log_qr_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_log',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='residents.Area'),
        ),
        migrations.AlterField(
            model_name='post_log',
            name='security_guard',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='security_guards.Security'),
        ),
    ]
