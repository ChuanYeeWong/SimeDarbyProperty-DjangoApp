# Generated by Django 2.2.4 on 2019-08-24 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('residents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReasonSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=255)),
                ('salt', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], default='I', max_length=1)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Area')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Community')),
            ],
            options={
                'verbose_name_plural': 'Security Guards',
            },
        ),
        migrations.CreateModel(
            name='PassNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_no', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Area')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Community')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_no', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Area')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Community')),
            ],
        ),
        migrations.CreateModel(
            name='BoomgateLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('E', 'Entry Boomgate'), ('X', 'Exit Boomgate')], default='E', max_length=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security_guards.ReasonSetting')),
                ('security_guard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security_guards.Security')),
            ],
        ),
    ]
