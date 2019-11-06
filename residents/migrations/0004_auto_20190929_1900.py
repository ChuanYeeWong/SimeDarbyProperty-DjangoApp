# Generated by Django 2.2.4 on 2019-09-29 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0003_resident_default_lot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Lot', verbose_name='House No.'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='lot',
            field=models.ManyToManyField(through='residents.ResidentLotThroughModel', to='residents.Lot', verbose_name='House No.'),
        ),
        migrations.AlterField(
            model_name='residentlotthroughmodel',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residents.Lot', verbose_name='House No.'),
        ),
    ]
