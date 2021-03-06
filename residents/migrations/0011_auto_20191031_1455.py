# Generated by Django 2.2.4 on 2019-10-31 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0010_auto_20191012_2145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='residentlotthroughmodel',
            options={'ordering': ('order',), 'verbose_name': "Resident's House No", 'verbose_name_plural': "Residents's House No"},
        ),
        migrations.AlterField(
            model_name='resident',
            name='default_lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_lot', to='residents.Lot', verbose_name='Default House No'),
        ),
    ]
