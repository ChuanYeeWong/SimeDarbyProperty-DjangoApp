# Generated by Django 2.2.4 on 2019-12-09 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0013_auto_20191202_1244'),
        ('security_guards', '0003_auto_20191006_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='post_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('longitude', models.CharField(max_length=150)),
                ('latitude', models.CharField(max_length=150)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Area')),
                ('security_guard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security_guards.Security')),
            ],
        ),
    ]
