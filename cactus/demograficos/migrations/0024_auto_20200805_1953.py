# Generated by Django 2.2.8 on 2020-08-06 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0023_auto_20200804_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='con_seguro',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]
