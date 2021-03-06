# Generated by Django 2.2.4 on 2019-08-24 10:46

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('residents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('thumbnail', models.ImageField(upload_to='announcement/')),
                ('body', tinymce.models.HTMLField()),
                ('publish_datetime', models.DateTimeField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Area')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Community')),
            ],
        ),
    ]
