# Generated by Django 2.2.8 on 2020-07-11 00:10

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0012_auto_20200520_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadbnxoutsetsva',
            name='upload',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/critter/Cactus/cactus/media/BNMX_OUTSETSVA'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='uploadtefout',
            name='upload',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/critter/Cactus/cactus/media/BNMX_OUTSETSVA'), upload_to=''),
        ),
    ]
